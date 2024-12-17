from collections import deque
from typing import Generator, Any
from bs4 import BeautifulSoup, Tag, NavigableString
from .counter import ThreadSafeCounter
from .exceptions import MaxLengthExceededError, TagCanNotBeSplittenError
import array
from .helpers import *

buffer = array.array('u')

MAX_LEN = 4096

END_TAG = 3 # closing tag symbols '</>'

def write(data: str):
	global buffer
	buffer.fromunicode(data)

def split_message(source: str, max_len=MAX_LEN) -> Generator[str, None, None]:
	"""Splits the original message (`source`) into fragments of the specified length
	(`max_len`)."""
	global buffer
	tags_hierarchy = deque()

	length = 0

	soup = BeautifulSoup(source, 'html.parser')

	partial_html = ""

	for element in soup.descendants:
		if isinstance(element, Tag):
			if isinstance(element.parent, BeautifulSoup):
				if partial_html:
					partial_html += closing_parent_tags_html(tags_hierarchy)
					tags_hierarchy.clear()
				else:
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

			length += opening_tag_len + before_tag_content_len + closing_tag_len + after_tag_content_len

			child_nodes_count = len([child_node for child_node in element.children if isinstance(child_node, Tag)])

			if length >= max_len:
				if isinstance(element.parent, BeautifulSoup):
					raise MaxLengthExceededError(
						f'{opening_tag}({opening_tag_len})' \
						f' + {before_tag_content}({before_tag_content_len})' \
						f' + {closing_tag}({closing_tag_len})' \
						f' + {after_tag_content}({after_tag_content_len}) = {length} >= {max_len}'
					)
				elif partial_html_used:
					raise TagCanNotBeSplittenError(
						f'{opening_tag}({opening_tag_len})' \
						f' + {before_tag_content}({before_tag_content_len})' \
						f' + {closing_tag}({closing_tag_len})' \
						f' + {after_tag_content}({after_tag_content_len}) = {length} >= {max_len}'
					)
				else:

					partial_data = []
					closest_tag = element.parent

					while not isinstance(closest_tag, BeautifulSoup):
						partial_data.append(opening_tag_html(closest_tag.name, closest_tag.attrs))
						closest_tag = closest_tag.parent
					
					partial_html = ''.join(reversed(partial_data)) + opening_tag + before_tag_content

					if child_nodes_count == 0:
						partial_html += closing_tag_html(tag_name)
						
					if len(buffer) != 0:
						write(closing_parent_tags_html(tags_hierarchy))

					length = 0

					for tag_in_hierarchy in tags_hierarchy:
						length += len(tag_in_hierarchy.get_name()) + END_TAG + len(tag_in_hierarchy.get_after_tag_content())
					
					length += after_tag_content_len

					content = buffer.tounicode()
					buffer = array.array('u')
					yield content
			else:

				if child_nodes_count == 0:
					write(opening_tag + before_tag_content + closing_tag + after_tag_content)

					while tags_hierarchy \
						and (tag_hierarchy := tags_hierarchy[-1]) \
						and (tag_hierarchy.decrement() == 0):
						write(closing_tag_html(tag_hierarchy.get_name()) + tag_hierarchy.get_after_tag_content())
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
		raise TagCanNotBeSplittenError(
					f'{partial_html} = {partial_html_len} > {max_len}'
				)
	
	if len(buffer) > 0:
		yield buffer.tounicode()
	
	if len(partial_html) > 0:
		yield partial_html
