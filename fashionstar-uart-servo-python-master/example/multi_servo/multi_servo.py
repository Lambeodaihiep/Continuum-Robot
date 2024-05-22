# 添加uservo.py的系统路径
import sys
sys.path.append("continuum/fashionstar-uart-servo-python-master/src")
# 导入依赖
import time
import struct
import serial
from uservo import UartServoManager

# 参数配置
# 角度定义
SERVO_PORT_NAME =  'COM5'		# 舵机串口号
SERVO_BAUDRATE = 115200			# 舵机的波特率
SERVO_ID1 = 1   				# 舵机的ID号
SERVO_ID2 = 2   				# 舵机的ID号
SERVO_ID3 = 3   				# 舵机的ID号
SERVO_ID4 = 4   				# 舵机的ID号
SERVO_HAS_MTURN_FUNC = False	# 舵机是否拥有多圈模式 - Does the servo have multi-turn mode?

# 初始化串口
uart = serial.Serial(port=SERVO_PORT_NAME, baudrate=SERVO_BAUDRATE,\
					 parity=serial.PARITY_NONE, stopbits=1,\
					 bytesize=8,timeout=0)
# 初始化舵机管理器 - Initialize the servo manager
uservo = UartServoManager(uart, is_debug=True)

# print("[单圈模式]设置舵机角度为 90.0° - [Single lap mode] Set the servo angle to 90.0°")
# uservo.set_servo_angle(SERVO_ID1, 90.0, interval=0) # 设置舵机角度 极速模式 - Set the servo angle in extreme speed mode
# uservo.set_servo_angle(SERVO_ID2, 90.0, interval=0) # 设置舵机角度 极速模式 - Set the servo angle in extreme speed mode
# uservo.wait() # 等待舵机静止 - Wait for the servo to stop
# print("-> {}".format(uservo.query_servo_angle(SERVO_ID1)))

while True:
    uservo.set_servo_angle(SERVO_ID1, 130.0, interval=1000)
    uservo.set_servo_angle(SERVO_ID2, 130.0, interval=1000)
    uservo.set_servo_angle(SERVO_ID3, 130.0, interval=1000)
    uservo.set_servo_angle(SERVO_ID4, 130.0, interval=1000)
    uservo.wait()
    time.sleep(1)

    uservo.set_servo_angle(SERVO_ID1, 111.5, interval=1000)
    uservo.set_servo_angle(SERVO_ID2, 79.2, interval=1000)
    uservo.set_servo_angle(SERVO_ID3, 79.2, interval=1000)
    uservo.set_servo_angle(SERVO_ID4, 130.0, interval=1000)
    uservo.wait()
    time.sleep(5)

# print("[单圈模式]设置舵机角度为-80.0°, 周期1000ms - [Single turn mode] Set the servo angle to -80.0°, period 1000ms")
# uservo.set_servo_angle(SERVO_ID, -80.0, interval=1000) # 设置舵机角度(指定周期 单位ms) - Set the servo angle (specify period in ms)
# uservo.wait() # 等待舵机静止 - Wait for the servo to stop
# print("-> {}".format(uservo.query_servo_angle(SERVO_ID)))

# print("[单圈模式]设置舵机角度为70.0°, 设置转速为200 °/s, 加速时间100ms, 减速时间100ms")
# print("[Single-turn mode] Set the servo angle to 70.0°, set the rotation speed to 200 °/s, accelerate the time to 100ms, and decelerate to the time of 100ms.")
# uservo.set_servo_angle(SERVO_ID, 70.0, velocity=200.0, t_acc=100, t_dec=100) # 设置舵机角度(指定转速 单位°/s) - Set the servo angle (specified speed unit °/s)
# uservo.wait() # 等待舵机静止 - Wait for the servo to stop
# print("-> {}".format(uservo.query_servo_angle(SERVO_ID)))

# print("[单圈模式]设置舵机角度为-90.0°, 添加功率限制 - [Single lap mode] Set the servo angle to -90.0° and add power limit")
# uservo.set_servo_angle(SERVO_ID, -90.0, power=400) # 设置舵机角度(指定功率 单位mW) - Set the servo angle (specify power in mW)
# uservo.wait() # 等待舵机静止 - Wait for the servo to stop
