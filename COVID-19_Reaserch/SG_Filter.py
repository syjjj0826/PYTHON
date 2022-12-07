import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from scipy.signal import savgol_filter


def sg_filter(L):
    global sg_result_list
    for i in range(len(L)):
        pre_list = np.array(L)
        np.set_printoptions(precision=8)
        sg_result = savgol_filter(pre_list, 7,3)
        sg_result_list = sg_result.tolist()
    return sg_result_list


if __name__ == "__main__":
    file = r"F:\Nighttime_Light\EX\Paper\移动数据\Google\TX_state.csv"
    data = pd.DataFrame(pd.read_csv(file))
    x = data["date"].to_list()
    y = data["parks_percent_change_from_baseline"].to_list()
    # plt.plot(x,y,color = "black")
    # yy = sg_filter(y)
    # plt.plot(x,yy,color = "red")
    RE = [data["date"].to_list()]
    for i in data.columns.to_list()[1:]:
        y = data[i].to_list()
        yy = sg_filter(y)
        RE.append(yy)
    df = pd.DataFrame(RE).T
    # print(df)
    df.columns = data.columns.to_list()
    df.to_excel(r"F:\Nighttime_Light\EX\Paper\移动数据\Google\sg_TX_state.xls")
    # plt.show()

