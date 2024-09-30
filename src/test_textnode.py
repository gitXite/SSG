import unittest
from textnode import TextNode
from node_helpers import *

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a test node", "bold")
        node2 = TextNode("This is a test node", "bold")     
        self.assertEqual(node, node2)

    def test_url_none(self):
        node = TextNode("This is also a test node", "italic", None)
        node2 = TextNode("This is also a test node", "italic", None)
        self.assertEqual(node, node2)

    def test_noneq(self):
        node = TextNode("We are not the same", "bold")
        node2 = TextNode("Are you sure?", "bold")
        self.assertNotEqual(node, node2)

    def test_noneq2(self):
        node = TextNode("We are the same", "italic")
        node2 = TextNode("We are the same", "bold")
        self.assertNotEqual(node, node2)

    def test_url(self):
        node = TextNode("Text", "bold", "https://www.text.com")
        node2 = TextNode("Text", "bold", "https://www.text.com")
        self.assertEqual(node, node2)

    def test_noneq_url(self):
        node = TextNode("Text", "italic", "url")
        node2 = TextNode("Text", "italic", "https://www.url.com")
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode("Printed", "text", "https://www.url.com")
        self.assertEqual(repr(node), "TextNode(Printed, text, https://www.url.com)")

class TestTextNodeToLeafNodeConversion(unittest.TestCase):
	def test_text_node(self):
		node = TextNode("Test", "text")
		self.assertEqual(create_text_node(node), LeafNode(None, "Test"))
		
	def test_bold_node(self):
		node = TextNode("Test", "bold")
		self.assertEqual(create_bold_node(node), LeafNode("b", "Test"))

	def test_italic_node(self):
		node = TextNode("Test", "italic")
		self.assertEqual(create_italic_node(node), LeafNode("i", "Test"))

	def test_code_node(self):
		node = TextNode("Test", "code")
		self.assertEqual(create_code_node(node), LeafNode("code", "Test"))

	def test_link_node(self):
		node = TextNode("Click me!", "link", "https://www.google.com")
		self.assertEqual(create_link_node(node), LeafNode("a", "Click me!", {"href": "https://www.google.com"}))

	def test_img_node(self):
		node = TextNode("Google logo", "img", "image.jpg")
		self.assertEqual(create_img_node(node), LeafNode("img", "", {"src": "image.jpg", "alt": "Google logo"}))

	def test_text_node_to_html_node_invalid_type(self):
		text_node = TextNode("Test", "invalid")
		with self.assertRaises(Exception):
			text_node_to_html_node(text_node)

	def test_text_node_to_html_node(self):
		text_node = TextNode("Test", "italic")
		self.assertEqual(text_node_to_html_node(text_node), LeafNode("i", "Test"))

if __name__ == "__main__":
    unittest.main()
