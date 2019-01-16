from PyQt4.QtCore import *
from PyQt4.QtGui import *
from app import user_interface, validate
import sys
import os
import json
import logging
import logging.config
import webbrowser

path_log_config = os.path.join('config', 'app_logging.json')

if os.path.exists(path_log_config):
    with open(path_log_config, 'rt') as f:
        log_config = json.load(f)
    logging.config.dictConfig(log_config)
    app_logger = logging.getLogger()
    # app_logger.config.dictConfig(log_config)
    app_logger.debug('Log Configurations loaded')
else:
    logging.basicConfig(level=logging.DEBUG)
    logging.debug('Log Configurations NOT loaded')

app_logger.info('************** Application started **************')

# loading config file
with open(os.path.join('config', 'properties.json'), 'r+') as f:
    app_config = json.load(f)

validation_status_dict = {0: app_config['VALIDATION_STATUS']['0'],
                          1: app_config['VALIDATION_STATUS']['1'],
                          2: app_config['VALIDATION_STATUS']['2'],
                          3: app_config['VALIDATION_STATUS']['3']}


class Main(QMainWindow, user_interface.Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)

        self.execution_id = app_config['LAST_EXECUTION_ID'] + 1
        app_config['LAST_EXECUTION_ID'] = self.execution_id

        self.lineEdit.setText(str(self.execution_id))

        with open(os.path.join('config', 'properties.json'), 'w+') as f:
            json.dump(app_config, f)

        self.validate_obj = None
        self.list_of_schema = []
        self.list_of_files = []
        self.load_schema_to_combobox()
        self.set_schema_from_combobox()

        self.add_button.clicked.connect(self.file_selector)
        self.validate_all_button.clicked.connect(self.validate_all_files)
        self.validate_selected_button.clicked.connect(self.validate_selected_files)
        self.remove_button.clicked.connect(self.remove_selected)
        self.clea_button.clicked.connect(self.clear_table)
        self.view_logs_button.clicked.connect(self.view_log_file)
        self.reload_schemas_button.clicked.connect(self.load_schema_to_combobox)
        self.comboBox.currentIndexChanged.connect(self.set_schema_from_combobox)

        self.table.resizeColumnsToContents()
        self.table.setSortingEnabled(True)

    def file_selector(self):
        list_of_files = QFileDialog.getOpenFileNames(self, caption="Select Files", directory=".",
                                                     filter='All Files (*.*)')
        list_of_files = list(set(list_of_files))

        for file in list_of_files:
            if file not in self.list_of_files:
                row_num = self.table.rowCount()
                self.table.insertRow(row_num)

                chk_box_item = QTableWidgetItem()
                chk_box_item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                chk_box_item.setCheckState(Qt.Unchecked)

                self.list_of_files += [file]

                self.table.setItem(row_num, 0, chk_box_item)
                self.table.setItem(row_num, 1, QTableWidgetItem(file.split(os.sep)[-1]))
                self.table.setItem(row_num, 2, QTableWidgetItem(validation_status_dict[0]))
            # else:
            #     self.set_status('Duplicate files removed.')

    def set_schema_from_combobox(self):
        self.validate_obj = validate.Validate(self.comboBox.currentText(),self.execution_id)

    def load_schema_to_combobox(self):
        count = 0
        self.list_of_schema = []
        for file in os.listdir("schemas"):
            if file.endswith(".xsd"):
                self.list_of_schema+=[file.split('.')[-2]]
                if count == 0 or count == 1: count += 1

        self.comboBox.clear()
        for schema in self.list_of_schema:
            self.comboBox.addItem(schema)

        if count == 1:
            self.comboBox.setEnabled(False)
        elif count == 2:
            self.comboBox.setEnabled(True)
        else:
            print('No Schema found')

    def validate_files(self, index_of_files):

        for index in index_of_files:
            self.table.setItem(index, 2, QTableWidgetItem(validation_status_dict[1]))

        for index in index_of_files:
            result = self.validate_obj.start_validation(open(self.list_of_files[index], 'r'))
            if result:
                self.table.setItem(index, 2, QTableWidgetItem(validation_status_dict[2]))
                # self.table.row(index).
            else:
                self.table.setItem(index, 2, QTableWidgetItem(validation_status_dict[3]))
        self.table.sortByColumn(2,1)

    def validate_all_files(self):
        self.show_progress_dialog(self.table.rowCount())
        self.validate_files(range(self.table.rowCount()))
        for index in range(self.table.rowCount()):
            self.table.item(index, 0).setCheckState(Qt.Checked)

    def validate_selected_files(self):
        list_of_indices = []
        for index in range(self.table.rowCount()):
            if self.table.item(index, 0).checkState() == Qt.Checked:
                list_of_indices += [index]
        self.validate_files(list_of_indices)

    def set_status(self, msg=''):
        self.statusbar.showMessage(msg)

    def remove_selected(self):
        list_of_indices = []
        for index in range(self.table.rowCount()):
            if self.table.item(index, 0).checkState() == Qt.Checked:
                list_of_indices += [index]

        for index in list_of_indices[::-1]:
            self.list_of_files.remove(self.table.item(index, 1).text())
            self.table.removeRow(index)

    def clear_table(self):
        self.list_of_files = []
        self.table.setRowCount(0)

    def show_progress_dialog(self, max_size):
        self.progress_dialog = QProgressDialog('Test', 'Ok', 0, max_size, self)
        #self.progress_dialog.
        self.progress_dialog.show()

    def view_log_file(self):
        webbrowser.open(os.getcwd() + os.path.join('.','Execution Logs','exec_'+str(self.execution_id)+'.log'))


app = QApplication(sys.argv)
main_obj = Main()
main_obj.show()
app.exec_()
app_logger.info('************** Application terminated  **************')
sys.exit()
