import unittest
from htmlnode import HTMLNode, LeafNode

test_node1 = {
    "href": "https://www.google.com", 
    "target": "_blank",
}

class TestHTMLNode(unittest.TestCase):
    def test_to_html(self):
        node = HTMLNode("p", "Hello", None, None)
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_props_to_html(self):
        node = HTMLNode("p", "Hello there", None, test_node1)
        self.assertEqual(node.props_to_html(), " href='https://www.google.com' target='_blank'")

    def test_no_props_to_html(self):
        node = HTMLNode("p", "Hello there", None, None)
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_noteq(self):
        node = HTMLNode("p", "Hello there", None, test_node1)
        self.assertNotEqual(node.props_to_html(), " href='https://www.google.com'")

class TestLeafNode(unittest.TestCase):
    def test_raise_error(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_simple_to_html(self):
        node = LeafNode("p", "This is a test")
        self.assertEqual(node.to_html(), "<p>This is a test</p>")

    def test_empty_tag_to_html(self):
        node = LeafNode("", "Raw text")
        self.assertEqual(node.to_html(), "Raw text")

    def test_empty_value_to_html(self):
        node = LeafNode("p", "")
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_no_tag(self):
        node = LeafNode(None, "Raw text")
        self.assertEqual(node.to_html(), "Raw text")

    def test_to_html_with_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), "<a href='https://www.google.com'>Click me!</a>")

    def test_to_html_no_props(self):
        node = LeafNode("p", "No props", None)
        self.assertEqual(node.to_html(), "<p>No props</p>")

    def test_to_html_empty_props(self):
        node = LeafNode("p", "Empty props", {})
        self.assertEqual(node.to_html(), "<p>Empty props</p>")

if __name__ == "__main__":
    unittest.main()
