from lxml import etree

class Validate:
    def __init__(self, file_name):
        xmlschema_doc = etree.parse("schemas/"+file_name)
        self.xmlschema = etree.XMLSchema(xmlschema_doc)
