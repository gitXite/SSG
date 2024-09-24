class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
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
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        props_html = self.props_to_html()
        
        if self.value is None:
            raise ValueError("all leaf nodes must have a value")
        elif self.tag is None:
            return self.value
        elif self.props is None:
                return f"<{self.tag}>{self.value}</{self.tag}>"
        return f"<{self.tag}{props_html}>{self.value}</{self.tag}>"
        