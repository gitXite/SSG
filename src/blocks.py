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
    header = None
    code = re.search(r"```(.*?)```", block)
    if code:
        return "this is a code block"
        
        
