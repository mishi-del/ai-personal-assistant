import sys
import json
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QTextEdit, QPushButton, QLineEdit, 
                            QLabel, QScrollArea, QFrame)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont, QIcon, QColor
from qt_material import apply_stylesheet
from agent import AIAgent
from config import default_config

class ChatMessage(QFrame):
    """Custom widget for chat messages"""
    def __init__(self, text, is_user=True, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setObjectName("chatMessage")
        
        layout = QHBoxLayout()
        message = QLabel(text)
        message.setWordWrap(True)
        message.setTextFormat(Qt.TextFormat.RichText)
        
        if is_user:
            layout.addStretch()
            self.setStyleSheet("""
                QFrame#chatMessage {
                    background-color: #DCF8C6;
                    border-radius: 10px;
                    margin: 5px;
                    padding: 10px;
                }
            """)
        else:
            self.setStyleSheet("""
                QFrame#chatMessage {
                    background-color: #E8E8E8;
                    border-radius: 10px;
                    margin: 5px;
                    padding: 10px;
                }
            """)
            
        layout.addWidget(message)
        
        if not is_user:
            layout.addStretch()
            
        self.setLayout(layout)

class AgentThread(QThread):
    """Thread for running AI agent commands"""
    response_ready = pyqtSignal(str)
    
    def __init__(self, agent, command):
        super().__init__()
        self.agent = agent
        self.command = command
        
    def run(self):
        response = self.agent.process_command(self.command)
        self.response_ready.emit(response)

class AIAssistantGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.agent = AIAgent()
        self.init_ui()
        
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle('AI Assistant')
        self.setMinimumSize(800, 600)
        
        # Create main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        
        # Create chat area
        self.chat_area = QWidget()
        self.chat_layout = QVBoxLayout(self.chat_area)
        self.chat_layout.addStretch()
        
        # Create scroll area for chat
        scroll = QScrollArea()
        scroll.setWidget(self.chat_area)
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        # Create input area
        input_widget = QWidget()
        input_layout = QHBoxLayout(input_widget)
        
        # Create input field
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Type your message here...")
        self.input_field.returnPressed.connect(self.send_message)
        
        # Create send button
        send_button = QPushButton("Send")
        send_button.clicked.connect(self.send_message)
        
        # Add widgets to input layout
        input_layout.addWidget(self.input_field)
        input_layout.addWidget(send_button)
        
        # Add welcome message
        welcome_text = """
        <h3>Welcome to AI Assistant!</h3>
        <p>I can help you with:</p>
        <ul>
            <li>Opening websites (e.g., 'open google')</li>
            <li>Searching the web (e.g., 'search for restaurants near me')</li>
            <li>Getting directions (e.g., 'get directions from New York to Boston')</li>
            <li>Checking weather (e.g., 'what's the weather in London')</li>
            <li>Booking restaurants (e.g., 'book a table for dinner')</li>
            <li>And more!</li>
        </ul>
        <p>How can I assist you today?</p>
        """
        self.add_message(welcome_text, False)
        
        # Add widgets to main layout
        layout.addWidget(scroll)
        layout.addWidget(input_widget)
        
        # Apply styling
        self.apply_styles()
        
    def apply_styles(self):
        """Apply custom styles to the GUI"""
        # Apply material theme
        apply_stylesheet(self, theme='light_blue.xml')
        
        # Custom styles
        self.setStyleSheet("""
            QMainWindow {
                background-color: #F0F2F5;
            }
            QScrollArea {
                border: none;
                background-color: #F0F2F5;
            }
            QLineEdit {
                padding: 10px;
                border-radius: 20px;
                border: 1px solid #E0E0E0;
                background-color: white;
                font-size: 14px;
            }
            QPushButton {
                padding: 10px 20px;
                border-radius: 20px;
                background-color: #0D47A1;
                color: white;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1565C0;
            }
        """)
        
    def add_message(self, text: str, is_user: bool):
        """Add a message to the chat area"""
        message = ChatMessage(text, is_user)
        self.chat_layout.insertWidget(self.chat_layout.count() - 1, message)
        
    def send_message(self):
        """Handle sending a message"""
        text = self.input_field.text().strip()
        if not text:
            return
            
        # Add user message to chat
        self.add_message(text, True)
        self.input_field.clear()
        
        # Process message in separate thread
        self.thread = AgentThread(self.agent, text)
        self.thread.response_ready.connect(self.handle_response)
        self.thread.start()
        
    def handle_response(self, response: str):
        """Handle the agent's response"""
        self.add_message(response, False)

def main():
    app = QApplication(sys.argv)
    window = AIAssistantGUI()
    window.show()
    sys.exit(app.exec()) 