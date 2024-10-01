from textnode import TextNode
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

    for node in old_nodes:
        if node.text_type == "text" and delimiter in node.text:
            split_text = node.text.split(delimiter)
            current_type = toggle() if split_text[0] else text_type # get the first type depending on delimiter position
            for text in split_text:
                new_nodes.append(TextNode(text, current_type))
                current_type = toggle() # toggle the next type and sets the new current_type
        else:
            new_nodes.append(node)
    return new_nodes
