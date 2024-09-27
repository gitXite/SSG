import unittest
from main import text_node_to_html_node
from node_helpers import *
from textnode import TextNode
from htmlnode import HTMLNode, LeafNode, ParentNode

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
    
