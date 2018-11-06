from PyQt4.QtCore import *
from PyQt4.QtGui import *
import user_interface
import sys
import os
import validate

validation_status_dict = {0: 'New', 1: 'Waiting', 2: 'Valid', 3: 'Invalid'}


class Main(QMainWindow, user_interface.Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)

        self.load_schema()

        self.add_button.clicked.connect(self.file_selector)


    def file_selector(self):
        list_of_files = QFileDialog.getOpenFileNames(self, caption="Select Files", directory=".",
                                                     filter='All Files (*.*)')
        for file in list_of_files:
            row_num = self.table.rowCount()
            self.table.insertRow(row_num)

            chk_box_item = QTableWidgetItem()
            chk_box_item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            chk_box_item.setCheckState(Qt.Unchecked)

            self.table.setItem(row_num, 0, chk_box_item)
            self.table.setItem(row_num, 1, QTableWidgetItem('0'))
            self.table.setItem(row_num, 2, QTableWidgetItem(file))  # filename only
            self.table.setItem(row_num, 3, QTableWidgetItem(validation_status_dict[0]))

    def load_schema(self):
        count = 0
        for file in os.listdir("schemas/"):
            if file.endswith(".xsd"):
                self.comboBox.addItem(file.split('.')[-2])
                if count == 0 or count == 1: count += 1

        if count == 1:
            self.comboBox.setEnabled(False)
        elif count == 2:
            self.comboBox.setEnabled(True)
        else:
            print('No Schema found')


app = QApplication(sys.argv)
main_obj = Main()
main_obj.show()
sys.exit(app.exec_())
