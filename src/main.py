from textnode import *
from htmlnode import *
from markdown import *
import shutil


src = "SSG/static/"
dst = "SSG/public/"

def copy_static_to_public():
    pass


def main():
    markdown = "### This is a heading\n\n*This is not a list\n*Because it gets treated as a paragraph\n\n1. This should also be a paragraph\n3. Because it has wrong numeration\n\n1. This however\n2. This is a sorted list\n3. Because it has the right syntax\n\n"
    print(markdown_to_html_node(markdown))


if __name__ == "__main__":
    main()
