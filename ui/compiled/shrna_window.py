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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QFrame, QHBoxLayout,
    QHeaderView, QLabel, QLineEdit, QListWidget,
    QListWidgetItem, QMainWindow, QMenu, QMenuBar,
    QPushButton, QSizePolicy, QSpacerItem, QStatusBar,
    QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget)

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
        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        self.input_label.setFont(font)

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

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.left_layout.addItem(self.verticalSpacer_2)

        self.debug_log_label = QLabel(self.central_widget)
        self.debug_log_label.setObjectName(u"debug_log_label")
        self.debug_log_label.setFont(font)

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
        self.results_label.setFont(font)

        self.right_layout.addWidget(self.results_label)

        self.gene_id_label = QLabel(self.central_widget)
        self.gene_id_label.setObjectName(u"gene_id_label")

        self.right_layout.addWidget(self.gene_id_label)

        self.ncbi_result_label = QLabel(self.central_widget)
        self.ncbi_result_label.setObjectName(u"ncbi_result_label")

        self.right_layout.addWidget(self.ncbi_result_label)

        self.line = QFrame(self.central_widget)
        self.line.setObjectName(u"line")
        self.line.setFrameShadow(QFrame.Raised)
        self.line.setFrameShape(QFrame.HLine)

        self.right_layout.addWidget(self.line)

        self.label = QLabel(self.central_widget)
        self.label.setObjectName(u"label")

        self.right_layout.addWidget(self.label)

        self.results_table = QTableWidget(self.central_widget)
        if (self.results_table.columnCount() < 14):
            self.results_table.setColumnCount(14)
        __qtablewidgetitem = QTableWidgetItem()
        self.results_table.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.results_table.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.results_table.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.results_table.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.results_table.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.results_table.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.results_table.setHorizontalHeaderItem(6, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.results_table.setHorizontalHeaderItem(7, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.results_table.setHorizontalHeaderItem(8, __qtablewidgetitem8)
        __qtablewidgetitem9 = QTableWidgetItem()
        self.results_table.setHorizontalHeaderItem(9, __qtablewidgetitem9)
        __qtablewidgetitem10 = QTableWidgetItem()
        self.results_table.setHorizontalHeaderItem(10, __qtablewidgetitem10)
        __qtablewidgetitem11 = QTableWidgetItem()
        self.results_table.setHorizontalHeaderItem(11, __qtablewidgetitem11)
        __qtablewidgetitem12 = QTableWidgetItem()
        self.results_table.setHorizontalHeaderItem(12, __qtablewidgetitem12)
        __qtablewidgetitem13 = QTableWidgetItem()
        self.results_table.setHorizontalHeaderItem(13, __qtablewidgetitem13)
        self.results_table.setObjectName(u"results_table")
        self.results_table.setSortingEnabled(False)
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
        self.results_label.setText(QCoreApplication.translate("shRNAWindow", u"Results", None))
        self.gene_id_label.setText(QCoreApplication.translate("shRNAWindow", u"Gene ID:", None))
        self.ncbi_result_label.setText(QCoreApplication.translate("shRNAWindow", u"NCBI Information:", None))
        self.label.setText(QCoreApplication.translate("shRNAWindow", u"Results Table:", None))
        ___qtablewidgetitem = self.results_table.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("shRNAWindow", u"Index", None));
        ___qtablewidgetitem1 = self.results_table.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("shRNAWindow", u"Alvo", None));
        ___qtablewidgetitem2 = self.results_table.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("shRNAWindow", u"siRNA", None));
        ___qtablewidgetitem3 = self.results_table.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("shRNAWindow", u"Passageira", None));
        ___qtablewidgetitem4 = self.results_table.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("shRNAWindow", u"Alvos em H. para Senso", None));
        ___qtablewidgetitem5 = self.results_table.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("shRNAWindow", u"Genbank Senso", None));
        ___qtablewidgetitem6 = self.results_table.horizontalHeaderItem(6)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("shRNAWindow", u"Nome dos Genes do Senso", None));
        ___qtablewidgetitem7 = self.results_table.horizontalHeaderItem(7)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("shRNAWindow", u"Guia", None));
        ___qtablewidgetitem8 = self.results_table.horizontalHeaderItem(8)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("shRNAWindow", u"Tm Guia", None));
        ___qtablewidgetitem9 = self.results_table.horizontalHeaderItem(9)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("shRNAWindow", u"GC Guia", None));
        ___qtablewidgetitem10 = self.results_table.horizontalHeaderItem(10)
        ___qtablewidgetitem10.setText(QCoreApplication.translate("shRNAWindow", u"Alvos em H. para Guia", None));
        ___qtablewidgetitem11 = self.results_table.horizontalHeaderItem(11)
        ___qtablewidgetitem11.setText(QCoreApplication.translate("shRNAWindow", u"Genbank Guia", None));
        ___qtablewidgetitem12 = self.results_table.horizontalHeaderItem(12)
        ___qtablewidgetitem12.setText(QCoreApplication.translate("shRNAWindow", u"Nomes dos Genes da Guia", None));
        ___qtablewidgetitem13 = self.results_table.horizontalHeaderItem(13)
        ___qtablewidgetitem13.setText(QCoreApplication.translate("shRNAWindow", u"shRNA", None));
        self.menu_file.setTitle(QCoreApplication.translate("shRNAWindow", u"File", None))
    # retranslateUi

