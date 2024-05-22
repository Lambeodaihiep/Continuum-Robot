import pandas as pd
import random
import numpy as np
import kinematic as knm

# Khoảng cách từ tâm đĩa tới lỗ luồn dây - mm
r = 8.5

# Số lượng phân đoạn
n = 8

data = np.array([[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]])

for i in range(200000):
    l = []
    for i in range(4):
        l.append(round(random.uniform(72, 111), 1))
    k_q, l_q, phi_q = knm.cal_intermediate_params(l, r, n)
    if k_q == 0:
        continue
    X, Y, Z = knm.FK(k_q, l_q, phi_q)
    if Z < 65:
        continue
    l.append(X)
    l.append(Y)
    l.append(Z)
    data = np.insert(data, 1, l, axis=0)

df1 = pd.DataFrame(data)
writer = pd.ExcelWriter("C:/Users/DELL/Desktop/python/QT designer/continuum/image_processing/data/FK/data.xlsx")

df1.to_excel(writer, sheet_name="frame 1", index=None)
writer.close()