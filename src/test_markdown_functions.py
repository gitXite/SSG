import unittest
from markdown_functions import *

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

class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        pass

class TestBlockToBlockType(unittest.TestCase):
    def test_block_to_block_type(self):
        pass
