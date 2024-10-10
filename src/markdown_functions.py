import re
from htmlnode import *
from textnode import *

# block_types
block_type_paragraph = "paragraph"
block_type_header = "header"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered_list = "unordered list"
block_type_ordered_list = "ordered list"

# functions for extracting markdown images/links from text
def extract_markdown_images(text):
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    if matches is None:
        return []
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    if matches is None:
        return []
    return matches

# converts markdown documents to blocks
def markdown_to_blocks(markdown):
    if not markdown:
        return []
        
    blocks = markdown.split("\n\n")
    for block in blocks:
        block.strip()
        if not block:
            blocks.remove(block)
    return blocks

# checks the type of block
def block_to_block_type(block):
    header = re.search(r"^#[1-6] ", block) # checks if there are 1-6 hashtags followed by a space at the beginning of the block
    if header:
        return block_type_header
    code = re.search(r"^```.*```$", block) # checks if there are 3 backticks at the beginning and end of the block
    if code:
        return block_type_code
    quote = re.search(r"^>", block, re.M) # checks if every line starts with ">"
    if quote:
        return block_type_quote
    unordered_list = re.search(r"^\*|- ", block, re.M) # checks if every line either starts with "*" or "-" followed by a space
    if unordered_list:
        returnblock_type_unordered_list
    ordered_list = re.search(r"^(\d+)\. ", block, re.M) # checks if every line starts with a digit followed by a "." and a space
    # checks if the digit starts at 1 and increments for every line
    if ordered_list:
        lines = block.split('\n')
        for i, line in enumerate(lines, start=1):
            if not re.match(r"^" + str(i) + r"\. ", line):
                return block_type_paragraph
        return block_type_ordered_list
        
    return block_type_paragraph

# converts full markdown documents to html nodes
def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    block_nodes = []
    for block in blocks:
        block_nodes.append(create_html_nodes(block))
    for node in block_nodes:
        if node.tag == "pre" and node.children and node.children[0].tag == "code":
            code_node = node.children[0]
            code_node.children = text_to_children(code_node.value)
        else:
            node.children = text_to_children(node.value)
    parent_node = HTMLNode("div", None, block_nodes)
    return parent_node

# helper function to create child nodes based on text in block node
def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    child_nodes = []
    for node in text_nodes:
        child_nodes.append(text_node_to_html_node(node))
    return child_nodes

# helper function to create html node based on the block_type
def create_html_nodes(block):
    block_type = block_to_block_type(block)
    if block_type_paragraph in block_type:
        p_node = HTMLNode("p", block, None, None)
        return p_node
    elif block_type_header in block_type:
        h_node = HTMLNode("header", block, None, None)
        return h_node
    elif block_type_code in block_type:
        code_node = HTMLNode("code", block, None, None)
        pre_node = HTMLNode("pre", None, [code_node], None)
        return pre_node
    elif block_type_quote in block_type:
        q_node = HTMLNode("blockquote", block, None, None)
        return q_node
    elif block_type_unordered_list in block_type:
        ul_node = HTMLNode("ul", block, None, None)
        return ul_node
    elif block_type_ordered_list in block_type:
        ol_node = HTMLNode("ol", block, None, None)
        return ol_node
    else:
        raise Exception("no corresponding block")
