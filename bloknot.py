import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QTextEdit,
    QAction,
    QFileDialog,
    QMessageBox,
)
from PyQt5.QtGui import QIcon


class NotepadApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # Set up the text area
        self.text_area = QTextEdit(self)
        self.setCentralWidget(self.text_area)

        # Create a menubar
        menubar = self.menuBar()

        # Create the file menu
        file_menu = menubar.addMenu("File")

        # Create actions for the file menu
        new_action = QAction("New", self)
        new_action.setShortcut("Ctrl+N")
        new_action.triggered.connect(self.new_file)
        file_menu.addAction(new_action)

        open_action = QAction("Open", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)

        save_action = QAction("Save", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)

        save_as_action = QAction("Save As", self)
        save_as_action.triggered.connect(self.save_file_as)
        file_menu.addAction(save_as_action)

        # Set up the window properties
        self.setWindowTitle("Bloknot")
        self.setWindowIcon(QIcon("notepad.png"))  # You can set your own icon here
        self.setGeometry(100, 100, 600, 400)

    def new_file(self):
        self.text_area.clear()

    def open_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Open File", "", "Text Files (*.txt);;All Files (*)", options=options
        )
        if file_name:
            with open(file_name, "r") as file:
                self.text_area.setPlainText(file.read())

    def save_file(self):
        if not hasattr(self, "current_file"):
            self.save_file_as()
        else:
            self.write_to_file(self.current_file)

    def save_file_as(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(
            self,
            "Save File",
            "",
            "Text Files (*.txt);;All Files (*)",
            options=options,
        )
        if file_name:
            self.current_file = file_name
            self.write_to_file(file_name)

    def write_to_file(self, file_name):
        try:
            with open(file_name, "w") as file:
                file.write(self.text_area.toPlainText())
        except Exception as e:
            QMessageBox.critical(
                self, "Error", f"An error occurred while saving the file: {e}"
            )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    notepad = NotepadApp()
    notepad.show()
    sys.exit(app.exec_())
