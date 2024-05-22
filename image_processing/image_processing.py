import cv2
import numpy as np
import kinematic as knm
import math

# color_dict_HSV = {'black': [[180, 255, 30], [0, 0, 0]],
#               'white': [[180, 18, 255], [0, 0, 231]],
#               'red1': [[180, 255, 255], [159, 50, 70]],
#               'red2': [[9, 255, 255], [0, 50, 70]],
#               'green': [[89, 255, 255], [36, 50, 70]],
#               'blue': [[128, 255, 255], [90, 50, 70]],
#               'yellow': [[35, 255, 255], [25, 50, 70]],
#               'purple': [[158, 255, 255], [129, 50, 70]],
#               'orange': [[24, 255, 255], [10, 50, 70]],
#               'gray': [[180, 18, 230], [0, 0, 40]]}

def find_blue(img):
    img_hsv=cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # lower mask (0-10)
    lower_red = np.array([100,20,20])
    upper_red = np.array([130,200,200])
    mask0 = cv2.inRange(img_hsv, lower_red, upper_red)

    # upper mask (170-180)
    lower_red = np.array([165,50,50])
    upper_red = np.array([180,255,255])
    mask1 = cv2.inRange(img_hsv, lower_red, upper_red)

    # join my masks
    mask = mask0+mask1

    # set my output img to zero everywhere except my mask
    output_img = img.copy()
    output_img[np.where(mask==0)] = 0

    # or your HSV image, which I *believe* is what you want
    # output_hsv = img_hsv.copy()
    # output_hsv[np.where(mask==0)] = 0

    return output_img

def find_red(img):
    img_hsv=cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # lower mask (0-10)
    lower_red = np.array([0,50,50])
    upper_red = np.array([15,255,255])
    mask0 = cv2.inRange(img_hsv, lower_red, upper_red)

    # upper mask (170-180)
    lower_red = np.array([165,50,50])
    upper_red = np.array([180,255,255])
    mask1 = cv2.inRange(img_hsv, lower_red, upper_red)

    # join my masks
    mask = mask0+mask1

    # set my output img to zero everywhere except my mask
    output_img = img.copy()
    output_img[np.where(mask==0)] = 0

    # or your HSV image, which I *believe* is what you want
    # output_hsv = img_hsv.copy()
    # output_hsv[np.where(mask==0)] = 0

    return output_img

