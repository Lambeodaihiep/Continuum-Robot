import pandas as pd
import numpy as np
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
# import trajectory as tj
# plt.style.use('seaborn-poster')

# circle trajectory
# center = np.array([0, 100, 0])
# X, Y, Z = tj.circle_trajectory(center, 50)

fig = plt.figure(figsize = (10,10))
ax = plt.axes(projection='3d')
ax.grid()

# data = pd.read_excel("continuum/image_processing/data/data_full.xlsx", sheet_name="data")
# data = pd.read_excel("continuum/image_processing/data/trajectory/10_85_-5_50.xlsx", sheet_name="data")
# data = pd.read_excel("continuum/image_processing/data/trajectory/0_80_0_65.xlsx", sheet_name="data")
data = pd.read_excel("C:/Users/DELL/Desktop/python/QT designer/continuum/image_processing/data/FK/data.xlsx", sheet_name="frame 1")
x = np.array(data["X"])
y = np.array(data["Y"])
z = np.array(data["Z"])

# ax.plot3D(x, y, z)
ax.scatter(x, y, z, c = 'r', s = 2, label='quỹ đạo thực')
# ax.scatter(center[0], center[1], center[2], c = 'b', s = 20)
# ax.scatter(X, Y, Z, c = 'b', s = 5, label='quỹ đạo mong muốn')
# ax.set_title('Quỹ đạo hình tròn tâm O(' + str(center[0]) + ';' + str(center[1]) + ';' + str(center[2]) + '), R = 50')
ax.legend()



# Set axes label
ax.set_xlabel('x', labelpad=20)
ax.set_ylabel('y', labelpad=20)
ax.set_zlabel('z', labelpad=20)

plt.show()


