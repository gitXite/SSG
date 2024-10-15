from htmlnode import LeafNode


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


text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_image = "image"
text_type_link = "link"

# conversion function using dictionary dispatch pattern
def text_node_to_html_node(text_node):
    if text_node.text_type not in type_to_node:
        raise Exception(f"invalid text type: {text_node.text_type}")
    return type_to_node[text_node.text_type](text_node)


# functions for creating LeafNode objects, to be used in dictionary dispatch pattern
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
