import sqlite3
import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QApplication
from PyQt5.QtCore import Qt


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(790, 530)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.btn_add_coffee = QtWidgets.QPushButton(self.centralwidget)
        self.btn_add_coffee.setObjectName("btn_add_coffee")
        self.gridLayout.addWidget(self.btn_add_coffee, 0, 0, 1, 1)
        self.btn_edit_coffe = QtWidgets.QPushButton(self.centralwidget)
        self.btn_edit_coffe.setObjectName("btn_edit_coffe")
        self.gridLayout.addWidget(self.btn_edit_coffe, 0, 1, 1, 1)
        self.coffee_table = QtWidgets.QTableWidget(self.centralwidget)
        self.coffee_table.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.coffee_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.coffee_table.setTabKeyNavigation(True)
        self.coffee_table.setProperty("showDropIndicator", True)
        self.coffee_table.setDragEnabled(False)
        self.coffee_table.setDragDropOverwriteMode(True)
        self.coffee_table.setDragDropMode(QtWidgets.QAbstractItemView.NoDragDrop)
        self.coffee_table.setDefaultDropAction(QtCore.Qt.IgnoreAction)
        self.coffee_table.setAlternatingRowColors(False)
        self.coffee_table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.coffee_table.setTextElideMode(QtCore.Qt.ElideRight)
        self.coffee_table.setObjectName("coffee_table")
        self.coffee_table.setColumnCount(0)
        self.coffee_table.setRowCount(0)
        self.coffee_table.horizontalHeader().setVisible(True)
        self.coffee_table.horizontalHeader().setCascadingSectionResizes(False)
        self.coffee_table.horizontalHeader().setHighlightSections(True)
        self.coffee_table.horizontalHeader().setSortIndicatorShown(False)
        self.coffee_table.horizontalHeader().setStretchLastSection(False)
        self.coffee_table.verticalHeader().setCascadingSectionResizes(False)
        self.coffee_table.verticalHeader().setHighlightSections(True)
        self.coffee_table.verticalHeader().setStretchLastSection(False)
        self.gridLayout.addWidget(self.coffee_table, 1, 0, 1, 2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 790, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Капучино"))
        self.btn_add_coffee.setText(_translate("MainWindow", "Добавить кофе"))
        self.btn_edit_coffe.setText(_translate("MainWindow", "Изменить кофе"))


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.add_coffee_widget = None
        self.edit_coffee_widget = None
        self.setupUi(self)
        self.con = sqlite3.connect("coffee.sqlite")
        self.cur = self.con.cursor()
        self.btn_add_coffee.clicked.connect(self.add_coffee)
        self.btn_edit_coffe.clicked.connect(self.edit_coffee)
        self.update_coffee()

    def add_coffee(self):
        self.add_coffee_widget = AddEditCoffee(self)
        self.add_coffee_widget.show()

    def edit_coffee(self):
        rows = list(set([i.row() for i in self.coffee_table.selectedItems()]))
        ids = [self.coffee_table.item(i, 0).text() for i in rows]
        if len(ids) != 1:
            self.statusbar.showMessage('Выберите 1 кофе!')
        else:
            self.edit_coffee_widget = AddEditCoffee(self, ids[0])
            self.edit_coffee_widget.show()

    def update_coffee(self):
        self.coffee_table.clearContents()
        result = self.cur.execute("""SELECT * FROM coffee""").fetchall()
        self.coffee_table.setRowCount(len(result))
        self.coffee_table.setColumnCount(len(result[0]))
        self.coffee_table.setHorizontalHeaderLabels(
            ['ID', "Название сорта", "Степень обжарки", "Молотый/в зёрнах", "Описание вкуса", "Цена в рублях",
             "Объём упаковки в граммах"])
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.coffee_table.setItem(i, j, QTableWidgetItem(str(val)))
        self.statusbar.showMessage('')
        self.coffee_table.resizeColumnsToContents()


class Ui_addEditCoffeeForm(object):
    def setupUi(self, addEditCoffeeForm):
        addEditCoffeeForm.setObjectName("addEditCoffeeForm")
        addEditCoffeeForm.resize(305, 533)
        addEditCoffeeForm.setMinimumSize(QtCore.QSize(0, 0))
        addEditCoffeeForm.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.centralwidget = QtWidgets.QWidget(addEditCoffeeForm)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setHorizontalSpacing(6)
        self.gridLayout.setVerticalSpacing(3)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 4, 0, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 5, 0, 1, 1)
        self.type = QtWidgets.QPlainTextEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.type.sizePolicy().hasHeightForWidth())
        self.type.setSizePolicy(sizePolicy)
        self.type.setObjectName("type")
        self.gridLayout.addWidget(self.type, 0, 1, 1, 1)
        self.degree = QtWidgets.QPlainTextEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.degree.sizePolicy().hasHeightForWidth())
        self.degree.setSizePolicy(sizePolicy)
        self.degree.setObjectName("degree")
        self.gridLayout.addWidget(self.degree, 1, 1, 1, 1)
        self.in_what = QtWidgets.QPlainTextEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.in_what.sizePolicy().hasHeightForWidth())
        self.in_what.setSizePolicy(sizePolicy)
        self.in_what.setObjectName("in_what")
        self.gridLayout.addWidget(self.in_what, 2, 1, 1, 1)
        self.description = QtWidgets.QPlainTextEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.description.sizePolicy().hasHeightForWidth())
        self.description.setSizePolicy(sizePolicy)
        self.description.setObjectName("description")
        self.gridLayout.addWidget(self.description, 3, 1, 1, 1)
        self.price = QtWidgets.QPlainTextEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.price.sizePolicy().hasHeightForWidth())
        self.price.setSizePolicy(sizePolicy)
        self.price.setObjectName("price")
        self.gridLayout.addWidget(self.price, 4, 1, 1, 1)
        self.amount = QtWidgets.QPlainTextEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.amount.sizePolicy().hasHeightForWidth())
        self.amount.setSizePolicy(sizePolicy)
        self.amount.setObjectName("amount")
        self.gridLayout.addWidget(self.amount, 5, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.btn_add_or_edit = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_add_or_edit.sizePolicy().hasHeightForWidth())
        self.btn_add_or_edit.setSizePolicy(sizePolicy)
        self.btn_add_or_edit.setObjectName("btn_add_or_edit")
        self.verticalLayout.addWidget(self.btn_add_or_edit)
        self.gridLayout_2.addLayout(self.verticalLayout, 0, 0, 1, 1)
        addEditCoffeeForm.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(addEditCoffeeForm)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 305, 21))
        self.menubar.setObjectName("menubar")
        addEditCoffeeForm.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(addEditCoffeeForm)
        self.statusbar.setObjectName("statusbar")
        addEditCoffeeForm.setStatusBar(self.statusbar)

        self.retranslateUi(addEditCoffeeForm)
        QtCore.QMetaObject.connectSlotsByName(addEditCoffeeForm)

    def retranslateUi(self, addEditCoffeeForm):
        _translate = QtCore.QCoreApplication.translate
        addEditCoffeeForm.setWindowTitle(_translate("addEditCoffeeForm", "Добавить кофе"))
        self.label.setText(_translate("addEditCoffeeForm", "Название сорта"))
        self.label_2.setText(_translate("addEditCoffeeForm", "Степень обжарки"))
        self.label_3.setText(_translate("addEditCoffeeForm", "Молотый/в зёрнах"))
        self.label_4.setText(_translate("addEditCoffeeForm", "Описание вкуса"))
        self.label_5.setText(_translate("addEditCoffeeForm", "Цена"))
        self.label_6.setText(_translate("addEditCoffeeForm", "Объём упаковки"))
        self.btn_add_or_edit.setText(_translate("addEditCoffeeForm", "Добавить"))


