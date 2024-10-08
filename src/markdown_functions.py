import re

# functions for extracting markdown text
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

def markdown_to_blocks(markdown):
    if not markdown:
        return []
        
    blocks = markdown.split("\n\n")
    for block in blocks:
        block.strip()
        if not block:
            blocks.remove(block)
    return blocks

def block_to_block_type(block):
    header = re.search(r"^#[1-6] ", block) # checks if there are 1-6 hashtags followed by a space at the beginning of the block
    if header:
        return "This is a header block"
    code = re.search(r"^```.*```$", block) # checks if there are 3 backticks at the beginning and end of the block
    if code:
        return "This is a code block"
    quote = re.search(r"^>", block, re.M) # checks if every line starts with ">"
    if quote:
        return "This is a quote block"
    unordered_list = re.search(r"^\*|- ", block, re.M) # checks if every line either starts with "*" or "-" followed by a space
    if unordered_list:
        return "This is an unordered list block"
    ordered_list = re.search(r"^(\d+)\. ", block, re.M) # checks if every line starts with a digit followed by a "." and a space
    # checks if the digit starts at 1 and increments for every line
    if ordered_list:
        lines = block.split('\n')
        for i, line in enumerate(lines, 1):
            if not re.match(r"^" + str(i) + r"\. ", line):
                return "This is a normal paragraph block"
        return "This is an ordered list block"
        
    return "This is a normal paragraph block"
