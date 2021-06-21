import os


def readConfig(fileName):
   if not os.path.exists("config_"+fileName):
         return ["","","","","","","","","","","","","","","","",""]
   with open("config_"+fileName, 'r') as file:
      data=[]
      for line in file:
         line=line.replace("\n","")
         if not line=="\n":
            data.append(line)
      return data


def saveConfig(fileName,data):
   with open("config_"+fileName, 'w') as file:
      
      for item in data:
         item=str(item)
         line=item.replace("\n","")
         if not item=="\n":
            file.write(str(item)+"\n")