from collections import deque
from bs4 import Tag
from typing import Any
import htmlentities
from .exceptions import TagCanNotBeSplittenError

END_TAG = 3  # closing tag symbols '</>'

BLOCK_TAGS = ["p", "b", "strong", "i", "ul", "ol", "div", "span"]


def list_to_str(lst: list) -> str:
    return "".join(lst)


def opening_tag_html(tag: str, attrs: dict[str, str | Any]) -> str:
    opening_tag = []
    opening_tag.append(f"<{tag}")
    if attrs:
        for key, value in attrs.items():
            if isinstance(value, list):
                value = " ".join(value)
            opening_tag.append(f' {key}="{value}"')

    opening_tag.append(">")
    return list_to_str(opening_tag)


def closing_tag_html(tag: str):
    return f"</{tag}>"


def closing_parent_tags_html(tags_hierarchy: deque) -> str:
    closing_tags = []
    for tag in tags_hierarchy:
        tag_name = tag.get_name()
        closing_tag = closing_tag_html(tag.get_name()) + tag.get_after_tag_content()
        if tag_name not in BLOCK_TAGS:
            raise TagCanNotBeSplittenError(opening_tag_html(tag.get_name(), tag.get_attrs()))
        closing_tags.append(closing_tag)

    return list_to_str(reversed(closing_tags))


def content_before_tags(element: Tag):
    content_buffer = []
    for content in element.children:
        if isinstance(content, Tag) and not str(content).isspace():
            break
        else:
            content_buffer.append(htmlentities.encode(content))
    return list_to_str(content_buffer)


def content_after_tags(element: Tag) -> str:
    content_buffer = []
    for content in element.next_siblings:
        if isinstance(content, Tag) and not str(content).isspace():
            break
        else:
            content_buffer.append(htmlentities.encode(content))
    return list_to_str(content_buffer)


def count_child_nodes(element: Tag) -> int:
    count = 0
    for child_node in element.children:
        if isinstance(child_node, Tag):
            count += 1
    return count
