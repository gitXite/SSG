from node_helpers import *
from split_functions import *
import re

text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_image = "image"
text_type_link = "link"

# converts raw markdown to TextNodes using helper split functions
def text_to_textnodes(text: str):
    if not text:
        return []
    node = TextNode(text, text_type_text)
    result = []


# conversion function using dictionary dispatch pattern from node_helpers.py
def text_node_to_html_node(text_node):
    if text_node.text_type not in type_to_node:
        raise Exception(f"invalid text type: {text_node.text_type}")
    return type_to_node[text_node.text_type](text_node)

# functions for extracting markdown text
def extract_markdown_images(text):
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    if matches is None:
        return []
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    if matches is None:
        return []
    return matches

class TextNode():
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        ):
            return True
        return False
    
    def __repr__(self):
        cls = self.__class__.__name__
        return f"{cls}({self.text}, {self.text_type}, {self.url})"
