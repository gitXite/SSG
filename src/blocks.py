import re

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
    ordered_list = re.search(r"^\d\. ", block, re.M) # needs to check increments for every line
    if ordered_list:
        return "This is an ordered list block"
    return "This is a normal paragraph block"
