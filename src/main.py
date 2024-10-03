from textnode import *
from htmlnode import *
from split_functions import *


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

    """# testing extracting images from markdown
    text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
    print(extract_markdown_images(text))
    text2 = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
    print(extract_markdown_links(text2))
    """

    # testing split image
    node = TextNode("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)", "text")
    print(split_nodes_image([node]))

if __name__ == "__main__":
    main()
