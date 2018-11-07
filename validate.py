from lxml import etree

class Validate:
    def __init__(self, file_name):
        xmlschema_doc = etree.parse("schemas/"+file_name+".xsd")
        self.xmlschema = etree.XMLSchema(xmlschema_doc)

    def start_validation(self, file):
        xml_doc = etree.parse(file)
        result = self.xmlschema.validate(xml_doc)
        return result
