import csv
import itertools
import numpy as np
np.set_printoptions(threshold=np.inf)

FILE_NAME_TO_CONVERT = "C:/Users/P96074147/Desktop/P96074147_Project3/project3dataset/IBMdataset.csv"
FILE_NAME_TO_SAVE_TXT = "C:/Users/P96074147/Desktop/P96074147_Project3/project3dataset/graph_7.txt"
old_ts_id = 10
transaction = []
out_data = []
row_len = 2

def unique_rows(a):
    a = np.ascontiguousarray(a)
    unique_a = np.unique(a.view([('', a.dtype)]*a.shape[1]))
    return unique_a.view(a.dtype).reshape((unique_a.shape[0], a.shape[1]))

with open(FILE_NAME_TO_CONVERT, newline='') as myFile:  
    reader = csv.reader(myFile)
    for row in reader:
        if(old_ts_id != int(row[0])) or (len(row) != row_len):
            for a, b in itertools.product(transaction, transaction): #笛卡兒乘積
                if a != b: #避免連到自己
                    out_data.append([a,b])
            transaction.clear()
            old_ts_id = int(row[0])
        else:
            transaction.append(int(row[1]))

new_arr = np.array(out_data)
out_np_data = unique_rows(new_arr) #刪除重複
out_put_file = open(FILE_NAME_TO_SAVE_TXT, 'w') #儲存結果
with out_put_file as opf:
    for row in out_np_data:
        print(str(row[0])+','+str(row[1]),file=opf)
