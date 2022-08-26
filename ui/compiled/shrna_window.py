# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'shrna_window.ui'
##
## Created by: Qt User Interface Compiler version 6.3.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QHBoxLayout, QHeaderView,
    QLabel, QLineEdit, QListWidget, QListWidgetItem,
    QMainWindow, QMenu, QMenuBar, QPushButton,
    QSizePolicy, QSpacerItem, QStatusBar, QTableWidget,
    QTableWidgetItem, QVBoxLayout, QWidget)

class Ui_shRNAWindow(object):
    def setupUi(self, shRNAWindow):
        if not shRNAWindow.objectName():
            shRNAWindow.setObjectName(u"shRNAWindow")
        shRNAWindow.resize(764, 493)
        shRNAWindow.setMinimumSize(QSize(600, 320))
        self.action_exit = QAction(shRNAWindow)
        self.action_exit.setObjectName(u"action_exit")
        self.action_open_rna_file = QAction(shRNAWindow)
        self.action_open_rna_file.setObjectName(u"action_open_rna_file")
        self.central_widget = QWidget(shRNAWindow)
        self.central_widget.setObjectName(u"central_widget")
        self.horizontalLayout = QHBoxLayout(self.central_widget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.left_layout = QVBoxLayout()
        self.left_layout.setObjectName(u"left_layout")
        self.left_layout.setContentsMargins(-1, -1, 0, -1)
        self.input_label = QLabel(self.central_widget)
        self.input_label.setObjectName(u"input_label")

        self.left_layout.addWidget(self.input_label)

        self.input_edit = QLineEdit(self.central_widget)
        self.input_edit.setObjectName(u"input_edit")

        self.left_layout.addWidget(self.input_edit)

        self.button_layout = QHBoxLayout()
        self.button_layout.setObjectName(u"button_layout")
        self.button_layout.setContentsMargins(-1, 0, -1, -1)
        self.button_spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.button_layout.addItem(self.button_spacer)

        self.load_rna_button = QPushButton(self.central_widget)
        self.load_rna_button.setObjectName(u"load_rna_button")

        self.button_layout.addWidget(self.load_rna_button)

        self.fetch_button = QPushButton(self.central_widget)
        self.fetch_button.setObjectName(u"fetch_button")

        self.button_layout.addWidget(self.fetch_button)


        self.left_layout.addLayout(self.button_layout)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.left_layout.addItem(self.verticalSpacer_2)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.left_layout.addItem(self.verticalSpacer)

        self.debug_log_label = QLabel(self.central_widget)
        self.debug_log_label.setObjectName(u"debug_log_label")

        self.left_layout.addWidget(self.debug_log_label)

        self.debug_log_list = QListWidget(self.central_widget)
        self.debug_log_list.setObjectName(u"debug_log_list")
        self.debug_log_list.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.debug_log_list.setSelectionMode(QAbstractItemView.SingleSelection)

        self.left_layout.addWidget(self.debug_log_list)

        self.debug_clear_layout = QHBoxLayout()
        self.debug_clear_layout.setObjectName(u"debug_clear_layout")
        self.debug_clear_layout.setContentsMargins(-1, 0, -1, -1)
        self.debug_clear_spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.debug_clear_layout.addItem(self.debug_clear_spacer)

        self.debug_clear_button = QPushButton(self.central_widget)
        self.debug_clear_button.setObjectName(u"debug_clear_button")

        self.debug_clear_layout.addWidget(self.debug_clear_button)


        self.left_layout.addLayout(self.debug_clear_layout)


        self.horizontalLayout.addLayout(self.left_layout)

        self.right_layout = QVBoxLayout()
        self.right_layout.setObjectName(u"right_layout")
        self.right_layout.setContentsMargins(-1, -1, 0, -1)
        self.results_label = QLabel(self.central_widget)
        self.results_label.setObjectName(u"results_label")

        self.right_layout.addWidget(self.results_label)

        self.results_table = QTableWidget(self.central_widget)
        self.results_table.setObjectName(u"results_table")
        self.results_table.horizontalHeader().setStretchLastSection(True)

        self.right_layout.addWidget(self.results_table)


        self.horizontalLayout.addLayout(self.right_layout)

        shRNAWindow.setCentralWidget(self.central_widget)
        self.status_bar = QStatusBar(shRNAWindow)
        self.status_bar.setObjectName(u"status_bar")
        shRNAWindow.setStatusBar(self.status_bar)
        self.menu_bar = QMenuBar(shRNAWindow)
        self.menu_bar.setObjectName(u"menu_bar")
        self.menu_bar.setGeometry(QRect(0, 0, 764, 22))
        self.menu_file = QMenu(self.menu_bar)
        self.menu_file.setObjectName(u"menu_file")
        shRNAWindow.setMenuBar(self.menu_bar)

        self.menu_bar.addAction(self.menu_file.menuAction())
        self.menu_file.addAction(self.action_exit)

        self.retranslateUi(shRNAWindow)
        self.action_exit.triggered.connect(shRNAWindow.close)

        QMetaObject.connectSlotsByName(shRNAWindow)
    # setupUi

    def retranslateUi(self, shRNAWindow):
        shRNAWindow.setWindowTitle(QCoreApplication.translate("shRNAWindow", u"shRNA v1.0", None))
        self.action_exit.setText(QCoreApplication.translate("shRNAWindow", u"Exit", None))
#if QT_CONFIG(shortcut)
        self.action_exit.setShortcut(QCoreApplication.translate("shRNAWindow", u"Ctrl+Q", None))
#endif // QT_CONFIG(shortcut)
        self.action_open_rna_file.setText(QCoreApplication.translate("shRNAWindow", u"Open RNA file...", None))
#if QT_CONFIG(shortcut)
        self.action_open_rna_file.setShortcut(QCoreApplication.translate("shRNAWindow", u"Ctrl+Shift+O", None))
#endif // QT_CONFIG(shortcut)
        self.input_label.setText(QCoreApplication.translate("shRNAWindow", u"Input:", None))
        self.input_edit.setPlaceholderText(QCoreApplication.translate("shRNAWindow", u"Enter a gene id...", None))
        self.load_rna_button.setText(QCoreApplication.translate("shRNAWindow", u"Load RNA", None))
        self.fetch_button.setText(QCoreApplication.translate("shRNAWindow", u"Fetch", None))
        self.debug_log_label.setText(QCoreApplication.translate("shRNAWindow", u"Debug Log:", None))
        self.debug_clear_button.setText(QCoreApplication.translate("shRNAWindow", u"Clear", None))
        self.results_label.setText(QCoreApplication.translate("shRNAWindow", u"Results:", None))
        self.menu_file.setTitle(QCoreApplication.translate("shRNAWindow", u"File", None))
    # retranslateUi

