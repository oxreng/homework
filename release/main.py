import sqlite3
import sys
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QApplication
from PyQt5.QtCore import Qt
from UI.addEditCoffeeForm import Ui_addEditCoffeeForm
from UI.main import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.add_coffee_widget = None
        self.edit_coffee_widget = None
        self.setupUi(self)
        self.con = sqlite3.connect("data/coffee.sqlite")
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
