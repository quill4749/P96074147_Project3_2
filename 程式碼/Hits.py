import numpy as np
import sys
import time
import csv


FILE_INPUT_NAME = "C:/Users/P96074147/Desktop/P96074147_Project3/project3dataset/graph_8.txt"
ERROR_TOLERANCE = 0.1
OUTPUT_HITS_RESULT_NAME = "C:/Users/P96074147/Desktop/P96074147_Project3/output/HITS_RESULT.csv"

pages_arr = [] #所有頁面
file_list = [] #輸入資料

inp = open(FILE_INPUT_NAME) #開始讀檔
for row in inp.readlines():
    source, target = row.split(',')
    file_list.append([int(source),int(target)])
    if int(source) not in pages_arr:
        pages_arr.append(int(source)) #讀取所有不重複的頁面
    if int(target) not in pages_arr:
        pages_arr.append(int(target))
inp.close()

page_num = max(pages_arr) #頁面最大數量
graph = np.zeros((page_num,page_num)) 
for row in file_list: 
    graph[row[0]-1][row[1]-1] = 1
    
hub = np.full((page_num),1.0) #初始化Hub
aut = np.full((page_num),1.0) #初始化Authority
error = sys.maxsize
start_time = time.time()
while error > ERROR_TOLERANCE:
    new_hub = np.full((page_num),0.0)
    new_aut = np.full((page_num),0.0)
    max_hub = 0.0
    max_aut = 0.0
    error = 0.0
    
    for x in range(0,page_num): #計算hub&authority的更新數值
        for y in range(0,page_num):
            if graph[x][y] == 1:
                new_hub[x] += aut[y]
                new_aut[y] += hub[x]            

    for z in range(0,page_num): #找到最大hub&authority
        if new_hub[z] > max_hub:
            max_hub = new_hub[z]
        if new_aut[z] > max_aut:
            max_aut = new_aut[z]
    
    for s in range(0,page_num): #正規化
        new_hub[s] = new_hub[s]/max_hub
        new_aut[s] = new_aut[s]/max_aut
        error += (abs(new_hub[s] - hub[s])+abs(new_aut[s] - aut[s]))
        hub[s] = new_hub[s]
        aut[s] = new_aut[s]
        print(str(hub[s])+" "+str(aut[s]))

print("執行時間 %s 秒" % (time.time() - start_time))

output_data = [] #儲存結果
for i in range(0,page_num):
    output_data.append([i+1,aut[i],hub[i]])
out_put_file = open(OUTPUT_HITS_RESULT_NAME, 'w', newline='')
with out_put_file:
    writer = csv.writer(out_put_file)
    writer.writerows(output_data)

