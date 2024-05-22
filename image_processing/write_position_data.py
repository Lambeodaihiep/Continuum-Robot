import pandas as pd
import numpy as np
import image_processing as imp

new_camera_matrix1 = np.load('continuum/cameraCalibration/saveData/cam1/new_camera_matrix.npy')
new_dist_coeffs1 = np.load('continuum/cameraCalibration/saveData/cam1/new_dist_coeffs.npy')
new_rvecs1 = np.load('continuum/cameraCalibration/saveData/cam1/new_rvecs.npy')
new_tvecs1 = np.load('continuum/cameraCalibration/saveData/cam1/new_tvecs.npy')

new_camera_matrix2 = np.load('continuum/cameraCalibration/saveData/cam2/new_camera_matrix.npy')
new_dist_coeffs2 = np.load('continuum/cameraCalibration/saveData/cam2/new_dist_coeffs.npy')
new_rvecs2 = np.load('continuum/cameraCalibration/saveData/cam2/new_rvecs.npy')
new_tvecs2 = np.load('continuum/cameraCalibration/saveData/cam2/new_tvecs.npy')

position = np.arange(-125,175,0.1)
data_X_1 = [[0] * 640 for _ in range(640)]
data_Y_1 = [[0] * 640 for _ in range(640)]
count_1 = [[0] * 640 for _ in range(640)]

data_X_2 = [[0] * 640 for _ in range(640)]
data_Y_2 = [[0] * 640 for _ in range(640)]
count_2 = [[0] * 640 for _ in range(640)]

origin1=(333, 240)
origin2=(112, 240)

for i in range(len(position)):
    for j in range(len(position)):
        pixx, pixy = imp.from_3d_to_2d_no_image((position[i],position[j],0), new_camera_matrix1, new_dist_coeffs1, new_rvecs1[0], new_tvecs1[0], origin=origin1)
        data_X_1[pixx][pixy] += position[i]
        data_Y_1[pixx][pixy] += position[j]
        count_1[pixx][pixy] +=1
        pixx, pixy = imp.from_3d_to_2d_no_image((position[i],position[j],0), new_camera_matrix2, new_dist_coeffs2, new_rvecs2[0], new_tvecs2[0], origin=origin2)
        data_X_2[pixx][pixy] += position[i]
        data_Y_2[pixx][pixy] += position[j]
        count_2[pixx][pixy] +=1

data_XYZ_1 = [[0] * 640 for _ in range(640)]
data_XYZ_2 = [[0] * 640 for _ in range(640)]

for i in range(640):
    for j in range(640):
        if count_1[i][j] == 0 or count_2[i][j] == 0:
            continue
        data_XYZ_1[i][j] = str(round(data_X_1[i][j]/count_1[i][j],2)) + "," + str(round(data_Y_1[i][j]/count_1[i][j],2))
        data_XYZ_2[i][j] = str(round(data_X_2[i][j]/count_2[i][j],2)) + "," + str(round(data_Y_2[i][j]/count_2[i][j],2))
print("almost done")

df1 = pd.DataFrame(data_XYZ_1)
df2 = pd.DataFrame(data_XYZ_2)
        
# X1 = pd.DataFrame(data_X_1)
# Y1 = pd.DataFrame(data_Y_1)
# C1 = pd.DataFrame(count_1)
# X2 = pd.DataFrame(data_X_2)
# Y2 = pd.DataFrame(data_Y_2)
# C2 = pd.DataFrame(count_2)

writer = pd.ExcelWriter("continuum/image_processing/data/data_XYZ.xlsx")

df1.to_excel(writer, sheet_name="frame 1")
df2.to_excel(writer, sheet_name="frame 2")
# X1.to_excel(writer, sheet_name="X1")
# Y1.to_excel(writer, sheet_name="Y1")
# C1.to_excel(writer, sheet_name="C1")
# X2.to_excel(writer, sheet_name="X2")
# Y2.to_excel(writer, sheet_name="Y2")
# C2.to_excel(writer, sheet_name="C2")

writer.close()