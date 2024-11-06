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

    def test_single_delimiter(self):
        node = TextNode("This doesnt have a *closing delimiter", "text")
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "*", "italic")


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
nodes_complex = [
    TextNode("This test contains images of ![birds](https://i.imgur.com/fJRm4Vk.jpeg) and the ![bees](https://i.imgur.com/fJRm4Vk.png) and more text", text_type_text),
    TextNode("This is text without images or links", text_type_text),
    TextNode("This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)", text_type_text),
    TextNode("This test contains links to [google](https://www.google.com) and [bing](https://www.bing.com)", text_type_text)
]


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

    def test_image_without_alt(self):
        node = [TextNode("Image without alt text ![](/static/images/withoutalt.jpeg)", text_type_text)]
        self.assertEqual(split_nodes_image(node), [
            TextNode("Image without alt text ", text_type_text),
            TextNode("", text_type_image, "/static/images/withoutalt.jpeg")
        ])

    def test_multiple_image_nodes_simple(self):
        self.assertEqual(split_nodes_image(nodes_simple), [
            TextNode("This is text without images or links", text_type_text),
            TextNode("This is ", text_type_text),
            TextNode("some image", text_type_image, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode("This is [some link](https://www.link.com)", text_type_text)
        ])

    def test_multiple_image_nodes_complex(self):
        self.assertEqual(split_nodes_image(nodes_complex), [
            TextNode("This test contains images of ", text_type_text),
            TextNode("birds", text_type_image, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and the ", text_type_text),
            TextNode("bees", text_type_image, "https://i.imgur.com/fJRm4Vk.png"),
            TextNode(" and more text", text_type_text),
            TextNode("This is text without images or links", text_type_text),
            TextNode("This is **text** with an *italic* word and a `code block` and an ", text_type_text),
            TextNode("obi wan image", text_type_image, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a [link](https://boot.dev)", text_type_text),
            TextNode("This test contains links to [google](https://www.google.com) and [bing](https://www.bing.com)", text_type_text)
        ])

    def test_image_invalid_syntax(self):
        nodes = [
            TextNode("This is ![some image](https://i.imgur.com/fJRm4Vk.jpeg", text_type_text),
            TextNode("Missing url ![alt text]", text_type_text),
            TextNode("Missing exclamation mark [some image](https://i.imgur.com/fJRm4Vk.jpeg)", text_type_text)
        ]
        self.assertEqual(split_nodes_image(nodes), [
            TextNode("This is ![some image](https://i.imgur.com/fJRm4Vk.jpeg", text_type_text),
            TextNode("Missing url ![alt text]", text_type_text),
            TextNode("Missing exclamation mark [some image](https://i.imgur.com/fJRm4Vk.jpeg)", text_type_text)
        ])

    def test_image_special_chars(self):
        node = [TextNode("This is ![some || image](https://i.imgur.com/fJRm&&4Vk.jpeg)", text_type_text)]
        self.assertEqual(split_nodes_image(node), [
            TextNode("This is ", text_type_text),
            TextNode("some || image", text_type_image, "https://i.imgur.com/fJRm&&4Vk.jpeg")
        ])

    def test_image_preceding_link(self):
        node = [TextNode("This is ![some image](https://i.imgur.com/fJRm4Vk.jpeg)[link](https://www.link.com)", text_type_text)]
        self.assertEqual(split_nodes_image(node), [
            TextNode("This is ", text_type_text),
            TextNode("some image", text_type_image, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode("[link](https://www.link.com)", text_type_text)
        ])

    def test_image_nested_brackets(self):
        node = [TextNode("This is ![[some image]](https://i.imgur.com/fJRm4Vk.jpeg)", text_type_text)]
        self.assertEqual(split_nodes_image(node), [
            TextNode("This is ", text_type_text),
            TextNode("[some image]", text_type_image, "https://i.imgur.com/fJRm4Vk.jpeg")
        ])

    def test_image_parentheses_in_alt(self):
        node = [TextNode("This is ![(some image)](https://i.imgur.com/fJRm4Vk.jpeg)", text_type_text)]
        self.assertEqual(split_nodes_image(node), [
            TextNode("This is ", text_type_text),
            TextNode("(some image)", text_type_image, "https://i.imgur.com/fJRm4Vk.jpeg")
        ])

    def test_image_nested_parentheses(self):
        node = [TextNode("This is ![some image]((https://i.imgur.com/fJRm4Vk.jpeg))", text_type_text)]
        self.assertEqual(split_nodes_image(node), [
            TextNode("This is ", text_type_text),
            TextNode("some image", text_type_image, "(https://i.imgur.com/fJRm4Vk.jpeg)")
        ])

    def test_image_parentheses_in_url(self):
        node = [TextNode("This is ![some image](https://example.com/image(1).jpg)", text_type_text)]
        self.assertEqual(split_nodes_image(node), [
            TextNode("This is ", text_type_text),
            TextNode("some image", text_type_image, "https://example.com/image(1).jpg")
        ])

    def test_image_invalid_parentheses(self):
        node = [TextNode("This is ![some image](https://example.com/image((1).jpg)", text_type_text)]
        self.assertEqual(split_nodes_image(node), [
            TextNode("This is ![some image](https://example.com/image((1).jpg)", text_type_text)
        ])

    def test_image_within_code(self):
        node = [TextNode("`This is a nested ![image](https://i.imgur.com/fJRm4Vk.jpeg) within a code block`", text_type_text)]
        self.assertEqual(split_nodes_image(node), [TextNode("`This is a nested ![image](https://i.imgur.com/fJRm4Vk.jpeg) within a code block`", text_type_text)])

    def test_image_complex_parentheses(self):
        node = [TextNode("This is a ![test image](http://example.com/image.jpg) string with a ![link image](http://example.org/path/image.png) and a ![complex image](http://example.com/path/(nested)/image.gif) with more ![nested image](http://example.org/another/path/(test_image)?query=1) examples.", text_type_text)]
        self.assertEqual(split_nodes_image(node), [
            TextNode("This is a ", text_type_text),
            TextNode("test image", text_type_image, "http://example.com/image.jpg"),
            TextNode(" string with a ", text_type_text),
            TextNode("link image", text_type_image, "http://example.org/path/image.png"),
            TextNode(" and a ", text_type_text),
            TextNode("complex image", text_type_image, "http://example.com/path/(nested)/image.gif"),
            TextNode(" with more ", text_type_text),
            TextNode("nested image", text_type_image, "http://example.org/another/path/(test_image)?query=1"),
            TextNode(" examples.", text_type_text)
        ])


class TestSplitNodesLink(unittest.TestCase):
    def test_link_type_list(self):
        node = TextNode("This is [some link](https://www.link.com)", text_type_text)
        with self.assertRaises(TypeError):
            split_nodes_link(node)

    def test_link_empty_list(self):
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

    def test_link_without_alt(self):
        node = [TextNode("Link without alt text [](https://www.google.com)", text_type_text)]
        self.assertEqual(split_nodes_link(node), [
            TextNode("Link without alt text ", text_type_text),
            TextNode("", text_type_link, "https://www.google.com")
        ])

    def test_multiple_link_nodes_simple(self):
        self.assertEqual(split_nodes_link(nodes_simple), [
            TextNode("This is text without images or links", text_type_text),
            TextNode("This is ![some image](https://i.imgur.com/fJRm4Vk.jpeg)", text_type_text),
            TextNode("This is ", text_type_text),
            TextNode("some link", text_type_link, "https://www.link.com")
        ])

    def test_multiple_link_nodes_complex(self):
        self.assertEqual(split_nodes_link(nodes_complex), [
            TextNode("This test contains images of ![birds](https://i.imgur.com/fJRm4Vk.jpeg) and the ![bees](https://i.imgur.com/fJRm4Vk.png) and more text", text_type_text),
            TextNode("This is text without images or links", text_type_text),
            TextNode("This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a ", text_type_text),
            TextNode("link", text_type_link, "https://boot.dev"),
            TextNode("This test contains links to ", text_type_text),
            TextNode("google", text_type_link, "https://www.google.com"),
            TextNode(" and ", text_type_text),
            TextNode("bing", text_type_link, "https://www.bing.com")
        ])

    def test_link_invalid_syntax(self):
        nodes = [
            TextNode("This is [some link](https://i.imgur.com/", text_type_text),
            TextNode("Missing url [anchor text]", text_type_text),
            TextNode("Missing bracket some link(https://i.imgur.com/)", text_type_text)
        ]
        self.assertEqual(split_nodes_link(nodes), [
            TextNode("This is [some link](https://i.imgur.com/", text_type_text),
            TextNode("Missing url [anchor text]", text_type_text),
            TextNode("Missing bracket some link(https://i.imgur.com/)", text_type_text)
        ])

    def test_link_special_chars(self):
        node = [TextNode("This is [some || link](https://i.imgur.com/)", text_type_text)]
        self.assertEqual(split_nodes_link(node), [
            TextNode("This is ", text_type_text),
            TextNode("some || link", text_type_link, "https://i.imgur.com/")
        ])

    def test_link_preceding_image(self):
        node = [TextNode("This is [some link](https://i.imgur.com/)![some image](https://i.imgur.com/fJRm4Vk.jpeg)", text_type_text)]
        self.assertEqual(split_nodes_link(node), [
            TextNode("This is ", text_type_text),
            TextNode("some link", text_type_link, "https://i.imgur.com/"),
            TextNode("![some image](https://i.imgur.com/fJRm4Vk.jpeg)", text_type_text)
        ])

    def test_link_nested_brackets(self):
        node = [TextNode("This is [[some link]](https://i.imgur.com/)", text_type_text)]
        self.assertEqual(split_nodes_link(node), [
            TextNode("This is ", text_type_text),
            TextNode("[some link]", text_type_link, "https://i.imgur.com/")
        ])

    def test_link_parentheses_in_anchor(self):
        node = [TextNode("This is [(some link)](https://i.imgur.com/)", text_type_text)]
        self.assertEqual(split_nodes_link(node), [
            TextNode("This is ", text_type_text),
            TextNode("(some link)", text_type_link, "https://i.imgur.com/")
        ])

    def test_link_nested_parentheses(self):
        node = [TextNode("This is [some link]((https://i.imgur.com/))", text_type_text)]
        self.assertEqual(split_nodes_link(node), [
            TextNode("This is ", text_type_text),
            TextNode("some link", text_type_link, "(https://i.imgur.com/)")
        ])

    def test_link_parentheses_in_url(self):
        node = [TextNode("This is [some link](https://example.com/image(1))", text_type_text)]
        self.assertEqual(split_nodes_link(node), [
            TextNode("This is ", text_type_text),
            TextNode("some link", text_type_link, "https://example.com/image(1)")
        ])

    def test_link_invalid_parentheses(self):
        node = [TextNode("This is [some link](https://example.com/image((1)", text_type_text)]
        self.assertEqual(split_nodes_link(node), [
            TextNode("This is [some link](https://example.com/image((1)", text_type_text)
        ])

    def test_link_within_code(self):
        node = [TextNode("`This is a nested [link](https://i.imgur.com/) within a code block`", text_type_text)]
        self.assertEqual(split_nodes_link(node), [TextNode("`This is a nested [link](https://i.imgur.com/) within a code block`", text_type_text)])

    def test_link_complex_nested_parentheses(self):
        node = [TextNode("This is a [test](http://example.com) string with a [link](http://example.org/path?query=value#fragment) and a [complex link](http://example.com/path/(nested)/value) with more [nested](http://example.org/another/path/(test)?) examples.", text_type_text)]
        self.assertEqual(split_nodes_link(node), [
            TextNode("This is a ", text_type_text),
            TextNode("test", text_type_link, "http://example.com"),
            TextNode(" string with a ", text_type_text),
            TextNode("link", text_type_link, "http://example.org/path?query=value#fragment"),
            TextNode(" and a ", text_type_text),
            TextNode("complex link", text_type_link, "http://example.com/path/(nested)/value"),
            TextNode(" with more ", text_type_text),
            TextNode("nested", text_type_link, "http://example.org/another/path/(test)?"),
            TextNode(" examples.", text_type_text)
        ])


class TestTextToTextnodes(unittest.TestCase):
    def test_text_to_textnodes_no_text(self):
        text = ""
        self.assertEqual(text_to_textnodes(text), [])

    def test_text_to_textnodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        self.assertEqual(text_to_textnodes(text), [
            TextNode("This is ", text_type_text),
            TextNode("text", text_type_bold),
            TextNode(" with an ", text_type_text),
            TextNode("italic", text_type_italic),
            TextNode(" word and a ", text_type_text),
            TextNode("code block", text_type_code),
            TextNode(" and an ", text_type_text),
            TextNode("obi wan image", text_type_image, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", text_type_text),
            TextNode("link", text_type_link, "https://boot.dev")
        ])

    def test_text_to_textnodes_order(self):
        text = "This is *text* with a `code block` and a **bold word** and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        self.assertEqual(text_to_textnodes(text), [
            TextNode("This is ", text_type_text),
            TextNode("text", text_type_italic),
            TextNode(" with a ", text_type_text),
            TextNode("code block", text_type_code),
            TextNode(" and a ", text_type_text),
            TextNode("bold word", text_type_bold),
            TextNode(" and an ", text_type_text),
            TextNode("obi wan image", text_type_image, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", text_type_text),
            TextNode("link", text_type_link, "https://boot.dev")
        ])


markdown_document = "# This is a heading\n\nThis is a paragraph of text. It has some **bold** and *italic* words inside of it.\n\n* This is the first list item in a list block\n* This is a list item\n* This is another list item"

class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks_empty_string(self):
        markdown = ""
        self.assertEqual(markdown_to_blocks(markdown), [])

    def test_markdown_to_blocks(self):
        self.assertEqual(markdown_to_blocks(markdown_document), [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            "* This is the first list item in a list block\n* This is a list item\n* This is another list item"
        ])

    def test_markdown_to_blocks_no_block(self):
        markdown = "# This is a heading\n\n\n\nThis is a paragraph of text. It has some **bold** and *italic* words inside of it.\n\n\n\n"
        self.assertEqual(markdown_to_blocks(markdown), [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it."
        ])


class TestBlockToBlockType(unittest.TestCase):
    def test_block_to_block_type_p(self):
        block = "This is a paragraph of text. It has some **bold** and *italic* words inside of it."
        self.assertEqual(block_to_block_type(block), block_type_paragraph)

    def test_block_to_block_type_header(self):
        block = "# This is a heading"
        self.assertEqual(block_to_block_type(block), block_type_header)

    def test_block_to_block_type_code(self):
        block = "```This is an example of a code block\nWhich spans over multiple lines\nIt starts and ends with three backticks```"
        self.assertEqual(block_to_block_type(block), block_type_code)

    def test_block_to_block_type_quote(self):
        block = ">This is a quote\n>This is also a quote\n>Together it is considered a quote block"
        self.assertEqual(block_to_block_type(block), block_type_quote)

    def test_block_to_block_type_ul_asterisk(self):
        block = "* This is the first list item in a list block\n* This is a list item\n* This is another list item"
        self.assertEqual(block_to_block_type(block), block_type_unordered_list)

    def test_block_to_block_type_ul_dash(self):
        block = "- This is the first list item in a list block\n- This is a list item\n- This is another list item"
        self.assertEqual(block_to_block_type(block), block_type_unordered_list)

    def test_block_to_block_type_ul_mix(self):
        block = "* This is the first list item in a list block\n- This is a list item\n* This is another list item"
        self.assertEqual(block_to_block_type(block), block_type_unordered_list)

    def test_block_to_block_type_ol(self):
        block = "1. First item in an ordered list\n2. Second item in an ordered list\n3. Third item in an ordered list"
        self.assertEqual(block_to_block_type(block), block_type_ordered_list)


class TestMarkdownToHTMLNode(unittest.TestCase):
    def test_no_markdown(self):
        markdown = ""
        self.assertEqual(markdown_to_html_node(markdown), HTMLNode("div", None, []))

    def test_split_delim_error(self):
        markdown = "This is just a\nparagraph with * a couple of * asterisks *"
        with self.assertRaises(ValueError):
            markdown_to_html_node(markdown)
        
    def test_markdown_to_html_node(self):
        markdown = "# This is a heading\n\nThis is a paragraph of text. It has some **bold** and *italic* words inside of it.\n\n* This is the first list item in a list block\n* This is a list item\n* This is another list item"
        self.assertEqual(markdown_to_html_node(markdown), HTMLNode("div", None, [
            HTMLNode("h1", "This is a heading", [
                LeafNode(None, "This is a heading")
            ]),
            HTMLNode("p", "This is a paragraph of text. It has some **bold** and *italic* words inside of it.", [
                LeafNode(None, "This is a paragraph of text. It has some "),
                LeafNode("b", "bold"),
                LeafNode(None, " and "),
                LeafNode("i", "italic"),
                LeafNode(None, " words inside of it.")
            ]),
            HTMLNode("ul", None, [
                HTMLNode("li", "This is the first list item in a list block", [
                    LeafNode(None, "This is the first list item in a list block")
                ]), 
                HTMLNode("li", "This is a list item", [
                    LeafNode(None, "This is a list item")
                ]), 
                HTMLNode("li", "This is another list item", [
                    LeafNode(None, "This is another list item")
                ])
            ])
        ]))

    def test_more_generic_markdown(self):
        markdown = "### **This is a bold heading**\n\n*This is not a list\n*Because it gets treated as a paragraph\n\n1. This should also be a paragraph\n3. Because it has wrong numeration\n\n1. This however\n2. This is a *sorted* list\n3. Because it has the right syntax\n\n"
        self.assertEqual(markdown_to_html_node(markdown), HTMLNode("div", None, [
            HTMLNode("h3", "**This is a bold heading**", [
                LeafNode("b", "This is a bold heading")
            ]),
            HTMLNode("p", "*This is not a list\n*Because it gets treated as a paragraph", [
                LeafNode("i", "This is not a list\n"),
                LeafNode(None, "Because it gets treated as a paragraph")
            ]),
            HTMLNode("p", "1. This should also be a paragraph\n3. Because it has wrong numeration", [
                LeafNode(None, "1. This should also be a paragraph\n3. Because it has wrong numeration")
            ]),
            HTMLNode("ol", None, [
                HTMLNode("li", "This however", [
                    LeafNode(None, "This however")
                ]), 
                HTMLNode("li", "This is a *sorted* list", [
                    LeafNode(None, "This is a "),
                    LeafNode("i", "sorted"),
                    LeafNode(None, " list")
                ]), 
                HTMLNode("li", "Because it has the right syntax", [
                    LeafNode(None, "Because it has the right syntax")
                ])
            ])
        ]))

    def test_code_quote_blocks(self):
        markdown = ">This first block is a quote block\n>As written by the great Daniel\n\n```I cant be arsed to write code in this code block\nBut it is still a code block```"
        self.assertEqual(markdown_to_html_node(markdown), HTMLNode("div", None, [
            HTMLNode("blockquote", "This first block is a quote\nAs written by the great Daniel", [
                LeafNode(None, "This first block is a quote\nAs written by the great Daniel")
            ]),
            HTMLNode("pre", None, [
                HTMLNode("code", "I cant be arsed to write code in this code block\nBut it is still a code block", [
                    LeafNode(None, "I cant be arsed to write code in this code block\nBut it is still a code block")
                ])
            ])
        ]))


if __name__ == "__main__":
    unittest.main()
