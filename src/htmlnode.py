class HTMLNode():
    def __init__(self, tag: str = None, value: str = None, children: list = None, props: dict = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("this is not implemented yet")
    
    def props_to_html(self):
        if self.props is not None and self.props:
            result = ""
            for key, value in self.props.items():
                result += f" {key}='{value}'"
            return result
        return ""
    
    def __repr__(self):
        cls = self.__class__.__name__
        return f"{cls}({self.tag}, {self.value}, {self.children}, {self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag: str, value: str, props: dict = None):
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        props_html = self.props_to_html()

        if self.value is None or self.value == "":
            raise ValueError("all leaf nodes must have a value")
        elif self.tag is None or self.tag == "":
            return self.value
        
        if self.props is None or len(self.props) == 0:
                return f"<{self.tag}>{self.value}</{self.tag}>"
        return f"<{self.tag}{props_html}>{self.value}</{self.tag}>"
        
class ParentNode(HTMLNode):
    def __int__(self, tag: str, children: list, props: dict = None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        result = ""
        props_html = self.props_to_html()
        
        if self.tag is None or self.tag == "":
            raise ValueError("all parent nodes must have a tag")
        elif self.children is None or len(self.children) == 0:
            raise ValueError("missing child node")
        elif type(self.children) != list:
            raise Exception("child nodes must be contained in a list")
        
        for node in self.children:
            result += node.to_html()
        if self.props is None or len(self.props) == 0:
            return f"<{self.tag}>{result}</{self.tag}>"
        return f"<{self.tag}{props_html}>{result}</{self.tag}>"
    
