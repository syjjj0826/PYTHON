# #-*-coding:utf-8-*-

# import glob
# import sys
# import os
# import pandas as pd

# # i=0
# # csv_list=[]
# # for root, dirs, files in os.walk("E:/资料/研究生/Python/爬虫/POI/poi-master/poi-master/gaode/data/"):
# #     for file_name in files:

# #         (filename, extension) = os.path.splitext(file_name)
        
# #         if (extension == '.csv'):             
# #             pathname=os.path.join(root,file_name) 
# #             father_path=os.path.abspath(os.path.dirname(pathname)+os.path.sep+".")
# #             print(pathname)  
# #             #print(father_path) 
# #             csv_list.append(pathname)
# # print('共发现%s个CSV文件'% len(csv_list))
# # print('正在处理......')
# # for i in csv_list: #循环读取同文件夹下的csv文件
# #     fr = open(i,'rb').read()
# #     with open('resultPOI.csv','ab') as f: #将结果保存为result.csv
# #         f.write(fr)
# # print('合并完毕！')            

# import csv
# i=1
# input1 = open(r'E:/资料/研究生/Python/爬虫/POI/poi-master/poi-master/gaode/resultPOI.csv', 'rb')
# output = open(r'E:/资料/研究生/Python/爬虫/POI/poi-master/poi-master/gaode/resultPOI1.csv', 'wb')
# writer = csv.writer(output)
# for row in csv.reader(input1):
#     if row:
#         print("写入第"+i+"行")
#         writer.writerow(row)
#     i=i+1
# input1.close()
# output.close()


#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/3/18 21:41
# @Author  : cunyu
# @Site    : cunyu1943.github.io
# @File    : deleteBlankLines.py
# @Software: PyCharm

"""
读取存在空行的文件，删除其中的空行，并将其保存到新的文件中
"""
i=1
with open('E:/资料/研究生/Python/爬虫/POI/poi-master/poi-master/gaode/resultPOI2.txt','r',encoding = 'utf-8') as fr,open('E:/资料/研究生/Python/爬虫/POI/poi-master/poi-master/gaode/new.txt','w',encoding = 'utf-8') as fd:
        for text in fr.readlines():
            if text.split():
                print("第"+str(i)+"行写入。。。")
                fd.write(text)
                i+=1
        print('输出成功....')
