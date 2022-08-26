from PySide6.QtWidgets import QListWidget, QListWidgetItem
import logging


class QListLogger(logging.Handler):
    def __init__(self):
        super(QListLogger, self).__init__()
        self.widget = None

    def set_widget(self, widget: QListWidget):
        self.widget = widget

    def emit(self, record):
        message = self.format(record)

        item = QListWidgetItem(message)
        self.widget.insertItem(self.widget.currentRow(), item)
