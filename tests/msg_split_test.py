import unittest
from html_fragmentor import split_message, MAX_LEN


class TestMsgSplit(unittest.TestCase):
	def test_msg_split_with_source1_html(self):
		content = ''
		with open('tests/source1.html', 'r', encoding='utf-8') as f:
			content = f.read()
		
		for fragment in split_message(content):
			self.assertLessEqual(len(fragment), MAX_LEN)
	
	def test_msg_split_with_source2_html(self):
		content = ''
		with open('tests/source2.html', 'r', encoding='utf-8') as ft:
			content = ft.read()

		for fragment in split_message(content):
			self.assertLessEqual(len(fragment), MAX_LEN)

if __name__ == '__main__':
	unittest.main()