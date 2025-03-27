'''from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit,QStackedWidget, QWidget, QLineEdit,QGridLayout, QVBoxLayout, QHBoxLayout, QPushButton, QFrame, QLabel, QSizePolicy
from PyQt5.QtGui import QIcon, QPainter, QMovie, QColor, QTextCharFormat, QFont, QPixmap, QTextBlockFormat

from PyQt5.QtCore import Qt, QSize, QTimer
from dotenv import dotenv_values

import sys
import os

env_vars = dotenv_values(".env")
Assistantnane = env_vars.get("Assistantname")
current_dir = os.getcwd()
old_chat_messages=""

TempDirPath = rf"{current_dir}\Frontend\Files"
GraphicsDirPath = rf"{current_dir}\Frontend\Graphics"

def AnswerModifier (Answer):
    lines=Answer.split('\n')
    non_empty_lines = [line for line in lines if line.strip()]
    modified_answer = '\n'.join(non_empty_lines)
    return modified_answer


def QueryModifier(Query):
    new_query = Query.lower().strip()
    query_words= new_query.split()
    question_words =["how","what","who","where","when","why","which","whose","whom","can you","what is","where's","how's"]
    if any(word+" " in new_query for word in question_words):
        if query_words[-1][-1] in ['.','?','!']:
            new_query=new_query[:-1] +"?"
        else:
            new_query+="?"
    
    else:
        if query_words[-1][-1] in ['.','?','!']:
             new_query=new_query[:-1] +"."
        else:
            new_query+="."

    return new_query.capitalize()




def SetMicrophoneStatus(Command) :
    with open(rf' {TempDirPath} \Mic.data', "w", encoding='utf-8') as file:
     file.write(Command)
    


def GetMicrophoneStatus() :
    with open(rf' {TempDirPath} \Mic.data', "r", encoding='utf-8') as file:
         
         Status=file.read()
    return Status


def SetAssistantStatus(Status):
    with open(rf' {TempDirPath}\Status data', "w", encoding='utf-8') as file:
        file.write(Status)
  


def GetAssistantStatus():
    with open(rf' {TempDirPath}\Status data', "r", encoding='utf-8') as file:
        Status = file.read()
    return Status

def MicButtonInitialed():
    SetMicrophoneStatus("False" )


def MicButtonClosed():
    SetMicrophoneStatus("True")


def GraphicsDirectoryPath (Filename):
    Path = rf' {GraphicsDirPath}\{Filename}'
    return Path


def TempDirectoryPath(Filename):
    Path = rf' {TempDirPath}\{Filename}'
    return Path


def ShowTextToScreen (Text):
    with open(rf' (TempDirPath) (Responses data', "w", encoding='utf-8') as file:
        file.write(Text)



class ChatSection(QWidget):
    def __init__(self):
        super (ChatSection, self).__init__()
        layout = QVBoxLayout(self)
        layout. setContentsMargins(-10, 40, 40, 100)
        layout. setSpacing(-100)
        self.chat_text_edit = QTextEdit()
        self.chat_text_edit.setReadOnly(True)
        self.chat_text_edit.setTextInteractionFlags(Qt.NoTextInteraction)
        self.chat_text_edit.setFrameStyle(QFrame.NoFrame)
        layout.addWidget(self.chat_text_edit)
        self.setStyleSheet ("background-color: black;")
        layout. setSizeConstraint(QVBoxLayout.SetDefaultConstraint)
        layout. setStretch(1, 1)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,QSizePolicy. Expanding))
        text_color = QColor(Qt.blue)
        text_color_text = QTextCharFormat()
        text_color_text. setForeground(text_color)
        self.chat_text_edit.setCurrentCharFormat(text_color_text)
        self.gif_label = QLabel()
        max_gif_size_W = 480
        max_gif_size_H = 270
        movie.setScaledSize(QSize(max_gif_size_w, max_gif_size_H))
        self.gif_lable.setAlignment(Qt.AlignRight|Qt.AlignBottom)
        self.gif_lable.setMovie(movie)
        movie.start()
        layout.addWidget(self.gif_label)
        self.lable=QLabel("")
        self.lable.setStyleSheet("color:white; font-size:16px; margin-right: 195px; border:none; margin-top: -30px")
        self.lable.setAlignment(Qt.AlignRight)
        layout.addWidget(self.lable)
        layout.setSpacing(-10)
        layout.addWidget(self.gif_lable)
        font=QFont()
        font.setPointSize(13)
        self.chat_text_edit.setFont(font)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.loadMessages)
        self.timer.timeout.connect(self.SpeechRecogText)
        self.timer.start(5)
        self. chat_text_edit.viewport().installEventFilter(self)
        self.setStyleSheet("""
                QScrollBar:vertical {
                border: none;
                background: black;
                width: 10px;
                margin: 0px 0px 0px 0px;
                }
                
                QScrollBar::handle:vertical{
                    background: white;
                    min-height:20px;
                }

                QScrollBar::add-line:vertical {
                    background:black;
                    subcontril-origin:margin;
                    height:10px;
                }

                QScrollBar::sub-line:vertical{
                    background:black;
                    subcontrol-position:top;
                    subcontrol-origin:margin;
                    height:10px;
                }

                QScrollBar::up-arrow:vertical,QScrollBar::down-arrow:vertical{
                    border:none;
                    background:none;
                    color:none;
                }

                QScrollBar::add-page:vertical,QScrollBar::sub-page:vertical{
                    background: none;
                }
                """)
        def loadMessages(self):
            global old_chat_messages
            with open(TempDirectoryPath('Responses data'), "r", encoding='utf-8') as file:
                messages = file.read()
                if None==messages:
                        pass
                elif len(messages) <= 1:
                        pass
                elif str(old_chat_message)==str(messages) :
                        pass
                else:
                self.addMessage(message=messages, color= 'White')
                old_chat_message = messages

    def SpeechRecogText(self):
        with open(TempDirectoryPath( 'Status.data'), "r", encoding='utf-8') as file:
            messages = file.read()
            self.label.setText(messages)

    def load_icon(self, path, width=60, height=60):
                pixmap = QPixmap(path)
                new_pixmap = pixmap.scaled(width, height)
                self.icon_label.setPixmap(new_pixmap)

    def toggle_icon(self, event=None):
        if self.toggled:
            self.load_icon(GraphicsDirectoryPath('voice.png'), 60, 60)
            MicButtonInitialed()
        else:
            self. load_icon(GraphicsDirectoryPath('mic.png'), 60, 60)
            MicButtonClosed()
            self.toggled = not self.toggled

    def addMessage(self, message, color):
            cursor = self.chat_text_edit.textCursor ()
            format = QTextCharFormat()
            formatm = QTextBlockFormat()
            formatm.setTopMargin(10)
            formatm.setLeftMargin(10)
            format.setForeground(QColor(color))
            cursor.setCharFormat (format)
            cursor.setBlockFormat(formatm)
            cursor.insertText(message + "\n")
            self.chat_text_edit.setTextCursor(cursor)


class InitialScreen (Widget):
        def __init__(self, parent=None):
            super().__init__(parent)
            desktop = QApplication.desktop()
            screen_width = desktop. screenGeometry().width()
            screen_height = desktop.screenGeometry().height()
            content_layout = QVBoxLayout()
            content_layout.setContentsMargins(0, 0, 0, 0)
            gif_label = QLabel()
            movie = QMovie(GraphicsDirectoryPath('Jarvis-gif'))
            gif_label.setMovie(movie)
            max_gif_size_H = int(screen_width / 16 * 9)
            movie.setScaledSize(QSize(screen_width, max_gif_size_H))
            gif_label.setAlignment(Qt.AlignCenter)
            movie.start()
            gif_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.icon_label = QLabel()
            pixmap = QPixmap(GraphicsDirectoryPath('Mic_on.png'))
            new_pixmap = pixmap.scaled(60, 60)
            self.icon_label.setPixmap(new_pixmap)
            self.icon_label.setFixedSize(150,150)
            self.icon_label.setAlignment(Qt.AlignCenter)
            self.toggled = True
            self.toggle_icon()
            self.icon_label.mousePressEvent = self.toggle_icon
            self.label - QLabel("")
            self.label.setStyleSheet("color: white; font-size:16px ; margin-bottom:0;") 
            content_layout.addWidget(gif_label, alignment=Qt.AlignCenter)
            content_layout.addwidget(self.label, alignment=Qt.AlignCenter)
            content_layout.addwidget(self.icon_label, alignment=Qt.AlignCenter)
            content_layout.setContentsMargins(0, 0, 0, 150)
            self.setLayout(content_layout) 
            self.setFixedHeight(screen_height)
            self.setFixedWidth(screen _width)
            self.setStyleSheet ("background-color: black;")
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.SpeechRecogText)
            self.timer.start(5)

        def SpeechRecogText(self):
                with open (TempDirectoryPath('Status data'), "r", encoding='utf-8') as file:
                     messages = file.read()
                     self.label.setText(messages)

        def load_icon(self,path,width=60,height=60):
             pixmap=QPixmap(path)
             new_pixmap=pixmap.scaled(width,height)
             self.icon_label.setPixmap(new_pixmap)

        def toggle_icon(self, event-None):
            if self.toggled:
                self.load_icon(GraphicsDirectoryPath('Mic_on.png'), 60, 60)
                MicButtonInitialed()

            else:
                self.load_icon(GraphicsDirectoryPath('Mic_off.png'), 60, 60)
                MicButtonClosed()
            self.toggled = not self.toggled
                 

             
                     
             
             
class MessageScreen (QWidget):
      def __init__(self, parent=None):
           super().__init__(parent)
           desktop = QApplication.desktop()
           screen_width=desktop.screenGeometry().width()
           screen_height=desktop.screenGeometry().height()
           layout=QVBoxLayout()
           label = QLabel("")
           layout.addWidget(label)
           chat_section=ChatSection()
           layout.addWidget(chat_section)
           self.setLayout(layout)
           self.setStyleSheet("background-color: black;")
           self.setFixedHeight(screen_height)
           self.setFixedWidth(screen_width)
           

class CustomTopBar(QWidget):
    def __init__(self, parent, stacked_widget):
         super().__init__(parent)
         self.initUI()
         self.current_screen = None
         self.stacked_widget = stacked_widget

    def initUl(self):
        self.setFixedHeight(50)
        layout=QHBoxLayout(self)
        layout.setAlignment (Qt.AlignRight)
        home_button = QPushButton()
        home_icon = QIcon(GraphicsDirectoryPath("Home.png" ))
        home_button.setIcon(home_icon)
        home_button.setText("  Home")
        home_button.setStyleSheet("height:40px; line-height:40px ; background-color:white ; color: black" )
        message_button = QPushButton()
        message_icon = QIcon(GraphicsDirectoryPath("Chats.png"))
        message_button.setIcon(message_icon)
        message_button.setText(" Chat")
        message_button.setStyleSheet("height:40px; line-height:40px; background-color:white ; color: black")
        minimize_button = QPushButton()
        minimize_icon = QIcon(GraphicsDirectoryPath('Minimize2.png'))
        minimize_button.setIcon(minimize_icon)
        minimize_button.setStyleSheet("background-color:white") minimize_button.clicked.connect(self.minimizeWindow)
        self.maximize_button = QPushButton( )
        self.maximize_icon = QIcon(GraphicsDirectoryPath( 'Maximize.png' ))
        self.restore_icon = QIcon(GraphicsDirectoryPath('Minimize.png' ))
        self.maximize_button.setIcon(self.maximize_icon)
        self.maximize_button.setFlat(True)
        self.maximize_button.setStyleSheet ("background-color:white")
        self.maximize_button.clicked.connect(self.maximizeWindow)
        close_button = QPushButton()
        close_icon = QIcon (GraphicsDirectoryPath('Close.png' ))
        close_button.setIcon(close_icon)
        close_button.setStyleSheet("background-color:white") 
        close_button.clicked.connect(self.closeWindow)
        line_frame = QFrame()
        line_frame.setFixedHeight (1)
        line_frame.setFrameShape(QFrame. HLine)
        line_frame.setFrameShadow(QFrame. Sunken)
        line_frame.setStyleSheet ("border-color: black;")
        title_label = QLabel(f" {str(Assistantname).capitalize()} AI ")
        title_label.setStyleSheet("color: black; font-size: 18px;background-color:white")
        home_button.clicked.connect(lambda:self.stacked_widget.setCurrent Index(0)) 
        message_button.clicked.connect(lambda: self.stacked_widget.setCurrent Index(1))
        layout.addwidget(title_label)
        layout.addStretch(1)
        layout.addWidget(home_button)
        layout.addWidget(message_button)
        layout.addStretch(1)
        layout.addWidget(minimize_button)
        layout.addWidget(self.maximize_button)
        layout.addWidget(close_button)
        layout.addWidget(line_frame)
        self.draggable = True
        self.offset = None

    def paintEvent(self, event):
         painter=QPainter(self)
         painter.fillRect(self.rect(),Qt.white)
         super().paintEvent (event)

    def minimizeWindow(self):
         self.parent().showMinimized()


    def maximizeWindow(self):
         if self.parent().isMaximized():
            self.parent().showNormal()
            self.maximize_button.setIcon(self.maximize_icon)
        else:
            self.parent().showMaximized()
            self maximize_button.setIcon(self.restore_icon)   
    
    def closeWindow(self):
            self-parent().close()


    def mousePressEvent (self, event):
            if self.draggable:
                self.offset =event.pos()

         
    def mouseMoveEvent(self, event):
         if self.draggable and self.offset:
              new_pos=event.globalPos()-self.offset
              self.parent().move(new_pos)

    def showMessageScreen(self):
         if self.current_screen is not None:
              self.current_screen.hide()

        message_screen=MessageScreen(self)
        layout=self.parent().layout()
        if layout is not None:
            layout.addWidget(message_screen)
        self.current_screen=message_screen
    
    def showInitialScreen(self):
         if self.current_screen is not None:
              self.current_screen.hide()

        initial_screen=InitialScreen(self)
        layout=self.parent().layout()
    if layout is not None:
         layout.addWidget(initial_screen)
         self.current_screen=initial_screen


class MainWindow(QMainWindow):
     def__init__(self):
          super().__init__()
          self.setWindowFlags(Qt.FramelessWindowHint)
          self.initUI()
     
     def initUI(self):
          desktop=QApplication.desktop()
          screen_width=desktop.screenGeometry().width()
          screen_height=desktop.screenGeometry().height()
          stacked_widget=QStackedWidget(self)
          initial_screen=InitialScreen()
          message_screen=MessageScreen()
          stacked_widget.addWidget(initial_screen)
          stacked_widget.addWidget(message_screen)
          self.setGeometry(0,0,screen_width,screen_height)
          self.setStyleSheet("background-color:black;")
          top_bar=CustomTopBar(self,stacked_widget)
          self.setMenuWidget(top_bar)
          self.setCentralWidget(stacked_widget)

    def GraphicalUserInterface():
        app=QApplication(sys.argv)
        window=MainWindow()
        window.show()
        sys.exit(app.exec_())


    if __name__=="__main__":
         GraphicalUserInterface()'''


