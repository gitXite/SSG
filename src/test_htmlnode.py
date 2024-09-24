import unittest
from htmlnode import HTMLNode

test_node1 = {
    "href": "https://www.google.com", 
    "target": "_blank",
}
test_node2 = {
    "href": "https://www.google.com", 
    "target": "_blank",
}
test_node3 = {
    "href": "https://www.google", 
    "target": "blank",
}

class TestHTMLNode(unittest.TestCase):
    def test_to_html(self):
        node = HTMLNode("p", "Hello", None, None)
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_props_to_html(self):
        node1 = HTMLNode("p", "Hello there", None, test_node1)
        self.assertEqual(node1.props_to_html(), " href='https://www.google.com' target='_blank'")

    def test_props_to_html_2(self):
        node1 = HTMLNode("p", "Hello there", None, test_node1)
        node2 = HTMLNode("p", "Hello there", None, test_node2)
        self.assertEqual(node1.props_to_html(), node2.props_to_html())

    def test_props_to_html_noteq(self):
        node1 = HTMLNode("p", "Hello there", None, test_node1)
        self.assertNotEqual(node1.props_to_html(), " href='https://www.google'")

if __name__ == "__main__":
    unittest.main()
