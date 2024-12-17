from collections import deque
from typing import Generator
from bs4 import BeautifulSoup, Tag
from .counter import ThreadSafeCounter
from .exceptions import MaxLengthExceededError
import array
from .helpers import (
    closing_parent_tags_html,
    opening_tag_html,
    content_before_tags,
    closing_tag_html,
    content_after_tags,
    count_child_nodes,
    list_to_str,
    END_TAG,
)

buffer = array.array("u")

MAX_LEN = 4096


def write(data: str):
    global buffer
    buffer.fromunicode(data)


def split_message(source: str, max_len=MAX_LEN) -> Generator[str, None, None]:
    """Splits the original message (`source`) into fragments of the specified length
    (`max_len`)."""
    global buffer
    tags_hierarchy = deque()

    length = 0

    soup = BeautifulSoup(source, "html.parser")

    partial_html = ""

    for element in soup.descendants:
        if isinstance(element, Tag):
            if isinstance(element.parent, BeautifulSoup):
                if partial_html:
                    partial_html += closing_parent_tags_html(tags_hierarchy)
                tags_hierarchy.clear()

            tag_name = element.name
            tag_attrs = element.attrs
            partial_html_used = False

            opening_tag = ""

            if partial_html:
                opening_tag += partial_html
                partial_html = ""
                partial_html_used = True

            opening_tag += opening_tag_html(tag_name, tag_attrs)
            before_tag_content = content_before_tags(element)
            closing_tag = closing_tag_html(tag_name)
            after_tag_content = content_after_tags(element)

            opening_tag_len = len(opening_tag)
            before_tag_content_len = len(before_tag_content)
            closing_tag_len = len(closing_tag)
            after_tag_content_len = len(after_tag_content)

            length += (
                opening_tag_len
                + before_tag_content_len
                + closing_tag_len
                + after_tag_content_len
            )

            child_nodes_count = count_child_nodes(element)

            if length >= max_len:
                if isinstance(element.parent, BeautifulSoup) or partial_html_used:
                    raise MaxLengthExceededError(
                        f"{opening_tag}({opening_tag_len})"
                        f" + {before_tag_content}({before_tag_content_len})"
                        f" + {closing_tag}({closing_tag_len})"
                        f" + {after_tag_content}({after_tag_content_len}) = {length} >= {max_len}"
                    )
                else:
                    partial_data = []
                    closest_tag = element.parent

                    while not isinstance(closest_tag, BeautifulSoup):
                        partial_data.append(
                            opening_tag_html(closest_tag.name, closest_tag.attrs)
                        )
                        closest_tag = closest_tag.parent

                    partial_html = list_to_str(
                        list(reversed(partial_data)) + [opening_tag, before_tag_content]
                    )

                    if child_nodes_count == 0:
                        partial_html += closing_tag_html(tag_name)

                    if len(buffer) != 0:
                        write(closing_parent_tags_html(tags_hierarchy))

                    length = 0

                    for tag_in_hierarchy in tags_hierarchy:
                        length += (
                            len(tag_in_hierarchy.get_name())
                            + END_TAG
                            + len(tag_in_hierarchy.get_after_tag_content())
                        )

                    length += after_tag_content_len

                    content = buffer.tounicode()
                    buffer = array.array("u")
                    yield content
            else:
                if child_nodes_count == 0:
                    write(
                        opening_tag
                        + before_tag_content
                        + closing_tag
                        + after_tag_content
                    )

                    while (
                        tags_hierarchy
                        and (tag_hierarchy := tags_hierarchy[-1])
                        and (tag_hierarchy.decrement() == 0)
                    ):
                        write(
                            closing_tag_html(tag_hierarchy.get_name())
                            + tag_hierarchy.get_after_tag_content()
                        )
                        tags_hierarchy.pop()

                else:
                    write(opening_tag + before_tag_content)

            if child_nodes_count > 0:
                current_tag_info = ThreadSafeCounter(element, child_nodes_count)
                tags_hierarchy.append(current_tag_info)
        else:
            pass

    partial_html += closing_parent_tags_html(tags_hierarchy)
    partial_html_len = len(partial_html)

    if partial_html_len > max_len:
        raise MaxLengthExceededError(f"{partial_html} = {partial_html_len} > {max_len}")

    if len(buffer) > 0:
        yield buffer.tounicode()

    if len(partial_html) > 0:
        yield partial_html
