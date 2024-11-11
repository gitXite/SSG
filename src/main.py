from textnode import *
from htmlnode import *
from markdown import *
import shutil


src = "SSG/static/"
dst = "SSG/public/"

def copy_static_to_public():
    pass


def main():
    markdown = "```I cant be arsed to write code in this code block```"
    print(markdown_to_html_node(markdown))


if __name__ == "__main__":
    main()
