import unittest
from textnode import TextNode

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
        node = TextNode("Printed", "text")
        self.assertEqual(repr(node), "TextNode(Printed, Text)")

if __name__ == "__main__":
    unittest.main()
