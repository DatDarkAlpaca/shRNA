from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
import logging


class HTMLDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super(HTMLDelegate, self).__init__(parent)
        self.doc = QTextDocument(self)

    def paint(self, painter, option, index):
        painter.save()
        options = QStyleOptionViewItem(option)
        self.initStyleOption(options, index)
        self.doc.setHtml(options.text)
        options.text = ""
        style = QApplication.style() if options.widget is None \
            else options.widget.style()
        style.drawControl(QStyle.CE_ItemViewItem, options, painter)

        ctx = QAbstractTextDocumentLayout.PaintContext()
        if option.state & QStyle.State_Selected:
            ctx.palette.setColor(QPalette.Text, option.palette.color(QPalette.Active, QPalette.HighlightedText))
        else:
            ctx.palette.setColor(QPalette.Text, option.palette.color(
                QPalette.Active, QPalette.Text))
        textRect = style.subElementRect(QStyle.SE_ItemViewItemText, options, None)
        if index.column() != 0:
            textRect.adjust(5, 0, 0, 0)
        constant = 4
        margin = (option.rect.height() - options.fontMetrics.height()) // 2
        margin = margin - constant
        textRect.setTop(textRect.top() + margin)

        painter.translate(textRect.topLeft())
        painter.setClipRect(textRect.translated(-textRect.topLeft()))
        self.doc.documentLayout().draw(painter, ctx)
        painter.restore()

    def sizeHint(self, option, index):
        return QSize(self.doc.idealWidth(), self.doc.size().height())


# Todo: move to a utils module.
def colored(text: str, color: str, bold: bool = False) -> str:
    bold = f"<strong>{text}</strong>" if bold else text
    return f"<span style=\"color:{color};\">{bold}</span>"


class QListLogger(logging.Handler):
    def __init__(self):
        super(QListLogger, self).__init__()
        self.widget, self.logger = [None] * 2

    def set_widget(self, widget: QListWidget):
        self.widget = widget

        delegate = HTMLDelegate()
        self.widget.setItemDelegate(delegate)

    def emit(self, record):
        logger_name = f"[ {record.name} ]"
        level = record.levelno
        message = self.format(record)

        message = f"{colored(logger_name, '#2F77D3')} {self.get_level_formatted(level)}: {colored(message, '#FF6B68')}"

        item = QListWidgetItem(message)
        self.widget.insertItem(self.widget.currentRow(), item)

    @staticmethod
    def get_level_formatted(level: int) -> str:
        level_to_format = {
            logging.CRITICAL: colored('CRITICAL', '#D63033', True),
            logging.ERROR: colored('ERROR', '#D63033'),
            logging.WARNING: colored('WARNING', '#FEFF69'),
            logging.INFO: colored('INFO', '#9C9B9B'),
            logging.DEBUG: colored('DEBUG', '#9C9B9B'),
            logging.NOTSET: '',
        }

        return level_to_format[level]
