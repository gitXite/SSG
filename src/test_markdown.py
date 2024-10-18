import unittest
from markdown import *
from textnode import *
from htmlnode import HTMLNode


# to test split_nodes_delimiter()
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


class TestExtractMarkdown(unittest.TestCase):
    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual(extract_markdown_images(text), [
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"), 
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")
        ])

    def test_extract_markdown_images_without_alt_text(self):
        text = "This is text with a ![](https://i.imgur.com/aKaOqIh.gif) and ![](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual(extract_markdown_images(text), [
            ("", "https://i.imgur.com/aKaOqIh.gif"), 
            ("", "https://i.imgur.com/fJRm4Vk.jpeg")
        ])

    def test_extract_markdown_images_no_matches(self):
        text = "This is text with a [](https://i.imgur.com/aKaOqIh.gif) and !https://i.imgur.com/fJRm4Vk.jpeg"
        self.assertEqual(extract_markdown_images(text), [])

    
    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertEqual(extract_markdown_links(text), [
            ("to boot dev", "https://www.boot.dev"), 
            ("to youtube", "https://www.youtube.com/@bootdotdev")
        ])

    def test_extract_markdown_links_without_link(self):
        text = "This is text with a link [](https://www.boot.dev) and [](https://www.youtube.com/@bootdotdev)"
        self.assertEqual(extract_markdown_links(text), [
            ("", "https://www.boot.dev"), 
            ("", "https://www.youtube.com/@bootdotdev")
        ])

    def test_extract_markdown_links_no_matches(self):
        text = "This is text with a link to boot devhttps://www.boot.dev and to youtubehttps://www.youtube.com/@bootdotdev"
        self.assertEqual(extract_markdown_links(text), [])


# to test split_nodes_image/link()
nodes_simple = [
    TextNode("This is text without images or links", text_type_text),
    TextNode("This is ![some image](https://i.imgur.com/fJRm4Vk.jpeg)", text_type_text),
    TextNode("This is [some link](https://www.link.com)", text_type_text)
]
"""nodes_complex = [
    TextNode(),
    TextNode(),
    TextNode()
]"""


