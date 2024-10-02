from textnode import (
    TextNode, 
    extract_markdown_images,
    extract_markdown_links
)
import itertools

# function to split nodes with "text" text_type, into different TextNodes with the right text_type
def split_nodes_delimiter(old_nodes: list, delimiter: str, text_type: str):
    # error catches
    if type(old_nodes) != list:
        raise TypeError("nodes must be contained in a list")
    if delimiter == None or text_type == None:
        raise TypeError("delimiter and or text type cannot be None")
    if not old_nodes:
        return []
    
    new_nodes = []
    toggle = itertools.cycle(["text", text_type]).__next__ # used to toggle between "text" and text_type
    
    # function logic
    for node in old_nodes:
        if node.text_type == "text" and delimiter in node.text:
            split_text = node.text.split(delimiter)
            current_type = toggle() if split_text[0] else text_type # get the first type depending on delimiter position
            for text in split_text:
                if text: # doesnt append if the node is an empty string
                    new_nodes.append(TextNode(text, current_type))
                    current_type = toggle() # toggle the next type and sets the new current_type
        else:
            new_nodes.append(node)
    return new_nodes

# function to split nodes with "text" text_type, into different TextNodes with image text_type
def split_nodes_image(old_nodes):
    # error catches
    if type(old_nodes) != list:
        raise TypeError("nodes must be contained in a list")
    if not old_nodes:
        return []

    new_nodes = []
    toggle = itertools.cycle(["text", "image"]).__next__ # used to toggle between "text" and "image" type

    for node in old_nodes:
        if node.text_type == "text":
            images_list = extract_markdown_images(node.text)

# function to split nodes with "text" text_type, into different TextNodes with link text_type
def split_nodes_link(old_nodes):
    # error catches
    if type(old_nodes) != list:
        raise TypeError("nodes must be contained in a list")
    if not old_nodes:
        return []

    new_nodes = []
    toggle = itertools.cycle(["text", "link"]).__next__ # used to toggle between "text" and "link" type
    
    for node in old_nodes:
        if node.text_type == "text":
            pass
