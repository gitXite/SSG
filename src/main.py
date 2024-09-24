from textnode import TextNode
from htmlnode import HTMLNode

def main():

    textnode = TextNode("Text", "bold", "https://www.text.com")
    print(textnode)

    htmlnode = HTMLNode("p", "Hello world", None, {"href": "https://www.none.com", "target": "test"})
    print(htmlnode)
    print(htmlnode.props_to_html())

if __name__ == "__main__":
    main()
