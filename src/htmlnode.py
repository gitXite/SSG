class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("this is not implemented yet")
    
    def props_to_html(self):
        for key, value in self.props.items():
            return f" {key}='{value}' {next(key)}='{next(value)}'"
        
    def __repr__(self):
        cls = self.__class__.__name__
        return f"{cls}({self.tag}, {self.value}, {self.children}, {self.props})"
    