class TestSplitNodesImage(unittest.TestCase):
    def test_type_list(self):
        node = TextNode("This is ![some image](https://i.imgur.com/fJRm4Vk.jpeg)", text_type_text)
        with self.assertRaises(TypeError):
            split_nodes_image(node)

    def test_empty_list(self):
        self.assertEqual(split_nodes_image([]), [])
    
    def test_split_nodes_image(self):
        node = [TextNode("This is ![some image](https://i.imgur.com/fJRm4Vk.jpeg)", text_type_text)]
        self.assertEqual(split_nodes_image(node), [
            TextNode("This is ", text_type_text),
            TextNode("some image", text_type_image, "https://i.imgur.com/fJRm4Vk.jpeg")
        ])

    def test_split_nodes_image2(self):
        node = [TextNode("This is ![some image](https://i.imgur.com/fJRm4Vk.jpeg) and some more text", text_type_text)]
        self.assertEqual(split_nodes_image(node), [
            TextNode("This is ", text_type_text),
            TextNode("some image", text_type_image, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and some more text", text_type_text)
        ])

    def test_image_startswith(self):
        node = [TextNode("![some image](https://i.imgur.com/fJRm4Vk.jpeg) like this", text_type_text)]
        self.assertEqual(split_nodes_image(node), [
            TextNode("some image", text_type_image, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" like this", text_type_text)
        ])

    def test_multiple_images(self):
        node = [TextNode("This test contains images of ![birds](https://i.imgur.com/fJRm4Vk.jpeg) and the ![bees](https://i.imgur.com/fJRm4Vk.png)", text_type_text)]
        self.assertEqual(split_nodes_image(node), [
            TextNode("This test contains images of ", text_type_text),
            TextNode("birds", text_type_image, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and the ", text_type_text),
            TextNode("bees", text_type_image, "https://i.imgur.com/fJRm4Vk.png")
        ])

    def test_only_images_without_space(self):
        node = [TextNode("![Joe](/static/images/joe.jpeg)![Donald](/static/images/donald.jpeg)", text_type_text)]
        self.assertEqual(split_nodes_image(node), [
            TextNode("Joe", text_type_image, "/static/images/joe.jpeg"),
            TextNode("Donald", text_type_image, "/static/images/donald.jpeg")
        ])

    def test_only_images_with_space(self):
        node = [TextNode("![Joe](/static/images/joe.jpeg) ![Donald](/static/images/donald.jpeg)", text_type_text)]
        self.assertEqual(split_nodes_image(node), [
            TextNode("Joe", text_type_image, "/static/images/joe.jpeg"),
            TextNode(" ", text_type_text),
            TextNode("Donald", text_type_image, "/static/images/donald.jpeg")
        ])

    def test_without_alt(self):
        node = [TextNode("Image without alt text ![](/static/images/withoutalt.jpeg)", text_type_text)]
        self.assertEqual(split_nodes_image(node), [
            TextNode("Image without alt text ", text_type_text),
            TextNode("", text_type_image, "/static/images/withoutalt.jpeg")
        ])

    def test_multiple_nodes_simple(self):
        self.assertEqual(split_nodes_image(nodes_simple), [
            TextNode("This is text without images or links", text_type_text),
            TextNode("This is ", text_type_text),
            TextNode("some image", text_type_image, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode("This is [some link](https://www.link.com)", text_type_text)
        ])

    def test_multiple_nodes_complex(self):
        pass


class TestSplitNodesLink(unittest.TestCase):
    def test_type_list(self):
        node = TextNode("This is [some link](https://www.link.com)", text_type_text)
        with self.assertRaises(TypeError):
            split_nodes_link(node)

    def test_empty_list(self):
        self.assertEqual(split_nodes_link([]), [])
    
    def test_split_nodes_link(self):
        node = [TextNode("This is [some link](https://www.link.com)", text_type_text)]
        self.assertEqual(split_nodes_link(node), [
            TextNode("This is ", text_type_text),
            TextNode("some link", text_type_link, "https://www.link.com")
        ])

    def test_split_nodes_link2(self):
        node = [TextNode("This is [some link](https://www.link.com) and some more text", text_type_text)]
        self.assertEqual(split_nodes_link(node), [
            TextNode("This is ", text_type_text),
            TextNode("some link", text_type_link, "https://www.link.com"),
            TextNode(" and some more text", text_type_text)
        ])

    def test_link_startswith(self):
        node = [TextNode("[some link](https://www.link.com) like this", text_type_text)]
        self.assertEqual(split_nodes_link(node), [
            TextNode("some link", text_type_link, "https://www.link.com"),
            TextNode(" like this", text_type_text)
        ])

    def test_multiple_links(self):
        node = [TextNode("This test contains links to [google](https://www.google.com) and [bing](https://www.bing.com)", text_type_text)]
        self.assertEqual(split_nodes_link(node), [
            TextNode("This test contains links to ", text_type_text),
            TextNode("google", text_type_link, "https://www.google.com"),
            TextNode(" and ", text_type_text),
            TextNode("bing", text_type_link, "https://www.bing.com")
        ])

    def test_only_links_without_space(self):
        node = [TextNode("[Joe](https://www.google.com)[Donald](https://www.google.com)", text_type_text)]
        self.assertEqual(split_nodes_link(node), [
            TextNode("Joe", text_type_link, "https://www.google.com"),
            TextNode("Donald", text_type_link, "https://www.google.com")
        ])

    def test_only_links_with_space(self):
        node = [TextNode("[Joe](https://www.google.com) [Donald](https://www.google.com)", text_type_text)]
        self.assertEqual(split_nodes_link(node), [
            TextNode("Joe", text_type_link, "https://www.google.com"),
            TextNode(" ", text_type_text),
            TextNode("Donald", text_type_link, "https://www.google.com")
        ])

    def test_without_alt(self):
        node = [TextNode("Link without alt text [](https://www.google.com)", text_type_text)]
        self.assertEqual(split_nodes_link(node), [
            TextNode("Link without alt text ", text_type_text),
            TextNode("", text_type_link, "https://www.google.com")
        ])

    def test_multiple_nodes_simple(self):
        self.assertEqual(split_nodes_link(nodes_simple), [
            TextNode("This is text without images or links", text_type_text),
            TextNode("This is ![some image](https://i.imgur.com/fJRm4Vk.jpeg)", text_type_text),
            TextNode("This is ", text_type_text),
            TextNode("some link", text_type_link, "https://www.link.com")
        ])

    def test_multiple_nodes_complex(self):
        pass


class TestTextToTextnodes(unittest.TestCase):
    def test_text_to_textnodes(self):
        pass


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        pass


class TestBlockToBlockType(unittest.TestCase):
    def test_block_to_block_type(self):
        pass


if __name__ == "__main__":
    unittest.main()
