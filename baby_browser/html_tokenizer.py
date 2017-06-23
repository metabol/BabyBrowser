import re
from baby_browser.html_objects import * 
#Tokens
t_OPENTAG = re.compile("<(\w+)>")
t_CLOSETAG = re.compile("</(\w+)>")
t_DATA = re.compile("[^<>]+")
t_WHITESPACE = re.compile("\s+")
#States
BEFORE_HTML = "before html"
BEFORE_HEAD = "before head"
IN_HEAD = "in head"
AFTER_HEAD = "after head"
IN_BODY = "in body"
AFTER_BODY = "after body"
AFTER_AFTER_BODY = "after after body"
#Special HTML Tags
BODY = "body"
HTML = "html"
HEAD = "head"
class Html_Tokenizer:
    def handle_opentag(self, tag, attrs):
       # print("Found start tag:", tag)
        tag = Tag(tag, attrs)
        tag.parse_state = self.current_state 
        self.dom.add_child(tag) 
    def handle_closetag(self, tag):
       # print("Found end tag:", tag)
        self.dom.close_child() 
    def handle_data(self, data):
        self.dom.add_content(data)
       # print("Found data:", data)
    def p_opentag(self, match):
        tag = match.group(1)
        if tag.lower()==HTML:
            self.current_state = BEFORE_HEAD
        elif tag.lower()==HEAD:
            self.current_state = IN_HEAD
        elif tag.lower()==BODY:
            self.current_state = IN_BODY
        return tag, None, len(tag)
    def p_closetag(self, match):
        tag = match.group(1)
        if tag.lower()==HTML:
            self.current_state = AFTER_AFTER_BODY
        elif tag.lower()==HEAD:
            self.current_state = AFTER_HEAD
        elif tag.lower()==BODY:
            self.current_state = AFTER_BODY
        return tag, None, len(tag)
    def tokenize(self, html):
        index = 0
        self.dom = DOM()
        self.current_state = BEFORE_HTML 
        while index<len(html):
            index = self.parse(html, index)
    def parse(self, html, index):
        add_to_index = 0
        opentag =  t_OPENTAG.match(html[index:])
        closetag =  t_CLOSETAG.match(html[index:])
        whitespace = t_WHITESPACE.match(html[index:])
        data = t_DATA.match(html[index:])
        if opentag:
            tag, attrs, tag_len = self.p_opentag(opentag)
            self.handle_opentag(tag, attrs)
            add_to_index = tag_len+2
        elif closetag:
            tag, attrs, tag_len = self.p_closetag(closetag)
            self.handle_closetag(tag)
            add_to_index = tag_len+2
        elif whitespace:
            add_to_index = len(whitespace.group(0))
        elif data:
            self.handle_data(data.group(0))
            add_to_index = len(data.group(0))
        else:
            add_to_index = 1
        return add_to_index+index
if __name__=="__main__":
    html_str = "<html>\n<head><title>Website Title</title></head>\n<body>\nHi\n</body>\n</html>"
    tokenizer = Html_Tokenizer()
    tokenizer.tokenize(html_str) 
    print(tokenizer.dom)
