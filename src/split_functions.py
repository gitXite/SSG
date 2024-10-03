from textnode import *
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
    toggle = itertools.cycle([text_type_text, text_type]).__next__ # used to toggle between "text" and text_type
    
    # function logic
    for node in old_nodes:
        if node.text_type == text_type_text and delimiter in node.text:
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
    
    # function logic
    for node in old_nodes:
        if node.text: # only process if node has text
            images_list = extract_markdown_images(node.text)
            if images_list: # only append if there are matches from function
                for tuple in images_list:
                    split_text = node.text.split(f"![{tuple[0]}]({tuple[1]})", 1) # split the text with the markdown image as delimiter
                    for text in split_text:
                        new_nodes.append(TextNode(text, text_type_text)) # append TextNode with "text" type
                    new_nodes.append(TextNode(tuple[0], text_type_image, tuple[1])) # append TextNode with "image" type
            else:
                new_nodes.append(node)
    return new_nodes

# function to split nodes with "text" text_type, into different TextNodes with link text_type
def split_nodes_link(old_nodes):
    # error catches
    if type(old_nodes) != list:
        raise TypeError("nodes must be contained in a list")
    if not old_nodes:
        return []

    new_nodes = []

    # function logic
    for node in old_nodes:
        if node.text: # only process if node has text
            links_list = extract_markdown_links(node.text)
            if links_list: # only append to list if there are matches from function
                for tuple in links_list:
                    split_text = node.text.split(f"[{tuple[0]}]({tuple[1]})", 1) # split the text with the markdown link as delimiter
                    for text in split_text:
                        new_nodes.append(TextNode(text, text_type_text)) # append TextNode with "text" type
                    new_nodes.append(TextNode(tuple[0], text_type_link, tuple[1])) # append TextNode with "link" type
            else:
                new_nodes.append(node)
    return new_nodes

# converts raw markdown to TextNodes using helper split functions
def text_to_textnodes(text: str):
    if not text:
        return []
    node = TextNode(text, text_type_text)
    result = []
    result.extend(split_nodes_delimiter([node], "`", text_type_code))
    result.extend(split_nodes_delimiter([node], "**", text_type_bold))
    result.extend(split_nodes_delimiter([node], "*", text_type_italic))
    #result.extend(split_nodes_image([node]))
    #result.extend(split_nodes_link([node]))
    return result