from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QStackedWidget, QWidget, QLineEdit, QGridLayout, QVBoxLayout, QHBoxLayout, QPushButton, QFrame, QLabel, QSizePolicy
from PyQt5.QtGui import QIcon, QPainter, QMovie, QColor, QTextCharFormat, QFont, QPixmap, QTextBlockFormat
from PyQt5.QtCore import Qt, QSize, QTimer
from dotenv import dotenv_values
import sys
import os

# Load environment variables
env_vars = dotenv_values(".env")
Assistantname = env_vars.get("Assistantname", "Assistant")  # Default name if not found
current_dir = os.getcwd()
old_chat_messages = ""

# Define directory paths using os.path.join for cross-platform compatibility
TempDirPath = os.path.join(current_dir, "Frontend", "Files")
GraphicsDirPath = os.path.join(current_dir, "Frontend", "Graphics")

# Create directories if they don't exist
os.makedirs(TempDirPath, exist_ok=True)
os.makedirs(GraphicsDirPath, exist_ok=True)

# Create default files if they don't exist
default_files = ['Mic.data', 'Status data', 'Responses data']
for file in default_files:
    filepath = os.path.join(TempDirPath, file)
    if not os.path.exists(filepath):
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write('')  # Create empty file

def AnswerModifier(Answer):
    lines = Answer.split('\n')
    non_empty_lines = [line for line in lines if line.strip()]
    return '\n'.join(non_empty_lines)

