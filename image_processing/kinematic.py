import numpy as np
import math

### Thông số chiều dài dây ban đầu
l = np.array([0, 0, 0, 0])

# Khoảng cách từ tâm đĩa tới lỗ luồn dây - mm
r = 8.5

# Số lượng phân đoạn
n = 8

### Ma trận chuyển đổi đồng nhất
def homogenous_mtx(k_q, l_q, phi_q):
    T = [[0] * 4 for _ in range(4)]

    # column 1
    T[0][0] = pow(math.cos(phi_q),2) * (math.cos(k_q*l_q)-1) + 1
    T[1][0] = math.sin(phi_q) * math.cos(phi_q) * (math.cos(k_q*l_q) - 1)
    T[2][0] = -math.cos(phi_q) * math.sin(k_q*l_q)
    T[3][0] = 0

    # column 2
    T[0][1] = math.sin(phi_q) * math.cos(phi_q) * (math.cos(k_q*l_q) - 1)
    T[1][1] = pow(math.cos(phi_q),2) * (math.cos(k_q*l_q)-1) + math.cos(k_q*l_q)
    T[2][1] = -math.sin(phi_q) * math.sin(k_q*l_q)
    T[3][1] = 0

    # column 3
    T[0][2] = math.cos(phi_q) * math.sin(k_q*l_q)
    T[1][2] = math.sin(phi_q) * math.sin(k_q*l_q)
    T[2][2] = math.cos(k_q*l_q)
    T[3][2] = 0

    # column 4
    T[0][3] = math.cos(phi_q) * (1 - math.cos(k_q*l_q)) / k_q
    T[1][3] = math.sin(phi_q) * (1 - math.cos(k_q*l_q)) / k_q
    T[2][3] = math.sin(k_q*l_q) / k_q
    T[3][3] = 1

    return np.array(T)

### Các tham số trung gian
def cal_intermediate_params(l, r, n):
    if l[0] == l[1] and l[1] == l[2] and l[2] == l[3]:
        return 0, l[0], 0
    if l[3]-l[1] == 0:
        l[3] += 0.1
    if l[2]-l[0] == 0:
        l[2] += 0.1
        
    # Độ cong của cung
    if l[1] < l[3]:
        if l[1] < l[0]:
            k_q = (l[0]-3*l[1]+l[2]+l[3]) * math.sqrt(pow(l[3]-l[1],2)+pow(l[2]-l[0],2)) / (r*(l[0]+l[1]+l[2]+l[3])*(l[3]-l[1]))
        else:
            if l[1] > l[0]:
                k_q = (l[1]-3*l[0]+l[2]+l[3]) * math.sqrt(pow(l[3]-l[1],2)+pow(l[2]-l[0],2)) / (r*(l[0]+l[1]+l[2]+l[3])*(l[2]-l[0]))
    else:
        if l[1] > l[3]:
            if l[3] < l[2]:
                k_q = (l[0]-3*l[3]+l[2]+l[1]) * math.sqrt(pow(l[3]-l[1],2)+pow(l[2]-l[0],2)) / (r*(l[0]+l[1]+l[2]+l[3])*(l[1]-l[3]))
            else:
                if l[3] > l[2]:
                    k_q = (l[1]-3*l[2]+l[0]+l[3]) * math.sqrt(pow(l[3]-l[1],2)+pow(l[2]-l[0],2)) / (r*(l[0]+l[1]+l[2]+l[3])*(l[0]-l[2]))

    # Chiều dài cung
    aa = k_q * (l[0]+l[1]+l[2]+l[3]) / (8*n)
    # print(aa)
    if aa < -1 or aa > 1:
        return 0, 0, 0
    l_q = (2*n / k_q) * math.asin(aa)
    # print(l_q)

    # Hướng cong
    if l[0] < l[2]:
        phi_q = math.atan((l[3]-l[1]) / (l[2]-l[0]))
    else:
        phi_q = math.atan((l[3]-l[1]) / (l[2]-l[0])) + math.pi
    # print(phi_q)

    return k_q, l_q, phi_q

def rotation_matrix(axis = "x", theta = 0):
    R = [[0] * 4 for _ in range(4)]

    if axis == "x":
        R[0][0] = 1
        R[1][0] = 0
        R[2][0] = 0

        R[0][1] = 0
        R[1][1] = math.cos(theta)
        R[2][1] = math.sin(theta)

        R[0][2] = 0
        R[1][2] = -math.sin(theta)
        R[2][2] = math.cos(theta)
    else:
        if axis == "y":
            R[0][0] = math.cos(theta)
            R[1][0] = 0
            R[2][0] = -math.sin(theta)

            R[0][1] = 0
            R[1][1] = 1
            R[2][1] = 0

            R[0][2] = math.sin(theta)
            R[1][2] = 0
            R[2][2] = math.cos(theta)
        else:
            R[0][0] = math.cos(theta)
            R[1][0] = math.sin(theta)
            R[2][0] = 0

            R[0][1] = -math.sin(theta)
            R[1][1] = math.cos(theta)
            R[2][1] = 0

            R[0][2] = 0
            R[1][2] = 0
            R[2][2] = 1


    R[3][0] = R[3][1] = R[3][2] = R[0][3] = R[1][3] = R[2][3]
    R[3][3] = 1

    return np.array(R)

def tendon_length_to_angle_2(length):
    # 130 degree - 111 mm
    # 100 degree - 105 mm
    # 70 degree - 98 mm
    # 40 degree - 91 mm
    # 10 degree - 85 mm
    # -20 degree - 79 mm
    # -50 degree - 72 mm
    res = []
    for i in range(4):
        res.append(round((length[i] - 72) / (111 - 72) * 180 - 50, 1))
    return res

def tendon_length_to_angle_1(length):
    # 0 degree - 134 mm
    # 150 degree - 98 mm
    res = []
    for i in range(4):
        res.append(int(150.0 - (length[i] - 98) / (134 - 98) * 150))
    return res

def FK(k_q, l_q, phi_q):
    X = (math.cos(phi_q) - 0.5*math.cos(k_q*l_q+phi_q) - 0.5*math.cos(k_q*l_q-phi_q)) / k_q
    Y = (math.sin(phi_q) - 0.5*math.sin(k_q*l_q+phi_q) + 0.5*math.sin(k_q*l_q-phi_q)) / k_q
    Z = math.sin(k_q*l_q) / k_q

    return X, Y, Z

# l = np.array([122, 125, 124.9, 122.1])
# k_q, l_q, phi_q = cal_intermediate_params(l, r, n)
# print(k_q, l_q, phi_q*180/math.pi)
# print(tendon_length_to_angle_1(l))

# T = np.matmul(homogenous_mtx(k_q, l_q, phi_q), rotation_matrix("z", math.pi/4))
# T = homogenous_mtx(k_q, l_q, phi_q)
# res = np.matmul(T, np.array([0,0,0,1]))
# print(f"X = {res[0]:3.4f}, Y = {res[1]:3.4f}, Z = {res[2]:3.4f}")

# print(FK(k_q, l_q, phi_q))

# angle = np.arange(115.1, 125, 0.1)
# for i in angle:
#     k_q, l_q, phi_q = cal_intermediate_params(np.array([i, 115, 125, 125]), r, n)
#     print(FK(k_q, l_q, phi_q))