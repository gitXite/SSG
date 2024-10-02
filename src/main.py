from textnode import TextNode
from htmlnode import HTMLNode, LeafNode, ParentNode
from split_delimiter import split_nodes_delimiter

def main():

    # testing repr
    """leafnodes = [
        LeafNode("i", "italic text"), 
        LeafNode("b", "bold text"),
        LeafNode(None, "Raw text"),
        LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        ]
    parentnode = ParentNode("p", None, leafnodes) # this doesnt really need None for value argument, needs to be fixed
    print(parentnode.to_html())
    """

    # testing split with delimiter
    """node = TextNode("**This is text** with a delimiter at the start", "text")
    print(split_nodes_delimiter([node], "**", "bold"))
    
    old_nodes = [
	TextNode("This is text with a `code block` word", "text"),
	TextNode("This is just some raw text", "text"),
	TextNode("This is text with **bold** delimiters", "text")
    ]
    print(split_nodes_delimiter(old_nodes, "`", "code"))
    """

if __name__ == "__main__":
    main()
