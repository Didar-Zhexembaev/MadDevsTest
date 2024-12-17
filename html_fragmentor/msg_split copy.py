from collections import deque
from typing import Generator, Any
from bs4 import BeautifulSoup, Tag, NavigableString
from .counter import ThreadSafeCounter
from .exceptions import MaxLengthExceededError, TagCanNotBeSplittenError
import array
import htmlentities

buffer = array.array('u')

MAX_LEN = 4096

BLOCK_TAGS = ['p', 'b', 'strong', 'i', 'ul', 'ol', 'div', 'span']

END_TAG = 3 # closing tag symbols '</>'

def opening_tag_html(tag: str, attrs: dict[str, str | Any]):
	opening_tag = []
	opening_tag.append(f'<{tag}')
	if attrs:
		for key, value in attrs.items():
			if isinstance(value, list):
				value = ' '.join(value)
			opening_tag.append(f' {key}="{value}"')

	opening_tag.append('>')
	return ''.join(opening_tag)

def closing_tag_html(tag: str):
	return f'</{tag}>'

def write(data: str):
	global buffer
	buffer.fromunicode(data)

def content_before_tags(element):
	content_buffer = []
	for content in element.children:
		if isinstance(content, Tag) and not str(content).isspace():
			break
		else:
			content_buffer.append(htmlentities.encode(content))
	return ''.join(content_buffer)

def content_after_tags(element):
	content_buffer = []
	for content in element.next_siblings:
		if isinstance(content, Tag) and not str(content).isspace():
			break
		else:
			content_buffer.append(htmlentities.encode(content))
	return ''.join(content_buffer)

def list_to_str(lst: list) -> str:
	return ''.join(lst)

def split_message(source: str, max_len=MAX_LEN) -> Generator[str, None, None]:
	"""Splits the original message (`source`) into fragments of the specified length
	(`max_len`)."""
	global buffer
	tags_hierarchy = deque()

	length = 0
	max_len = 135

	soup = BeautifulSoup(source, 'html.parser')

	partial_html = ""

	for element in soup.descendants:
		if isinstance(element, Tag):
			if isinstance(element.parent, BeautifulSoup):
				if partial_html:
					partial_html += ''.join(reversed([closing_tag_html(tag.get_key()) for tag in tags_hierarchy if tag.get_value() > 0]))
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

			opening_tag_len = len(opening_tag)
			before_tag_content_len = len(before_tag_content)
			closing_tag_len = len(closing_tag)

			length += opening_tag_len + before_tag_content_len + closing_tag_len

			child_nodes_count = len([child_node for child_node in element.children if isinstance(child_node, Tag)])

			if length > max_len:
				if isinstance(element.parent, BeautifulSoup):
					raise MaxLengthExceededError(
						f'{opening_tag}({opening_tag_len})' \
						f' + {before_tag_content}({before_tag_content_len})' \
						f' + {closing_tag}({closing_tag_len}) = {length} > {max_len}'
					)
				elif partial_html_used:
					raise TagCanNotBeSplittenError(
						f'{opening_tag}({opening_tag_len})' \
						f' + {before_tag_content}({before_tag_content_len})' \
						f' + {closing_tag}({closing_tag_len}) = {length} > {max_len}'
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
						# if tags_hierarchy \
						# 	and (last_tag := tags_hierarchy[-1]) \
						# 	and last_tag.decrement() == 0:
						# 	partial_html += closing_tag_html(last_tag.get_key())
						# 	tags_hierarchy.pop()
					
					if len(buffer) != 0:
						write(''.join(reversed([closing_tag_html(tag.get_key()) for tag in tags_hierarchy if tag.get_value() > 0])))

					length = 0

					for tag_in_hierarchy in tags_hierarchy:
						length += len(tag_in_hierarchy.get_key()) + END_TAG

					content = buffer.tounicode()
					buffer = array.array('u')

					yield content
			else:

				if child_nodes_count == 0:
					write(opening_tag + before_tag_content + closing_tag)

					while tags_hierarchy \
						and (tag_hierarchy := tags_hierarchy[-1]) \
						and (tag_hierarchy.decrement() == 0):
						write(closing_tag_html(tag_hierarchy.get_key()))
						tags_hierarchy.pop()
					
				else:
					write(opening_tag + before_tag_content)
			
			if child_nodes_count > 0:
				current_tag_info = ThreadSafeCounter(tag_name, child_nodes_count, tag_attrs)
				tags_hierarchy.append(current_tag_info)
		else:
			pass
	
	partial_html += ''.join(reversed([closing_tag_html(tag.get_key()) for tag in tags_hierarchy if tag.get_value() > 0]))
	partial_html_len = len(partial_html)

	if partial_html_len > max_len:
		raise TagCanNotBeSplittenError(
					f'{partial_html} = {partial_html_len} > {max_len}'
				)
	
	if len(buffer) > 0:
		yield buffer.tounicode()
	
	if len(partial_html) > 0:
		yield partial_html

