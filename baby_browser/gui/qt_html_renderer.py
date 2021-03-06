from PyQt5.QtWidgets import * 
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from baby_browser.tokenizer.css import *
from baby_browser.tokenizer.html_tokenizer import *
from baby_browser.utility.networking import *

class QT_HTML_Renderer:

    HEADERS = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']
    IMG = "img"
    HR = 'hr'

    def __init__(self):
        pass

    def render_dom(self, root, htmlWidget, layout):
        """Method that renders the given webpage based on the DOM object
        :param root: DOM object containing webpage elements 
        :param htmlWidget: Browser_Widget containing empty webpage 
        :param layout: QLayout object for the htmlWidget 
        :returns: None 
        """
        self.traverse_dom(root, htmlWidget, layout)

    def traverse_dom(self, root, htmlWidget, layout):
        """Method that traverses the given DOM object and calls render methods
        :param root: DOM object containing webpage elements 
        :param htmlWidget: Browser_Widget containing empty webpage 
        :param layout: QLayout object for the htmlWidget 
        :returns: None 
        """
        if root.parse_state==IN_BODY:
            self.render_in_body_content(root, layout)
        if isinstance(root, Tag):
            if root.tag.lower()=="title":
                title = root.content
                self.set_page_title(title, htmlWidget)
            if root.tag.lower()=="body":
                self.render_body(root, htmlWidget)
        #Process the Children
        for child in root.children:
            self.traverse_dom(child, htmlWidget, layout)

    def set_page_title(self, title, page):
        """Method that stores the title of the page
        :param title: str containing webpage Title 
        :param page: Browser_Widget object representing the webpage 
        :returns: None 
        """
        page.setWindowTitle(title)
        page.title = title

    def render_body(self, root, htmlWidget):
        """Method that renders the Body Element of the webpage
        :param root: DOM object containing webpage 
        :param htmlWidget: Browser_Widget object representing the webpage 
        :returns: None 
        """
        widget = htmlWidget.widget
        self.render_box_styles(root, widget)

    def render_in_body_content(self, element, layout):
        widget = self.render_tag(element)
        if widget:
            layout.addWidget(widget)

    def render_tag(self, element):
        widget = None
        if isinstance(element, Tag):
            tag = element.tag.lower()
            if tag in QT_HTML_Renderer.HEADERS:
                widget = None
            elif tag==QT_HTML_Renderer.IMG:
                widget = self.render_img(element)
            elif tag==QT_HTML_Renderer.HR:
                widget = self.render_hr(element)
            else:
                widget = QWidget()
        elif isinstance(element, Text):
            widget = self.render_text(element)
        if widget:
            self.render_box_styles(element, widget)
        return widget

    def render_hr(self, element):
        hr = QFrame()
        hr.setFrameStyle(QFrame.HLine)
        return hr

    def render_img(self, element):
        element.content = Network.get_image(element.attrs["src"])
        image = QImage()
        image.loadFromData(element.content)
        label = QLabel()
        label.setPixmap(QPixmap(image))
        return label 

    def render_box_styles(self, element, widget):
        css = element.css
        box_style = []

        background_color = element.get_css_property(p_BACKGROUND_COLOR)
        color = element.get_css_property(p_COLOR)
        
        box_style.append(self.setBackgroundColor(widget, background_color))
        box_style.append(self.setColor(widget, color))
        
        #Apply Styles
        widget.setStyleSheet("".join(box_style))

    def render_text(self, element):
        text = QLabel(element.content)
        text.setWordWrap(True)
        text.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum);

        font = QFont()

        weight = element.get_css_property(p_FONT_WEIGHT)
        size = element.get_css_property(p_FONT_SIZE)
        
        self.set_font_weight(font, weight)
        self.set_font_point_size(font, size)
        
        text.setFont(font)
        return text
    #CSS
    def setBackgroundColor(self, widget, color):
        return "background-color:"+color+";"

    def setColor(self, widget, color):
        return "color:"+color+";"

    def set_font_weight(self, font, weight):
        if weight==FONT_WEIGHT_BOLD:
            font.setBold(True)
        elif weight==FONT_WEIGHT_NORMAL:
            fold.setBold(False)

    def set_font_point_size(self, font, size):
        font.setPointSize(size.value)