class AddEditCoffee(QMainWindow, Ui_addEditCoffeeForm):
    def __init__(self, parent=None, coffee_id=None):
        super().__init__(parent)
        self.setupUi(self)
        self.parent = parent
        self.coffee_id = coffee_id
        self.setWindowModality(Qt.ApplicationModal)
        if coffee_id is not None:
            self.btn_add_or_edit.clicked.connect(self.edit_elem)
            self.btn_add_or_edit.setText('Отредактировать')
            self.setWindowTitle('Редактирование записи')
            self.get_elem()  # метод, заполняющий форму
        else:
            self.btn_add_or_edit.clicked.connect(self.add_coffee)

    def add_coffee(self):
        if self.get_adding_verdict():
            type_r, degree, in_what, description, price, amount = self.type.toPlainText(), self.degree.toPlainText(), \
                self.in_what.toPlainText(), self.description.toPlainText(), self.price.toPlainText(), \
                self.amount.toPlainText()
            self.parent.cur.execute(f"""INSERT INTO coffee(type, degree, in_what, description, price, amount) 
            VALUES('{type_r}', '{degree}', '{in_what}', '{description}', {price}, {amount})""")
            self.parent.con.commit()
            self.parent.update_coffee()
            self.close()
        else:
            self.statusbar.showMessage('Неверно заполнена форма')

    def get_elem(self):
        data = self.parent.cur.execute("SELECT * FROM coffee WHERE id = ?", (self.coffee_id,)).fetchone()
        self.type.setPlainText(str(data[1]))
        self.degree.setPlainText(str(data[2]))
        self.in_what.setPlainText(data[3])
        self.description.setPlainText(str(data[4]))
        self.price.setPlainText(str(data[5]))
        self.amount.setPlainText(str(data[6]))

    def edit_elem(self):
        if self.get_editing_verdict():
            type_r, degree, in_what, description, price, amount = self.type.toPlainText(), self.degree.toPlainText(), \
                self.in_what.toPlainText(), self.description.toPlainText(), self.price.toPlainText(), \
                self.amount.toPlainText()
            self.parent.cur.execute(
                """UPDATE coffee SET type = ?, degree = ?, in_what = ?, description = ?, price = ?, amount = ? 
                WHERE id = ?""",
                (type_r, degree, in_what, description, price, amount, self.coffee_id))
            self.parent.con.commit()
            self.parent.update_coffee()
            self.close()
        else:
            self.statusbar.showMessage('Неверно заполнена форма')

    def get_adding_verdict(self):
        try:
            return int(self.amount.toPlainText()) > 0 and int(
                self.price.toPlainText()) > 0 and self.in_what.toPlainText().lower() in (
                'молотый', 'в зернах', 'в зёрнах') and all([self.type.toPlainText(), self.degree.toPlainText(),
                                                            self.in_what.toPlainText(), self.description.toPlainText(),
                                                            self.price.toPlainText(),
                                                            self.amount.toPlainText()])
        except ValueError:
            return False

    def get_editing_verdict(self):
        try:
            return int(self.amount.toPlainText()) > 0 and int(
                self.price.toPlainText()) > 0 and self.in_what.toPlainText().lower() in (
                'молотый', 'в зернах', 'в зёрнах') and all([self.type.toPlainText(), self.degree.toPlainText(),
                                                            self.in_what.toPlainText(), self.description.toPlainText(),
                                                            self.price.toPlainText(),
                                                            self.amount.toPlainText()])
        except ValueError:
            return False


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = MainWindow()
    form.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
