from htmlnode import LeafNode

# functions to be used in dictionary dispatch pattern
def create_text_node(text_node):
    return LeafNode(None, text_node.text)
    
def create_bold_node(text_node):
    return LeafNode("b", text_node.text)
    
def create_italic_node(text_node):
    return LeafNode("i", text_node.text)

def create_code_node(text_node):
    return LeafNode("code", text_node.text)

def create_link_node(text_node):
    return LeafNode("a", text_node.text, {"href": text_node.url})

def create_img_node(text_node):
    return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})

# dictionary dispatch pattern, used in main to convert textnode object to leafnode
type_to_node = {
    "text": create_text_node,
    "bold": create_bold_node,
    "italic": create_italic_node,
    "code": create_code_node,
    "link": create_link_node,
    "img": create_img_node,
}

# helper functions for markdown_to_html_node() function