# find contours and draw them
def find_color_position(img, blue_img, Threshold=[100, 100], minArea=100):

    gray = cv2.cvtColor(blue_img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 1)
    _, threshs = cv2.threshold(blur, Threshold[0], Threshold[1], cv2.THRESH_BINARY_INV)
    # canny = cv2.Canny(threshs, Threshold[0], Threshold[1])
    kernel = np.ones((3, 3))
    Dilate = cv2.dilate(threshs, kernel, iterations=2)
    Erode = cv2.erode(Dilate, kernel, iterations=2)

    cnts, _ = cv2.findContours(255-Erode, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in cnts:
        # cnt = (center(x, y), (width, height), angle of rotation)
        rr = cv2.minAreaRect(cnt)
        if rr[1][0] == 0 or rr[1][1] == 0 or rr[0][0] > 500 or rr[0][0] < 200 or rr[0][1] > 400 or rr[0][1] < 100:
            continue
        if rr[1][0] * rr[1][1] > minArea:
            ### Nếu muốn vẽ bounding box
            # box = cv2.boxPoints(rr)
            # box = np.int0(box)
            # cv2.drawContours(img, [box], 0, (0, 255, 0), 2)
            ### Nếu chỉ muốn vẽ vị trí tâm
            Cx = int(rr[0][0])
            Cy = int(rr[0][1])
            cv2.circle(img, (Cx,Cy), 2, (0, 255, 0), -1)

            return img, Cx, Cy
        
    return img, 0, 0

def find_red_position(img, red_img, Threshold=[100, 100], minArea=1000, data_XYZ=None, axis=""):

    gray = cv2.cvtColor(red_img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 1)
    _, threshs = cv2.threshold(blur, Threshold[0], Threshold[1], cv2.THRESH_BINARY_INV)
    # canny = cv2.Canny(threshs, Threshold[0], Threshold[1])
    kernel = np.ones((5, 5))
    Dilate = cv2.dilate(threshs, kernel, iterations=1)
    Erode = cv2.erode(Dilate, kernel, iterations=3)

    cnts, _ = cv2.findContours(255-Erode, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in cnts:
        # cnt = (center(x, y), (width, height), angle of rotation)
        rr = cv2.minAreaRect(cnt)
        if rr[1][0] == 0 or rr[1][1] == 0 or rr[0][0] > 500 or rr[0][0] < 150 or rr[0][1] > 400 or rr[0][1] < 100:
            continue
        if rr[1][0] * rr[1][1] > minArea:
            ### Nếu muốn vẽ bounding box
            # box = cv2.boxPoints(rr)
            # box = np.int0(box)
            # cv2.drawContours(img, [box], 0, (0, 255, 0), 2)
            ### Nếu chỉ muốn vẽ vị trí tâm
            Cx = int(rr[0][0])
            Cy = int(rr[0][1])
            cv2.circle(img, (Cx,Cy), 3, (0, 255, 0), -1)
            ### Hiển thị tọa độ pixel trên ảnh
            # cv2.putText(img, str(Cx) + ", " + str(Cy), (Cx,Cy-25), cv2.FONT_HERSHEY_COMPLEX, 0.6, (0,0,0), 1)
            if axis == "x":
                cv2.putText(img, "  Y    X", (Cx,Cy-45), cv2.FONT_HERSHEY_COMPLEX, 0.6, (0,0,0), 1)
            else:
                if axis == "y":
                    cv2.putText(img, "  Y    Z", (Cx,Cy-45), cv2.FONT_HERSHEY_COMPLEX, 0.6, (0,0,0), 1)
            # cv2.putText(img, str(data_XYZ[Cx][Cy]), (Cx,Cy-25), cv2.FONT_HERSHEY_COMPLEX, 0.6, (0,0,0), 1)
            pos = data_XYZ[Cy][Cx]
            if pos != 0:
                pos = pos.split(",")
            else:
                pos = (0,0)

            return img, pos, Cx, Cy
        
    return img, (0,0), 0, 0

def from_3d_to_2d(img, point_3d, camera_matrix, dist_coeffs, rvecs, tvecs, origin=(0, 0)):
    # point_3d = np.float32([[0,0,0],point_3d]).reshape(-1,3)
    point_3d = np.float32(point_3d).reshape(-1,3)

    img_points, _ = cv2.projectPoints(point_3d, rvecs, tvecs, camera_matrix, dist_coeffs)
    img_points = img_points.astype(int)

    # Khoảng cách so với gốc tọa độ chọn trên ảnh
    offset_X = origin[0] - img_points[0][0][0]
    offset_Y = origin[1] - img_points[0][0][1]
    # Điều chỉnh lại tọa độ theo offset
    for i in range(len(img_points)):
        img_points[i][0][0] += offset_X
        img_points[i][0][1] += offset_Y
       
    for i in range(len(img_points)):
        cv2.circle(img, (img_points[i][0][0], img_points[i][0][1]), radius=3, color=(0, 0, 0), thickness=-1)
    # print(img_points[1][0][0], img_points[1][0][1])
    return img

def from_3d_to_2d_no_fix(img, point_3d, camera_matrix, dist_coeffs, rvecs, tvecs):
    # point_3d = np.float32([[0,0,0],point_3d]).reshape(-1,3)
    point_3d = np.float32(point_3d).reshape(-1,3)

    img_points, _ = cv2.projectPoints(point_3d, rvecs, tvecs, camera_matrix, dist_coeffs)
    img_points = img_points.astype(int)
    
    for i in range(len(img_points)):
        cv2.circle(img, (img_points[i][0][0], img_points[i][0][1]), radius=3, color=(0, 0, 0), thickness=-1)
    # print(img_points[1][0][0], img_points[1][0][1])
    return img

def from_3d_to_2d_no_image(point_3d, camera_matrix, dist_coeffs, rvecs, tvecs, origin=(0, 0)):
    point_3d = np.float32([[0,0,0],point_3d]).reshape(-1,3)

    img_points, _ = cv2.projectPoints(point_3d, rvecs, tvecs, camera_matrix, dist_coeffs)
    img_points = img_points.astype(int)

    # Khoảng cách so với gốc tọa độ chọn trên ảnh
    offset_X = origin[0] - img_points[0][0][0]
    offset_Y = origin[1] - img_points[0][0][1]
    # Điều chỉnh lại tọa độ theo offset
    for i in range(len(img_points)):
        img_points[i][0][0] += offset_X
        img_points[i][0][1] += offset_Y
       
    # print(img_points[1][0][0], img_points[1][0][1])
    return img_points[1][0][0], img_points[1][0][1]

# Đọc hình ảnh cần rectify
def get_coordinate_axes(camera_matrix, dist_coeffs, rvecs, tvecs, axis_length=125, origin=(0, 0), axis="x"):
    # 3D points of the coordinate axes
    axis_points = np.float32([[0,0,0], [axis_length,0,0],[0,axis_length,0]]).reshape(-1,3)
    # Chia khoảng trên trục x và y
    x_axis = np.float32([[-125,0,0],[-100,0,0], [-75,0,0], [-50,0,0], [-25,0,0], [0,0,0], [25,0,0], [50,0,0], [75,0,0], [100,0,0], [125,0,0]]).reshape(-1,3)
    if axis == "x":
        y_axis = np.float32([[0,-125,0],[0,-100,0], [0,-75,0], [0,-50,0], [0,-25,0], [0,0,0], [0,25,0], [0,50,0], [0,75,0], [0,100,0], [0,125,0]]).reshape(-1,3)
    else:
        y_axis = np.float32([[0,0,0],[0,25,0], [0,50,0], [0,75,0], [0,100,0], [0,125,0], [0,150,0], [0,175,0], [0,200,0], [0,225,0], [0,250,0]]).reshape(-1,3)
    # Project the 3D points to 2D image points
    img_points, _ = cv2.projectPoints(axis_points, rvecs, tvecs, camera_matrix, dist_coeffs)
    x_points, _ = cv2.projectPoints(x_axis, rvecs, tvecs, camera_matrix, dist_coeffs)
    y_points, _ = cv2.projectPoints(y_axis, rvecs, tvecs, camera_matrix, dist_coeffs)
    # Convert image points to integer
    img_points = img_points.astype(int)
    x_points = x_points.astype(int)
    y_points = y_points.astype(int)
    # Khoảng cách so với gốc tọa độ chọn trên ảnh
    offset_X = origin[0] - img_points[0][0][0]
    offset_Y = origin[1] - img_points[0][0][1]
    # Điều chỉnh lại tọa độ theo offset
    for i in range(len(img_points)):
        img_points[i][0][0] += offset_X
        img_points[i][0][1] += offset_Y

    for i in range(len(x_points)):
        x_points[i][0][0] += offset_X
        x_points[i][0][1] += offset_Y

    for i in range(len(y_points)):
        y_points[i][0][0] += offset_X
        y_points[i][0][1] += offset_Y
    # # print(x_points[0][0])

    return img_points, x_points, y_points

def draw_coordinate_axes(image, img_points, x_points, y_points, axis=""):
    cv2.line(image, tuple(img_points[0].ravel()), tuple(img_points[1].ravel()), (0,0,255), 2)  # y-axis (green)
    # Đánh dấu các khoảng trên trục tọa độ
    # Keep radius as 0 for plotting a single point and thickness as a negative number for a filled circle
    # for i in range(len(x_points)):
    #     cv2.circle(image, (x_points[i][0][0], x_points[i][0][1]), radius=3, color=(0, 0, 0), thickness=-1)
    #     cv2.putText(image, str(25 * i - 125), (x_points[i][0][0] - 20, x_points[i][0][1]), cv2.FONT_ITALIC, 0.3, (0, 0, 0), 1) 
    cv2.putText(image, "Y", (x_points[-1][0][0] + 20, x_points[-1][0][1]), cv2.FONT_ITALIC, 0.7, (0, 0, 0), 2) 
    if axis == "x":
        cv2.line(image, tuple(img_points[0].ravel()), tuple(img_points[2].ravel()), (0,255,0), 2)  # x-axis (red)
        # for i in range(len(y_points)):
        #     cv2.circle(image, (y_points[i][0][0], y_points[i][0][1]), radius=3, color=(0, 0, 0), thickness=-1)
        #     cv2.putText(image, str(25 * i - 125), (y_points[i][0][0]-20, y_points[i][0][1] + 20), cv2.FONT_ITALIC, 0.3, (0, 0, 0), 1) 
        cv2.putText(image, "X", (y_points[-1][0][0], y_points[-1][0][1] - 20), cv2.FONT_ITALIC, 0.7, (0, 0, 0), 2) 
    else:
        if axis == "y":
            cv2.line(image, tuple(img_points[0].ravel()), tuple(img_points[2].ravel()), (255,0,0), 2)  # z-axis (blue)
            # for i in range(len(y_points)):
            #     cv2.circle(image, (y_points[i][0][0], y_points[i][0][1]), radius=3, color=(0, 0, 0), thickness=-1)
            #     cv2.putText(image, str(25 * i), (y_points[i][0][0]-20, y_points[i][0][1] + 20), cv2.FONT_ITALIC, 0.3, (0, 0, 0), 1) 
            cv2.putText(image, "Z", (y_points[-1][0][0], y_points[-1][0][1] - 20), cv2.FONT_ITALIC, 0.7, (0, 0, 0), 2) 
    
    return image

def draw_coordinate_axes_no_fix(image, camera_matrix, dist_coeffs, rvecs, tvecs, axis_length=250):
    # 3D points of the coordinate axes
    axis_points = np.float32([[0,0,0], [axis_length,0,0], [0,axis_length,0], [0,0,-axis_length]]).reshape(-1,3)

    # Project the 3D points to 2D image points
    img_points, _ = cv2.projectPoints(axis_points, rvecs, tvecs, camera_matrix, dist_coeffs)

    # Convert image points to integer
    img_points = img_points.astype(int)

    # Draw coordinate axes on the image
    cv2.line(image, tuple(img_points[0].ravel()), tuple(img_points[1].ravel()), (0,0,255), 2)  # x-axis (red)
    cv2.line(image, tuple(img_points[0].ravel()), tuple(img_points[2].ravel()), (0,255,0), 2)  # y-axis (green)
    cv2.line(image, tuple(img_points[0].ravel()), tuple(img_points[3].ravel()), (255,0,0), 2)  # z-axis (blue)

    return image

def calculate_real_position(camera1=(0,0,0), camera2=(0,0,0), A1=(0,0,0), A3=(0,0,0), B2=(0,0,0), B3=(0,0,0)):
    # Viết phương trình đường thẳng C1A3 và C2B3: y = kx + c
    # k = (y2-y1)/(x2-x1)
    k1 = (A3[1]-camera1[1])/(A3[0]-camera1[0]+1.0)
    k2 = (B3[1]-camera2[1])/(B3[0]-camera2[0])

    c1 = camera1[1] - k1*camera1[0]
    c2 = camera2[1] - k2*camera2[0]

    X = (c2-c1)/(k1-k2)
    Z = k1*X + c1

    d1 = abs(camera1[1]) - abs(Z)
    d2 = abs(camera2[0]) - abs(X)
    
    Y1 = d1 * A1[2] / (camera1[1]-A3[1])
    Y2 = d2 * B2[2] / (abs(camera2[0])-abs(B3[0]))
    Y = 0.6*Y2 + 0.4*Y1
    # print(Z1,Z2)

    return round(X,2), round(Y,2), round(Z,2)

def cal_phi_and_theta(point):
    E_X = point[0]
    E_Y = point[1]
    E_Z = point[2]

    if E_X == 0:
        if E_Y == 0:
            phi = 0
        elif E_Y > 0:
            phi = math.pi/2
        else:
            phi = 3*math.pi/2
    elif E_X > 0:
        if E_Y >= 0:
            phi = math.atan(E_Y/E_X)
        else:
            phi = 2*math.pi + math.atan(E_Y/E_X)
    elif E_X < 0:
        phi = math.atan(E_Y/E_X) + math.pi

    theta = 2*math.atan(math.sqrt(E_X**2 + E_Y**2) / E_Z)

    return phi, theta

def cal_error_phi_and_theta(target_point, current_point):
    phi_target, theta_target = cal_phi_and_theta(target_point)
    phi_current, theta_current = cal_phi_and_theta(current_point)

    phi_error = phi_target - phi_current
    theta_error = theta_target - theta_current

    return [phi_error, theta_error]

def PID(sum_error, error, prev_error, Kp, Ki, Kd, delta_t, limit):
    U = []

    sum_error[0] += error[0]
    sum_error[1] += error[1]

    U.append(Kp[0]*error[0] + Ki[0]*sum_error[0] + Kd[0]*(error[0]-prev_error[0])/delta_t)
    U.append(Kp[1]*error[1] + Ki[1]*sum_error[1] + Kd[1]*(error[1]-prev_error[1])/delta_t)
    if U[0] > limit[0]:
        U[0] = limit[0]
    if U[0] < -limit[0]:
        U[0] = -limit[0]
    if U[1] > limit[1]:
        U[1] = limit[1]
    if U[1] < -limit[1]:
        U[1] = -limit[1]
    return U

def update_phi_and_theta(current_phi, current_theta, U):

    current_phi += 0.005*U[0]
    current_theta += 0.05*U[1]

    return current_phi, current_theta

def update_tendon_length(phi, theta, tendon_length, r=8.5, n=8):
    _, l, _ = knm.cal_intermediate_params(tendon_length, r, n)

    tendon_length[0] = l - 0.5*r*theta*math.cos(phi)
    # if tendon_length[0] > 111:
    #     tendon_length[0] = 111
    tendon_length[1] = l - 0.5*r*theta*math.cos(math.pi/2 - phi)
    # if tendon_length[1] > 111:
    #     tendon_length[1] = 111
    tendon_length[2] = l + 0.5*r*theta*math.cos(phi)
    # if tendon_length[2] > 111:
    #     tendon_length[2] = 111
    tendon_length[3] = l - 0.5*r*theta*math.cos(math.pi/2 + phi)
    # if tendon_length[3] > 111:
    #     tendon_length[3] = 111
    if tendon_length[0] > 111 or tendon_length[1] > 111 or tendon_length[2] > 111 or tendon_length[3] > 111:
        tendon_length[0] -= 2
        tendon_length[1] -= 2
        tendon_length[2] -= 2
        tendon_length[3] -= 2
    return tendon_length