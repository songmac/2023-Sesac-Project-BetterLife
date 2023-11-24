import pandas as pd
import sys
sys.path.append("D:/2023-Sesac-Project-BetterLife/module/")
import csvfile

csvPath = "./data/sample_data/"
savePath = "./data/"
fileName = "id_1 (7)"

csvdata = csvfile.getCSVFile(csvPath, fileName)
print(csvdata)
#csvfile.merge_csv(csvPath, savePath,"merge_file")
