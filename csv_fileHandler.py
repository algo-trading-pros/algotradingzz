import os
from csv import DictWriter



class File:
   def __init__(self,name,column_name):
      self.filename=name
      self.column_name=column_name
      print("loaded ",self.filename)
      with open(self.filename, 'a+') as f_object1:
         filesize = os.path.getsize(self.filename)
         if filesize==0:
            dictwriter_object = DictWriter(f_object1, fieldnames=self.column_name)
            dictwriter_object.writeheader()

   def addRow(self,row):
      
      with open(self.filename, 'a') as f_object:
         dictwriter_object = DictWriter(f_object, fieldnames=self.column_name)
         dictwriter_object.writerow(row)

         f_object.close()


