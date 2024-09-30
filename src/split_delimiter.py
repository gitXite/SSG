from textnode import TextNode

def split_nodes_delimiter(old_nodes: list, delimiter: str, text_type: str):
    # error catches
    if type(old_nodes) != list:
        raise TypeError("nodes must be contained in a list")
    if len(old_nodes) == 0:
        raise ValueError("not a node")
    
    new_nodes = []

    for node in old_nodes:
        if node.text_type == "text" and delimiter in node.text:
            split_text = node.text.split(delimiter)
            if not node.text.startswith(delimiter) and not node.text.endswith(delimiter):
                new_nodes.extend(TextNode(split_text[0], "text"), TextNode(split_text[1], text_type), TextNode(split_text[2], "text"))
            if node.text.startswith(delimiter):
                new_nodes.extend(TextNode(split_text[0], text_type), TextNode(split_text[1], "text"))
            if node.text.endswith(delimiter):
                new_nodes.extend(TextNode(split_text[0], "text"), TextNode(split_text[1], text_type))
            if node.text.startswith(delimiter) and node.text.endswith(delimiter):
                new_nodes.append(TextNode(node.text, text_type))
        else:
            new_nodes.append(node)
    return new_nodes
