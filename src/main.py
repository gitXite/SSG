from textnode import TextNode
from htmlnode import HTMLNode

def main():

    textnode = TextNode("Text", "bold", "https://www.text.com")
    print(textnode)

    htmlnode = HTMLNode("p", "Hello world", None, None)
    print(htmlnode)

if __name__ == "__main__":
    main()
