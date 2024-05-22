# import pandas as pd
# import kinematic as knm
# data = pd.read_excel("continuum/image_processing/data/data_XYZ.xlsx", sheet_name="frame 1")

# print(data[240][293])

# import image_processing as imp

# print(imp.calculate_real_position((0,835,0), (-710,125,0), (0,270,56.5), (-30,270,0), (-145,125,60.5), (-145,92,0)))
# print(imp.calculate_real_position((0,835,0), (-710,125,0), (0,270,42), (-7,270,0), (-145,125,42.5), (-145,113.5,0)))
# print(imp.calculate_real_position((0,835,0), (-710,125,0), (0,270,-65), (-8.5,270,0), (-145,125,-73.5), (-145,82.5,0)))

# data_real = []

# data_real.append([5, 6, 7])
# data_real.append([5, 6, 8])
# data_real.append([5, 6, 8])
# data_real.append([5, 6, 8])

# print(data_real)

# data = pd.DataFrame(data_real)

# writer = pd.ExcelWriter("continuum/image_processing/data/data1.xlsx")
# data.to_excel(writer, sheet_name="data", index=False, columns=None, startcol=4)

# writer.close()
# import numpy as np
# aaa = np.load("continuum/image_processing/data/trajectory/10_85_-5_50.npy")

# print(aaa)


# Dữ liệu vị trí
# data = pd.read_excel("C:/Users/DELL/Desktop/python/QT designer/continuum/image_processing/data/FK/data.xlsx")
# n = len(data)

# XX = [25, -10, -3]
# YY = [13, -9, 30]
# ZZ = [100, 82, 80]
# l = []
# aa = 0
# for i in range(n):
#     if abs(XX[aa] - data["X"][i]) < 1 and abs(YY[aa] - data["Y"][i]) < 1 and abs(ZZ[aa] - data["Z"][i]) < 1:
#         l.append(data["L1"][i])
#         l.append(data["L2"][i])
#         l.append(data["L3"][i])
#         l.append(data["L4"][i])
#         break
# print(l)
# angle = knm.tendon_length_to_angle_2(l)
# print(angle)

# import math
# X = -25
# Y = -15
# Z = 102.7
# # δ - delta
# if X == 0:
#     if Y == 0:
#         delta = 0
#     elif Y > 0:
#         delta = math.pi/2
#     else:
#         delta = -math.pi/2
# elif X > 0:
#     if Y >= 0:
#         delta = math.atan(Y/X)
#     else:
#         delta = 2*math.pi + math.atan(Y/X)
# elif X < 0:
#     delta = math.atan(Y/X) + math.pi

# # print(delta*180/math.pi)

# theta = math.atan(math.sqrt(X**2 + Y**2) / Z)
# # print(2*temp*180/math.pi)

# l=100
# r=8.5
# l1 = l - r*theta*math.cos(delta)
# l2 = l - r*theta*math.cos(math.pi/2 - delta)
# l3 = l + r*theta*math.cos(delta)
# l4 = l - r*theta*math.cos(math.pi/2 + delta)

# print(l1, l2, l3, l4)
# k_q, l_q, phi_q = knm.cal_intermediate_params([l1, l2, l3, l4], r, 8)
# print(knm.FK(k_q, l_q, phi_q))

import multi_servo

multi_servo.move_by_length([111, 111, 111, 111])