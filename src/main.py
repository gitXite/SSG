from textnode import TextNode
from htmlnode import HTMLNode, LeafNode, ParentNode
from node_helpers import *

# conversion function using dictionary dispatch pattern
def text_node_to_html_node(text_node):
    if text_node.text_type not in type_to_node:
        raise Exception(f"invalid text type: {text_node.text_type}")
    return type_to_node[text_node.text_type](text_node)

def main():

    leafnodes = [
        LeafNode("i", "italic text"), 
        LeafNode("b", "bold text"),
        LeafNode(None, "Raw text"),
        LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        ]
    parentnode = ParentNode("p", None, leafnodes) # this doesnt really need None for value argument, needs to be fixed
    print(parentnode.to_html())

if __name__ == "__main__":
    main()
