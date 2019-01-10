import numpy as np
import sys
import random
import time
import csv


FILE_INPUT_NAME = "C:/Users/P96074147/Desktop/P96074147_Project3/project3dataset/graph_8.txt"
ERROR_TOLERANCE = 0.1
OUTPUT_PAGERANK_RESULT_NAME = "C:/Users/P96074147/Desktop/P96074147_Project3/output/PAGERANK_RESULT.csv"

pages_arr = [] #所有頁面
file_list = [] #輸入資料

inp = open(FILE_INPUT_NAME) #開始讀檔
for row in inp.readlines():
    source, target = row.split(',')
    file_list.append([int(source),int(target)])
    if int(source) not in pages_arr:
        pages_arr.append(int(source)) #讀入所有不重複頁面
    if int(target) not in pages_arr:
        pages_arr.append(int(target))
inp.close() 

page_num = max(pages_arr) #頁面最大數量
graph = np.zeros((page_num,page_num)) 
for row in file_list:
    graph[row[0]-1][row[1]-1] = 1

pr_vector = np.full((page_num),1.0) #每個node的PR初始化

temp1, temp2 = np.unique(graph, return_counts=True) #計算連結數量
link_num = temp2[1]

for i in range(0,page_num): #平分每個連結
    for j in range(0,page_num):
        if graph[i][j] == 1.0:
            graph[i][j] = graph[i][j] / link_num
            
graph = graph.T #轉置

page_ranks_i = np.full((page_num,page_num),0.0)
page_ranks_j = np.full((page_num,page_num),0.0)
start_time = time.time()
for i in range(0,page_num): #套用公式
    for j in range(0,page_num):
        DAMP_FACTOR =  0.15 #調整阻尼係數(0.1~0.15)
        page_ranks_j[i][j] = (1.0-DAMP_FACTOR)/page_num
        page_ranks_i[i][j] = (DAMP_FACTOR * graph[i][j]) + page_ranks_j[i][j]
        
error = sys.maxsize
new_pr_vector = np.full((page_num),1.0)

while error > ERROR_TOLERANCE: #疊代
    error = 0.0
    for i in range(0,page_num):
        temp = 0.0
        for j in range(0,page_num):
            temp += page_ranks_i[i][j] * pr_vector[j]
        new_pr_vector[i] = temp
        
    for i in range(0,page_num):
        error += abs(new_pr_vector[i] - pr_vector[i])
        pr_vector[i] = new_pr_vector[i]
        print(pr_vector[i])

print("執行時間 %s 秒" % (time.time() - start_time))

output_data = [] #儲存結果
for i in range(0,page_num):
    output_data.append([i+1,pr_vector[i]])
out_put_file = open(OUTPUT_PAGERANK_RESULT_NAME, 'w', newline='')
with out_put_file:
    writer = csv.writer(out_put_file)
    writer.writerows(output_data)
