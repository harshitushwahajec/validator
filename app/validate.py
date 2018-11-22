from lxml import etree
import os


class Validate:
    def __init__(self, file_name):
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
            print(xml_errors.error_log)
            result = False
        except Exception as err:
            print(err.error_log)
            result = False
        finally:
            return result

