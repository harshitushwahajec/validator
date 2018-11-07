from PyQt4.QtCore import *
from PyQt4.QtGui import *
import user_interface
import sys
import os
import validate

#move to config
validation_status_dict = {0: 'New', 1: 'Waiting', 2: 'Valid', 3: 'Invalid'}


class Main(QMainWindow, user_interface.Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.validate_obj = None
        self.list_of_schema = []
        self.load_schema_to_combobox()
        self.set_schema_from_combobox()
        self.add_button.clicked.connect(self.file_selector)
        self.validate_all_button.clicked.connect(self.validate_all_files)
        self.validate_selected_button.clicked.connect(self.validate_selected_files)

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

    def set_schema_from_combobox(self):
        self.validate_obj = validate.Validate(self.comboBox.currentText())

    def load_schema_to_combobox(self):
        count = 0
        self.list_of_schema = []
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

    def validate_files(self, index_of_files):

        for index in index_of_files:
            self.table.setItem(index, 3, QTableWidgetItem(validation_status_dict[1]))

        for index in index_of_files:
            result = self.validate_obj.start_validation(open(self.table.item(index, 2).text(),'r'))
            if result:
                self.table.setItem(index, 3, QTableWidgetItem(validation_status_dict[2]))
            else:
                self.table.setItem(index, 3, QTableWidgetItem(validation_status_dict[3]))

    def validate_all_files(self):
        self.validate_files(range(self.table.rowCount()))

    def validate_selected_files(self):
        for index in range(self.table.rowCount()):
            #if self.table.item(index, 0 )
            pass


app = QApplication(sys.argv)
main_obj = Main()
main_obj.show()
sys.exit(app.exec_())
