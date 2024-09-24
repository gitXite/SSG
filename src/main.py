from textnode import TextNode
from htmlnode import HTMLNode, LeafNode, ParentNode

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
