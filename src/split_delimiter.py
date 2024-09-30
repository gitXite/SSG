from textnode import TextNode

def split_nodes_delimiter(old_nodes: list, delimiter: str, text_type: str):
    # error catches
    if type(old_nodes) != list:
        raise TypeError("nodes must be contained in a list")
    if len(old_nodes) == 0:
        raise ValueError("not a node")
    
    new_nodes = []

    for node in old_nodes:
        if text_type == "text" and delimiter in node.text:
            new_nodes.append(node.text.split(delimiter)) # probably wrong
    print(new_nodes)