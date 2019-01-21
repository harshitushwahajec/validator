from lxml import etree, objectify
import xmltodict
import xml.etree.ElementTree as ET

dict_of_attr = {'id':None, 'name':None, 'age':None, 'city':None}
# with open('Students.xml') as f:
#     xml = f.read()

tree = ET.parse('Students.xml')

root = tree.getroot()

dynamic_obj = type('dynamic_obj', (object,), dict_of_attr)

for temp in root.iter('student'):
    new_obj = dynamic_obj()
    #dynamic_obj.__dict__.items()
    for attr in dict_of_attr:
        setattr(new_obj, attr, [i for i in temp.iter(attr)][0].text if [i for i in temp.iter(attr)][0]!=None else None)
        #print(temp.find('id'))
    for attr1 in dict_of_attr:
        print(getattr(new_obj, attr1))
