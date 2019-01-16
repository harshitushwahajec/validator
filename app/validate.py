from lxml import etree
import os
import logging

class Validate:
    def __init__(self, file_name,execution_id):
        self.execution_id = execution_id
        self.app_logger = logging.getLogger('root')
        self.exec_logger = logging.getLogger()

        formatter =  logging.Formatter('{} - %(asctime)s - %(levelname)s - %(message)s'.format(execution_id))
        exec_log_file = os.path.join('.','Execution Logs','exec_'+str(execution_id) + '.log')

        f_handler = logging.FileHandler(exec_log_file)
        f_handler.setFormatter(formatter)

        self.exec_logger.addHandler(f_handler)

        self.app_logger.debug('Testing from  Validate file')

        xmlschema_doc = etree.parse(os.path.join('schemas',file_name+'.xsd'))
        self.xmlschema = etree.XMLSchema(xmlschema_doc)

    def start_validation(self, file):

        # result = self.xmlschema.validate(xml_doc)
        # return result
        result = True
        try:
            xml_doc = etree.parse(file)
            self.xmlschema.assertValid(xml_doc)
        except etree.Error as xml_errors:
            self.exec_logger.error(xml_errors.error_log)
            result = False
        except Exception as err:
            logging.error(err.error_log)
            result = False
        finally:
            return result

    def evict_old_error_logs(self):
        list = os.listdir('Execution Logs')  # dir is your directory path
        number_files = len(list)
        logging.debug(number_files)
        if number_files>50:
            excess = number_files-50
