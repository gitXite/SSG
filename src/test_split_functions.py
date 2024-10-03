import unittest
from textnode import *
from split_functions import *

old_nodes = [
	TextNode("This is text with a `code block` word", "text"),
	TextNode("This is just some raw text", "text"),
	TextNode("This is text with **bold** delimiters", "text")
]

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_type_list(self):
        node = TextNode("This is text with a `code block` word", "text")
        with self.assertRaises(TypeError):
            split_nodes_delimiter(node, "`", "code")
			
    def test_empty_node(self):
        self.assertEqual(split_nodes_delimiter([], "**", "bold"), [])

    def test_split_nodes_delimiter(self):
        self.assertEqual(split_nodes_delimiter(old_nodes, "`", "code"), [
            TextNode("This is text with a ", "text"),
            TextNode("code block", "code"),
            TextNode(" word", "text"),
            TextNode("This is just some raw text", "text"),
            TextNode("This is text with **bold** delimiters", "text")
        ])

    def test_split_nodes_delimiter2(self):
        self.assertEqual(split_nodes_delimiter(old_nodes, "**", "bold"), [
            TextNode("This is text with a `code block` word", "text"),
            TextNode("This is just some raw text", "text"),
            TextNode("This is text with ", "text"),
            TextNode("bold", "bold"),
            TextNode(" delimiters", "text")
        ])

    def test_split_nodes_delimiter_multiple_delimiters(self):
        node = TextNode("This is some *text* with *multiple* delimiters", "text")
        self.assertEqual(split_nodes_delimiter([node], "*", "italic"), [
            TextNode("This is some ", "text"),
            TextNode("text", "italic"),
            TextNode(" with ", "text"),
            TextNode("multiple", "italic"),
            TextNode(" delimiters", "text")
        ])

    def test_split_nodes_delimiter_startswith(self):
        node = TextNode("**This is text** with a delimiter at the start", "text")
        self.assertEqual(split_nodes_delimiter([node], "**", "bold"), [
            TextNode("This is text", "bold"),
            TextNode(" with a delimiter at the start", "text")
        ])

    def test_split_nodes_delimiter_endswith(self):
        node = TextNode("This is text with a delimiter at the *end*", "text")
        self.assertEqual(split_nodes_delimiter([node], "*", "italic"), [
            TextNode("This is text with a delimiter at the ", "text"),
            TextNode("end", "italic")
        ])

    def test_split_nodes_delimiter_non_text_node(self):
        node = TextNode("This has wrong text type", "bold")
        self.assertEqual(split_nodes_delimiter([node], "`", "code"), [
		    TextNode("This has wrong text type", "bold")
	    ])

    def test_split_nodes_delimiter_not_in_text(self):
        node = TextNode("This is text with a `code block` word", "text")
        self.assertEqual(split_nodes_delimiter([node], "*", "italic"), [
            TextNode("This is text with a `code block` word", "text")
        ])

    def test_split_nodes_delimiter_none(self):
        node = TextNode("This is text with a `code block` word", "text")
        with self.assertRaises(TypeError):
            split_nodes_delimiter([node], None, None)

    def test_split_nodes_delimiter_empty_string(self):
        node = TextNode("", "text")
        self.assertEqual(split_nodes_delimiter([node], "`", "code"), [TextNode("", "text")])

    def test_consecutive_delimiters(self):
        node = TextNode("This text has **consecutive** **delimiters**", "text")
        self.assertEqual(split_nodes_delimiter([node], "**", "bold"), [
            TextNode("This text has ", "text"),
            TextNode("consecutive", "bold"),
            TextNode(" ", "text"),
            TextNode("delimiters", "bold")
        ])

class TestSplitNodesImage(unittest.TestCase):
    def test_split_nodes_image(self):
        pass

class TestSplitNodesLink(unittest.TestCase):
    def test_split_nodes_link(self):
        pass