def QueryModifier(Query):
    new_query = Query.lower().strip()
    query_words = new_query.split()
    question_words = ["how", "what", "who", "where", "when", "why", 
                     "which", "whose", "whom", "can you", "what is", 
                     "where's", "how's"]
    
    if any(word + " " in new_query for word in question_words):
        if query_words[-1][-1] in ['.', '?', '!']:
            new_query = new_query[:-1] + "?"
        else:
            new_query += "?"
    else:
        if query_words[-1][-1] in ['.', '?', '!']:
            new_query = new_query[:-1] + "."
        else:
            new_query += "."
    return new_query.capitalize()

def SetMicrophoneStatus(Command):
    with open(os.path.join(TempDirPath, 'Mic.data'), "w", encoding='utf-8') as file:
        file.write(Command)

def GetMicrophoneStatus():
    try:
        with open(os.path.join(TempDirPath, 'Mic.data'), "r", encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        return "False"

def SetAssistantStatus(Status):
    with open(os.path.join(TempDirPath, 'Status data'), "w", encoding='utf-8') as file:
        file.write(Status)

def GetAssistantStatus():
    try:
        with open(os.path.join(TempDirPath, 'Status data'), "r", encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        return ""

def MicButtonInitialed():
    SetMicrophoneStatus("False")

def MicButtonClosed():
    SetMicrophoneStatus("True")

def GraphicsDirectoryPath(Filename):
    return os.path.join(GraphicsDirPath, Filename)

def TempDirectoryPath(Filename):
    return os.path.join(TempDirPath, Filename)

def ShowTextToScreen(Text):
    with open(os.path.join(TempDirPath, 'Responses data'), "w", encoding='utf-8') as file:
        file.write(Text)

class ChatSection(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(-10, 40, 40, 100)
        layout.setSpacing(-100)
        
        self.chat_text_edit = QTextEdit()
        self.chat_text_edit.setReadOnly(True)
        self.chat_text_edit.setTextInteractionFlags(Qt.NoTextInteraction)
        self.chat_text_edit.setFrameStyle(QFrame.NoFrame)
        layout.addWidget(self.chat_text_edit)
        
        self.setStyleSheet("background-color: black;")
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # Text formatting
        text_color = QColor(Qt.blue)
        text_format = QTextCharFormat()
        text_format.setForeground(text_color)
        self.chat_text_edit.setCurrentCharFormat(text_format)
        
        # GIF Label
        self.gif_label = QLabel()
        gif_path = GraphicsDirectoryPath('Jarvis-gif.gif')  # Added .gif extension
        if os.path.exists(gif_path):
            self.movie = QMovie(gif_path)
            self.movie.setScaledSize(QSize(480, 270))
            self.gif_label.setMovie(self.movie)
            self.movie.start()
        else:
            self.gif_label.setText("Jarvis GIF")
            self.gif_label.setStyleSheet("color: white;")
        
        self.gif_label.setAlignment(Qt.AlignRight | Qt.AlignBottom)
        layout.addWidget(self.gif_label)
        
        # Status label
        self.label = QLabel("")
        self.label.setStyleSheet("color:white; font-size:16px; margin-right: 195px; border:none; margin-top: -30px")
        self.label.setAlignment(Qt.AlignRight)
        layout.addWidget(self.label)
        
        # Font settings
        font = QFont()
        font.setPointSize(13)
        self.chat_text_edit.setFont(font)
        
        # Timer for updates
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.loadMessages)
        self.timer.timeout.connect(self.SpeechRecogText)
        self.timer.start(5)
        
        # Scrollbar styling
        self.chat_text_edit.setStyleSheet("""
            QScrollBar:vertical {
                border: none;
                background: black;
                width: 10px;
                margin: 0px 0px 0px 0px;
            }
            QScrollBar::handle:vertical {
                background: white;
                min-height: 20px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                background: black;
                height: 10px;
            }
            QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
                border: none;
                background: none;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
        """)

    def loadMessages(self):
        global old_chat_messages
        try:
            with open(TempDirectoryPath('Responses data'), "r", encoding='utf-8') as file:
                messages = file.read()
                if messages and len(messages) > 1 and str(old_chat_messages) != str(messages):
                    self.addMessage(message=messages, color='White')
                    old_chat_messages = messages
        except FileNotFoundError:
            pass

    def SpeechRecogText(self):
        self.label.setText(GetAssistantStatus())

    def addMessage(self, message, color):
        cursor = self.chat_text_edit.textCursor()
        format = QTextCharFormat()
        format.setForeground(QColor(color))
        
        block_format = QTextBlockFormat()
        block_format.setTopMargin(10)
        block_format.setLeftMargin(10)
        
        cursor.setBlockFormat(block_format)
        cursor.setCharFormat(format)
        cursor.insertText(message + "\n")
        self.chat_text_edit.setTextCursor(cursor)
        self.chat_text_edit.ensureCursorVisible()

class InitialScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUI()

    def setupUI(self):
        desktop = QApplication.desktop()
        screen_width = desktop.screenGeometry().width()
        screen_height = desktop.screenGeometry().height()
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # GIF Label
        gif_label = QLabel()
        gif_path = GraphicsDirectoryPath('Jarvis-gif.gif')
        if os.path.exists(gif_path):
            self.movie = QMovie(gif_path)
            self.movie.setScaledSize(QSize(screen_width, int(screen_width / 16 * 9)))
            gif_label.setMovie(self.movie)
            self.movie.start()
        else:
            gif_label.setText("Jarvis Assistant")
            gif_label.setStyleSheet("color: white; font-size: 24px;")
        
        gif_label.setAlignment(Qt.AlignCenter)
        gif_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(gif_label, alignment=Qt.AlignCenter)
        
        # Status label
        self.label = QLabel("")
        self.label.setStyleSheet("color: white; font-size:16px; margin-bottom:0;")
        layout.addWidget(self.label, alignment=Qt.AlignCenter)
        
        # Mic button
        self.icon_label = QLabel()
        self.load_icon(GraphicsDirectoryPath('Mic_on.png'), 60, 60)
        self.icon_label.setFixedSize(150, 150)
        self.icon_label.setAlignment(Qt.AlignCenter)
        self.toggled = True
        self.icon_label.mousePressEvent = self.toggle_icon
        layout.addWidget(self.icon_label, alignment=Qt.AlignCenter)
        
        layout.setContentsMargins(0, 0, 0, 150)
        self.setFixedSize(screen_width, screen_height)
        self.setStyleSheet("background-color: black;")
        
        # Timer for updates
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.SpeechRecogText)
        self.timer.start(5)

    def SpeechRecogText(self):
        self.label.setText(GetAssistantStatus())

    def load_icon(self, path, width=60, height=60):
        try:
            pixmap = QPixmap(path)
            if pixmap.isNull():
                pixmap = QPixmap(width, height)
                pixmap.fill(Qt.gray)
            self.icon_label.setPixmap(pixmap.scaled(width, height))
        except:
            pixmap = QPixmap(width, height)
            pixmap.fill(Qt.gray)
            self.icon_label.setPixmap(pixmap)

    def toggle_icon(self, event=None):
        if self.toggled:
            self.load_icon(GraphicsDirectoryPath('Mic_on.png'), 60, 60)
            MicButtonInitialed()
        else:
            self.load_icon(GraphicsDirectoryPath('Mic_off.png'), 60, 60)
            MicButtonClosed()
        self.toggled = not self.toggled

class MessageScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUI()

    def setupUI(self):
        desktop = QApplication.desktop()
        screen_width = desktop.screenGeometry().width()
        screen_height = desktop.screenGeometry().height()
        
        layout = QVBoxLayout(self)
        chat_section = ChatSection()
        layout.addWidget(chat_section)
        
        self.setFixedSize(screen_width, screen_height)
        self.setStyleSheet("background-color: black;")

class CustomTopBar(QWidget):
    def __init__(self, parent, stacked_widget):
        super().__init__(parent)
        self.stacked_widget = stacked_widget
        self.setupUI()

    def setupUI(self):
        self.setFixedHeight(50)
        layout = QHBoxLayout(self)
        layout.setAlignment(Qt.AlignRight)
        
        # Title
        title_label = QLabel(f" {Assistantname.capitalize()} AI ")
        title_label.setStyleSheet("color: black; font-size: 18px; background-color:white")
        layout.addWidget(title_label)
        
        # Spacer
        layout.addStretch(1)
        
        # Navigation buttons
        home_button = self.create_button("Home.png", "  Home")
        home_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        layout.addWidget(home_button)
        
        chat_button = self.create_button("Chats.png", " Chat")
        chat_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        layout.addWidget(chat_button)
        
        # Spacer
        layout.addStretch(1)
        
        # Window controls
        minimize_button = self.create_button("Minimize2.png")
        minimize_button.clicked.connect(self.parent().showMinimized)
        layout.addWidget(minimize_button)
        
        self.maximize_button = self.create_button("Maximize.png")
        self.maximize_button.clicked.connect(self.toggle_maximize)
        layout.addWidget(self.maximize_button)
        
        close_button = self.create_button("Close.png")
        close_button.clicked.connect(self.parent().close)
        layout.addWidget(close_button)
        
        # Dragging functionality
        self.draggable = True
        self.offset = None

    def create_button(self, icon_name, text=None):
        button = QPushButton()
        icon_path = GraphicsDirectoryPath(icon_name)
        if os.path.exists(icon_path):
            button.setIcon(QIcon(icon_path))
        if text:
            button.setText(text)
        button.setStyleSheet("""
            height: 40px; 
            line-height: 40px; 
            background-color: white; 
            color: black;
            border: none;
        """)
        return button

    def toggle_maximize(self):
        if self.parent().isMaximized():
            self.parent().showNormal()
            self.maximize_button.setIcon(QIcon(GraphicsDirectoryPath("Maximize.png")))
        else:
            self.parent().showMaximized()
            self.maximize_button.setIcon(QIcon(GraphicsDirectoryPath("Minimize.png")))

    def mousePressEvent(self, event):
        if self.draggable and event.button() == Qt.LeftButton:
            self.offset = event.pos()

    def mouseMoveEvent(self, event):
        if self.draggable and self.offset and event.buttons() & Qt.LeftButton:
            self.parent().move(event.globalPos() - self.offset)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.setWindowFlags(Qt.FramelessWindowHint)
        
        # Get screen dimensions
        desktop = QApplication.desktop()
        screen_width = desktop.screenGeometry().width()
        screen_height = desktop.screenGeometry().height()
        
        # Create stacked widget for screens
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.addWidget(InitialScreen())
        self.stacked_widget.addWidget(MessageScreen())
        
        # Set window properties
        self.setGeometry(0, 0, screen_width, screen_height)
        self.setStyleSheet("background-color: black;")
        
        # Add top bar
        self.setMenuWidget(CustomTopBar(self, self.stacked_widget))
        self.setCentralWidget(self.stacked_widget)

def main():
    # Suppress the QApplication thread warning
    import warnings
    warnings.filterwarnings("ignore", category=RuntimeWarning)
    
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

def GraphicalUserInterface():
    # Identical to main()
    import warnings
    warnings.filterwarnings("ignore", category=RuntimeWarning)
    
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()