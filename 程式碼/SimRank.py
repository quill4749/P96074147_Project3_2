import itertools
import numpy as np
import time
import networkx as nx
import csv
start_time = time.time()

FILE_INPUT_NAME = "C:/Users/P96074147/Desktop/P96074147_Project3/project3dataset/graph_8.txt"
LOOP_TIMES = 40
PARAMETER_C = 0.1
OUTPUT_SIMRANK_RESULT_NAME = "C:/Users/P96074147/Desktop/P96074147_Project3/output/SIMRANK_RESULT.csv"

pages_arr = [] #所有頁面
file_list = [] #輸入資料
graph = nx.DiGraph()

inp = open(FILE_INPUT_NAME) #開始讀檔
for row in inp.readlines():
    source, target = row.split(',')
    file_list.append([int(source),int(target)])
    if int(source) not in pages_arr:
        pages_arr.append(int(source)) #讀入所有不重複頁面
    if int(target) not in pages_arr:
        pages_arr.append(int(target))
inp.close() 

for row in file_list:
    graph.add_edge(int(row[0]),int(row[1]))

nodes = list(graph.nodes())
nodes_i = {k: v for(k, v) in [(nodes[i], i) for i in range(0, len(nodes))]}
sim_prev = np.zeros(len(nodes))
sim = np.identity(len(nodes))
print(sim)

for loop in range(0,LOOP_TIMES): #疊代迴圈
    sim_prev = np.copy(sim) 
    for u, v in itertools.product(nodes, nodes): #笛卡兒乘積
        if u is v: #跳過自己
            continue
        u_ns, v_ns = graph.predecessors(u), graph.predecessors(v)
        if len(u_ns) == 0 or len(v_ns) == 0: #如果其中有個沒被連到，則此點相似度設為0
            sim[nodes_i[u]][nodes_i[v]] = 0
        else:                    
            s_uv = sum([sim_prev[nodes_i[u_n]][nodes_i[v_n]] for u_n, v_n in itertools.product(u_ns, v_ns)]) #套入公式
            sim[nodes_i[u]][nodes_i[v]] = (PARAMETER_C * s_uv) / (len(u_ns) * len(v_ns))

print("執行時間 %s 秒" % (time.time() - start_time))

output_data = [] #儲存結果
for i in range(0,len(nodes)):
    output_data.append(sim[i])
out_put_file = open(OUTPUT_SIMRANK_RESULT_NAME, 'w', newline='')
with out_put_file:
    writer = csv.writer(out_put_file)
    writer.writerows(output_data)
