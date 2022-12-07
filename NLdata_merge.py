import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator
from dbfread import DBF
import xlwt
import xlrd


def dt_xls(dbf_filename, out_path):  # dbf_filename为文件的basename，out_path为储存指定目录
    if os.path.splitext(dbf_filename)[1] == ".dbf":  # 筛选dbf文件
        xls_filename = os.path.basename(dbf_filename).replace("dbf", "xls")  # 修改文件名
        table = DBF(dbf_filename, encoding="gbk")
        all_sheet = []
        book = xlwt.Workbook()  # 新建一个excel
        sheet = book.add_sheet("all_sheet")  # 添加一个sheet页
        row = 0  # 控制行数
        write_row = 0
        sheet_list = []
        for record in table:
            col = 0
            if all_sheet is not None:  # 控制只读取字段名一次
                sheet_dict = record.keys()
                sheet_list = list(sheet_dict)  # 将keys转化为列表进行操作
                all_sheet = sheet_list
            if write_row == 0:  # 控制只将字段名写入一次
                col = 0
                for i in range(len(sheet_list)):
                    sheet.write(row, col, sheet_list[i])
                    col += 1
                col = 0
                row += 1
                write_row += 1
            for field in record:
                sheet.write(row, col, record[field])
                col += 1
            row += 1
        out_file = os.path.join(out_path, xls_filename)  # 输出文件名
        book.save(out_file)  # 保存到指定目录下的指定文件
        print("Success: 【" + dbf_filename + "】转换成功！")
    else:
        print("Error：【" + dbf_filename + "】不是.dbf文件，请确认文件路径，重新输入！")


def ntl_merge(folderpath, output_path):
    #  表头
    filenames = os.listdir(folderpath)
    filedirs = []
    for f in filenames:
        if os.path.splitext(f)[1] == ".xls":
            filedirs.append(f)
        else:
            pass
    first_path = os.path.join(folderpath, filedirs[0])
    print(first_path)
    data = xlrd.open_workbook(first_path, encoding_override="utf-8")
    table = data.sheets()[0]  # 选定表
    nrows = table.nrows  # 获取行号
    title = table.row_values(0)  # 表头行
    print("字段：\n", title)
    ID = []
    for i in range(1, nrows):  # 第0行为表头
        all_data = table.row_values(i)  # 循环输出excel表中每一行，即所有数据
        result = all_data[0]  # 单纯读取批量处理的文件的第一列属性，可以简化
        ID.append(str(result))
    print("第一列：", ID)

    def NLread(xls_filepath):
        data = xlrd.open_workbook(xls_filepath, encoding_override="utf-8")
        table = data.sheets()[0]
        nrows = table.nrows
        figure = []
        for i in range(1, nrows):  # 第0行为表头
            all_data = table.row_values(i)  # 循环输出excel表中每一行，即所有数据
            result = all_data[-3]  # 取出表中指定字段数值，-1可以改成其他需要的字段位置
            figure.append(result)
        NL_data.append(figure)

    l = len(filedirs)
    NL_data = []
    month = []
    for num in range(l):
        xls_filename = os.path.join(folderpath, filedirs[num])  # 文件路径消除转义符（加不了r）
        print("\n", xls_filename)
        NLread(xls_filename)
        num += 1
        # date = "M" + str(num).rjust(2, "0")
        date = os.path.basename(xls_filename)
        date = os.path.splitext(date)[0].replace("result_","")[-6:]
        month.append(date)
    FRAME = pd.DataFrame(NL_data)  # 行列转置换cloums名称
    FRAME.columns = ID
    FRAME = FRAME.T
    FRAME.columns = month
    FRAME.to_excel(output_path)


if __name__ == "__main__":

    filepath = r"G:\NIGHTTIME_LIGHT\NTL\G_Dal\tab"
    out = r"G:\NIGHTTIME_LIGHT\NTL\G_Dal\tab"
    for file in os.listdir(filepath):
        dt_xls(os.path.join(filepath, file), filepath)
    outpath = os.path.join(out, "ANTL_dal.xls")
    ntl_merge(filepath, outpath)