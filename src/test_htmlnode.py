import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

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

    def test_repr(self):
        node = HTMLNode("p", "Hello there", None, {"href": "https://www.google.com"})
        self.assertEqual(repr(node), "HTMLNode(p, Hello there, children: None, {'href': 'https://www.google.com'})")

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

    def test_repr(self):
        node = LeafNode("p", "Test")
        self.assertEqual(repr(node), "LeafNode(p, Test)")

child_nodes = [
    LeafNode("i", "italic text"), 
    LeafNode("b", "bold text"),
    LeafNode(None, "Raw text"),
    LeafNode("a", "Click me!", {"href": "https://www.google.com"})
]

class TestParentNode(unittest.TestCase):
    def test_no_tag(self):
        node = ParentNode(None, None, child_nodes)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_empty_tag(self):
        node = ParentNode("", None, child_nodes)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_no_children(self):
        node = ParentNode("p", None, None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_empty_children_list(self):
        node = ParentNode("p", None, [])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_no_props(self):
        node = ParentNode("p", None, child_nodes)
        self.assertEqual(node.to_html(), "<p><i>italic text</i><b>bold text</b>Raw text<a href='https://www.google.com'>Click me!</a></p>")

    def test_to_html_props(self):
        node = ParentNode("a", None, child_nodes, test_node1)
        self.assertEqual(node.to_html(), "<a href='https://www.google.com' target='_blank'><i>italic text</i><b>bold text</b>Raw text<a href='https://www.google.com'>Click me!</a></a>")

    def test_to_html_empty_props(self):
        node = ParentNode("p", None, child_nodes, {})
        self.assertEqual(node.to_html(), "<p><i>italic text</i><b>bold text</b>Raw text<a href='https://www.google.com'>Click me!</a></p>")

    def test_to_html_one_child(self):
        node = ParentNode("p", None, [LeafNode("b", "bold text")])
        self.assertEqual(node.to_html(), "<p><b>bold text</b></p>")

    def test_child_node_is_list(self):
        node = ParentNode("p", None, LeafNode("b", "bold text"))
        with self.assertRaises(TypeError):
            node.to_html()

    def test_child_node_tuple(self):
        node = ParentNode("p", None, (LeafNode("b", "bold text")))
        with self.assertRaises(TypeError):
            node.to_html()

    def test_parent_as_child_to_html(self):
        parent_as_child_node = [ParentNode("a", None, child_nodes, test_node1)]
        node = ParentNode("p", None, parent_as_child_node)
        self.assertEqual(node.to_html(), "<p><a href='https://www.google.com' target='_blank'><i>italic text</i><b>bold text</b>Raw text<a href='https://www.google.com'>Click me!</a></a></p>")

    def test_repr(self):
        node = ParentNode("p", None, [LeafNode("b", "bold text")])
        self.assertEqual(repr(node), "ParentNode(p, value: None, [LeafNode(b, bold text)])")
    

if __name__ == "__main__":
    unittest.main()
