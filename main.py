# This Python file uses the following encoding: utf-8
import sys
import io


from PyQt6.QtSql import QSqlDatabase, QSqlTableModel
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6 import uic


class InteractiveReceipt(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        # f = io.StringIO(template)
        uic.loadUi("main.ui", self)
        db = QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName("coffee.sqlite")
        db.open()

        model = QSqlTableModel(self, db)
        model.setTable("coffee")
        model.select()
        self.tableView.setModel(model)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = InteractiveReceipt()
    widget.show()
    sys.exit(app.exec())
