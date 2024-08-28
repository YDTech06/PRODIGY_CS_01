# IMPORTS
import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QTextEdit, QPushButton,
    QMessageBox, QGridLayout
)
from PyQt5.QtCore import Qt

# CLASS DEFINITION AND INITIALIZATION
# CAESAR-CIPHER APP CLASS
class CaesarCipherApp(QWidget):
    # INITIALIZATION
    def __init__(self):
        
        # Initialize the Caesar Cipher application window.
        super().__init__()
        self.initUI()

    # UI INITIALIZATION
    # USER INTERFACE SETUP
    def initUI(self):
        
        # Set up the user interface components
        self.setWindowTitle('Caesar Cipher Tool')
        self.setGeometry(100, 100, 500, 400)
        layout = QVBoxLayout()

        # Input text field
        self.input_label = QLabel('Enter the message:')
        self.input_text = QTextEdit()
        layout.addWidget(self.input_label)
        layout.addWidget(self.input_text)

        # Shift value input
        self.shift_label = QLabel('Enter the shift value (0-25):')
        self.shift_entry = QLineEdit()
        layout.addWidget(self.shift_label)
        layout.addWidget(self.shift_entry)

        # Button layout setup using grid layout
        button_layout = QGridLayout()
        
        # Encrypt button
        self.encrypt_button = QPushButton('Encrypt')
        self.encrypt_button.setStyleSheet("background-color: green; color: white; font-weight: bold;")
        self.encrypt_button.setFixedSize(150, 40)
        self.encrypt_button.clicked.connect(self.encrypt_text)
        self.encrypt_button.installEventFilter(self)
        button_layout.addWidget(self.encrypt_button, 0, 0)
        
        # Copy button
        self.copy_button = QPushButton('Copy')
        self.copy_button.setStyleSheet("background-color: #2196F3; color: white; font-weight: bold;")
        self.copy_button.setFixedSize(150, 40)
        self.copy_button.clicked.connect(self.copy_to_clipboard)
        self.copy_button.installEventFilter(self)
        button_layout.addWidget(self.copy_button, 0, 1)

        # Decrypt button
        self.decrypt_button = QPushButton('Decrypt')
        self.decrypt_button.setStyleSheet("background-color: #f44336; color: white; font-weight: bold;")
        self.decrypt_button.setFixedSize(150, 40)
        self.decrypt_button.clicked.connect(self.decrypt_text)
        self.decrypt_button.installEventFilter(self)
        button_layout.addWidget(self.decrypt_button, 0, 2)
        
        # Align buttons centrally
        button_layout.setColumnStretch(0, 1)
        button_layout.setColumnStretch(1, 1)
        button_layout.setColumnStretch(2, 1)
        button_layout.setAlignment(Qt.AlignCenter)
        layout.addLayout(button_layout)

        # Result output field
        self.result_label = QLabel('Result:')
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        layout.addWidget(self.result_label)
        layout.addWidget(self.output_text)

        # Set the layout for the main widget
        self.setLayout(layout)

    # CAESAR CIPHER METHOD
    def caesar_cipher(self, text, shift, mode):
    
        # Encrypt or decrypt text using Caesar cipher with the given shift.
        result = ''
        for char in text:
            if char.isalpha():
                # Shift character code
                shifted = ord(char) + shift if mode == 'encrypt' else ord(char) - shift
                # Wrap around the alphabet for lower-case characters
                if char.islower():
                    if shifted > ord('z'):
                        shifted -= 26
                    elif shifted < ord('a'):
                        shifted += 26
                # Wrap around the alphabet for upper-case characters
                elif char.isupper():
                    if shifted > ord('Z'):
                        shifted -= 26
                    elif shifted < ord('A'):
                        shifted += 26
                result += chr(shifted)
            else:
                # Non-alphabetic characters are added unchanged
                result += char
        return result

    # TEXT PROCESSING
    # ENCRYPT TEXT
    def encrypt_text(self):
        
        # Encrypt the text using the Caesar cipher and update the result.
        self.process_text('encrypt')

    # DECRYPT TEXT
    def decrypt_text(self):
        
        # Decrypt the text using the Caesar cipher and update the result.
        self.process_text('decrypt')

    # PROCESSING TEXT
    def process_text(self, mode):
        
        # Process the input text with Caesar cipher encryption or decryption.
        text = self.input_text.toPlainText()
        try:
            shift = int(self.shift_entry.text())
            if not (0 <= shift <= 25):
                raise ValueError("Shift value must be between 0 and 25.")
        except ValueError as e:
            QMessageBox.critical(self, "Error", f"Invalid shift value: {e}")
            return

        result = self.caesar_cipher(text, shift, mode)
        self.output_text.setPlainText(result)

    # CLIPBOARD OPERATIONS
    def copy_to_clipboard(self):
        
        # Copy the result text to the clipboard and show a confirmation message.
        clipboard = QApplication.clipboard()
        clipboard.setText(self.output_text.toPlainText())
        QMessageBox.information(self, "Copied", "Result copied to clipboard!")

    # EVENT HANDLING
    def eventFilter(self, obj, event):
        
        # Handle button hover effects to change styles on mouse events.
        if event.type() == event.Enter:
            if obj == self.encrypt_button:
                obj.setStyleSheet("background-color: #43a047; color: white; font-weight: bold;")
            elif obj == self.decrypt_button:
                obj.setStyleSheet("background-color: #e53935; color: white; font-weight: bold;")
            elif obj == self.copy_button:
                obj.setStyleSheet("background-color: #1976D2; color: white; font-weight: bold;")
        elif event.type() == event.Leave:
            if obj == self.encrypt_button:
                obj.setStyleSheet("background-color: #4caf50; color: white; font-weight: bold;")
            elif obj == self.decrypt_button:
                obj.setStyleSheet("background-color: #f44336; color: white; font-weight: bold;")
            elif obj == self.copy_button:
                obj.setStyleSheet("background-color: #2196F3; color: white; font-weight: bold;")
        return super().eventFilter(obj, event)

    # APPLICATION EXIT 
    # CLOSE EVENT HANDLING
    def closeEvent(self, event):
        
        # Prompt the user for confirmation before closing the application.
        reply = QMessageBox.question(self, 'Quit', "Do you want to quit?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

# MAIN EXECUTION
# MAIN BLOCK
if __name__ == '__main__':
    # Create the application instance and main window, then start the event loop
    app = QApplication(sys.argv)
    window = CaesarCipherApp()
    window.show()
    sys.exit(app.exec_())
