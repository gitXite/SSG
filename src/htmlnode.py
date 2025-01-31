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
    
    def __eq__(self, other):
        if (
            self.tag == other.tag
            and self.value == other.value
            and self.children == other.children
            and self.props == other.props
        ):
            return True
        return False
    
    def __repr__(self):
        cls = self.__class__.__name__
        return f"{cls}({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        # error catches
        if self.value is None:
            raise ValueError("all leaf nodes must have a value")
        if self.tag is None or self.tag == "":
            return self.value
            
        props_html = self.props_to_html()

        # function body
        if self.props is None or len(self.props) == 0:
                return f"<{self.tag}>{self.value}</{self.tag}>"
        return f"<{self.tag}{props_html}>{self.value}</{self.tag}>"
    
    def __eq__(self, other):
        if (
            self.tag == other.tag
            and self.value == other.value
            and self.props == other.props
        ):
            return True
        return False

    def __repr__(self):
        cls = self.__class__.__name__
        return f"{cls}({self.tag}, {self.value}, {self.props})"


class ParentNode(HTMLNode):
    def __int__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        # base case for recursion, error catches
        if self.tag is None or self.tag == "":
            raise ValueError("all parent nodes must have a tag")
        if self.children is None or len(self.children) == 0:
            raise ValueError("missing child node")
        if type(self.children) != list:
            raise TypeError("child nodes must be contained in a list")
    
        props_html = self.props_to_html()
        # recursive statement with list comprehension
        children_html = "".join(child.to_html() for child in self.children)

        # function body
        if self.props is None or len(self.props) == 0:
            return f"<{self.tag}>{children_html}</{self.tag}>"
        return f"<{self.tag}{props_html}>{children_html}</{self.tag}>"
    
    def __eq__(self, other):
        if (
            self.tag == other.tag
            and self.children == other.children
            and self.props == other.props
        ):
            return True
        return False

    def __repr__(self):
        cls = self.__class__.__name__
        return f"{cls}({self.tag}, {self.children}, {self.props})"
    
