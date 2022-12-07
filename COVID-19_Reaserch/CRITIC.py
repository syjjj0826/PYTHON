import numpy as np
import pandas as pd


# 正向化
def max_minNormalization(x):
    x = (x - np.min(x)) / (np.max(x) - np.min(x))
    return x

def critic(X):
    # 无量纲处理
    Z = []
    for i in range(len(X)):
        xx = max_minNormalization(X[i])
        Z.append(xx)
    data = pd.DataFrame(Z).T
    # print(data)

    # 指标变异性计算
    S = []
    for i in range(data.shape[1]):
        std = np.std(np.array(data[i].to_list()),ddof = 1)
        S.append(std)
    print("指标变异性:")
    print(S)

    # 指标冲突性
    corr = data.corr()
    print(corr)
    R = []
    for i in range(corr.shape[0]):
        r_list = corr.iloc[i]
        A = []
        for j in range(len(r_list)):
            a = 1 - r_list[j]
            A.append(a)
        R.append(np.sum(A))
    print("指标冲突性:")
    print(R)

    # 信息量计算
    C = []
    for i in range(len(R)):
        s = S[i]
        r = R[i]
        c = s * r
        C.append(c)
    print("信息量：")
    print(C)

    # 最终客观权重
    W = []
    for i in range(len(C)):
        w = C[i] / np.sum(C)
        W.append(w)
    print("最终权重：")
    print(W)


if __name__ == '__main__':
    file = r"F:\Nighttime_Light\EX\Exper20210925\critic_5\NY_Google.csv"
    X = []
    df = pd.DataFrame(pd.read_csv(file))
    for i in range(len(df["class"].to_list())):
        record = df.iloc[i].to_list()[1:]
        X.append(record)
    d = pd.DataFrame(X)
    d = d.T
    d.columns = df["class"]
    print(d)


    critic(X)