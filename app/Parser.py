from app.bank.test1 import Bank
# from bank.parser_bmo import ParseRBC
import importlib

xml_path = 'Study_App4July2018.xml'
parsebank_obj = Bank()
# data = obj.parse(xml_path)
bank_name, page_tag = parsebank_obj.parse(xml_path)


module_path = 'app.' + 'bank.' + 'parser_bmo'
module = importlib.import_module(module_path)
bank_name1 = 'ParseRBC'
my_class = getattr(module, bank_name1)
bank_object = my_class()
# bank_object = eval('Parse' + bank_name)()
data = bank_object.parse(page_tag)
print(data)
