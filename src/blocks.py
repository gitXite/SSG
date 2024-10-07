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
    header = re.search(r"^#[1-6] ", block)
    if header:
        return "This is a header block"
    code = re.search(r"^```.*```$", block)
    if code:
        return "This is a code block"
    quote = re.search(r"^>", block, re.M)
    if quote:
        return "This is a quote block"
    unordered_list = re.search(r"^\*|\- ", block, re.M)
    if unordered_list:
        return "This is an unordered list block"
    ordered_list = re.search(r"^\d\. ", block, re.M) # needs to check increments for every line
    if ordered_list:
        return "This is an ordered list block"
    return "This is a normal paragraph block"
