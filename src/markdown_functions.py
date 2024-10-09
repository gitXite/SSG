import re
from htmlnode import *

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
        return f"This is a {block_type_header} block"
    code = re.search(r"^```.*```$", block) # checks if there are 3 backticks at the beginning and end of the block
    if code:
        return f"This is a {block_type_code} block"
    quote = re.search(r"^>", block, re.M) # checks if every line starts with ">"
    if quote:
        return f"This is a {block_type_quote} block"
    unordered_list = re.search(r"^\*|- ", block, re.M) # checks if every line either starts with "*" or "-" followed by a space
    if unordered_list:
        return f"This is an {block_type_unordered_list} block"
    ordered_list = re.search(r"^(\d+)\. ", block, re.M) # checks if every line starts with a digit followed by a "." and a space
    # checks if the digit starts at 1 and increments for every line
    if ordered_list:
        lines = block.split('\n')
        for i, line in enumerate(lines, 1):
            if not re.match(r"^" + str(i) + r"\. ", line):
                return f"This is a normal {block_type_paragraph} block"
        return f"This is an {block_type_ordered_list} block"
        
    return f"This is a normal {block_type_paragraph} block"

# converts full markdown documents to html nodes
def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
    
