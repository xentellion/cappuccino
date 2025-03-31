# This Python file uses the following encoding: utf-8
import sys
import io
import sqlite3


from PyQt6.QtSql import QSqlDatabase, QSqlTableModel
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QMessageBox
from PyQt6 import uic

from main_screen import Ui_MainWindow
from addEditCoffeeForm import Ui_Form


class AddWidget(QWidget, Ui_Form):
    def __init__(self, parent=None, changed_line=None):
        super().__init__(parent)
        self.params = self.set_params()
        self.setupUi(self)
        self.changed_line = changed_line
        self.save.clicked.connect(self.update_db)

        if self.changed_line is not None:
            idx = self.changed_line - 1
            self.sort_name.setText(self.params[idx][1])
            self.roasting.setText(str(self.params[idx][2]))
            self.milled.setText(str(self.params[idx][3]))
            self.taste.setText(self.params[idx][4])
            self.price.setText(str(self.params[idx][5]))
            self.volume.setText(str(self.params[idx][6]))

    def update_db(self):
        if not self.changed_line:
            query = f"""
                INSERT INTO coffee 
                (sort_name, roasting, milled, taste_desc, price, volume)
                VALUES
                ({self.sort_name.text()}, {self.roasting.text()}, {self.milled.text()}, 
                {self.taste.text()}, {self.price.text()}, {self.volume.text()})
            """
        else:
            query = f"""
                UPDATE coffee 
                SET 
                    sort_name = "{self.sort_name.text()}",
                    roasting = {int(self.roasting.text())},
                    milled = {int(self.milled.text())},
                    taste_desc = "{self.taste.text()}",
                    price = {int(self.price.text())},
                    volume = {float(self.volume.text())}
                WHERE id = {self.params[self.changed_line - 1][0]};
            """
        try:
            with sqlite3.connect(self.parent().db.databaseName()) as con:
                con.cursor().execute(query).fetchall()
        except Exception as e:
            # Я знаю, такая себе практика, но мне сейчас все равно
            QMessageBox.warning(
                self,
                "",
                "Ошибка: " + e.__class__.__name__,
                buttons=QMessageBox.StandardButton.Ok,
            )

        self.close()
        self.parent().load_data()

    def set_params(self):
        query = "SELECT * FROM coffee;"
        with sqlite3.connect(self.parent().db.databaseName()) as con:
            data = con.cursor().execute(query).fetchall()
            return data


class InteractiveReceipt(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        # f = io.StringIO(template)
        self.setupUi(self)
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName("data/coffee.sqlite")

        self.load_data()

        self.add_coffee.clicked.connect(self.new_coffee)
        self.change_coffee.clicked.connect(self.change_coffee_q)

    def load_data(self):
        self.db.open()
        model = QSqlTableModel(self, self.db)
        model.setTable("coffee")
        model.select()
        self.tableView.setModel(model)
        self.db.close()

    def new_coffee(self):
        self.add_form = AddWidget(parent=self)
        self.add_form.show()

    def change_coffee_q(self):
        # Get selcted line id
        index = self.tableView.currentIndex()
        self.add_form = AddWidget(
            parent=self, changed_line=self.tableView.model().data(index)
        )
        self.add_form.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = InteractiveReceipt()
    widget.show()
    sys.exit(app.exec())
