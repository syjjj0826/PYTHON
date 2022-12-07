import os
import re
import sys



def renameall():
    fileList = os.listdir(r"C:\Users\Administrator\Desktop\夜光导出数据")  # 待修改文件夹

    currentpath = os.getcwd()  # 得到进程当前工作目录
    os.chdir(r"C:\Users\Administrator\Desktop\夜光导出数据")  # 将当前工作目录修改为待修改文件夹的位置
    num = 1992  # 名称变量(重命名可从1开始)
    for fileName in fileList:  # 遍历文件夹中所有文件
        pat = ".dbf"  # 匹配文件名正则表达式(用来识别修改文件)
        pattern = re.findall(pat, fileName)  # 进行匹配

        os.rename(fileName, ("NL"+str(num)+"Output"+pattern[0]))  # 文件重新命名
        num = num + 1  # 改变编号，继续下一项
    os.chdir(currentpath)  # 改回程序运行前的工作目录
    sys.stdin.flush()  # 刷新

renameall()
