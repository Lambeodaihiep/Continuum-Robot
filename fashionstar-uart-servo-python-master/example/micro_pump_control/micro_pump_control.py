'''
FashionStar Uart舵机 
> 气泵开关控制 <
--------------------------------------------------
- 作者: 阿凯
- Email: kyle.xing@fashionstar.com.hk
- 更新时间: 2021-3-22
--------------------------------------------------
'''
# 添加uservo.py的系统路径
import sys
sys.path.append("../../src")
# 导入依赖
import time
import struct
import serial
from uservo import UartServoManager

# 参数配置
# 角度定义
SERVO_PORT_NAME =  'COM12' # 舵机串口号
SERVO_BAUDRATE = 115200 # 舵机的波特率
SERVO_ID = 0xFE  # 舵机的ID号

# 初始化串口
uart = serial.Serial(port=SERVO_PORT_NAME, baudrate=SERVO_BAUDRATE,\
					 parity=serial.PARITY_NONE, stopbits=1,\
					 bytesize=8,timeout=0)
# 初始化舵机管理器
uservo = UartServoManager(uart, is_debug=True, is_scan_servo=False)

def pump_value(uservo, value):
	param_bytes = struct.pack('<BhHH', 0xFE, int(value*10), int(0), int(0))
	uservo.send_request(uservo.CODE_SET_SERVO_ANGLE, param_bytes)
	
def pump_on(uservo):
	'''气泵打开'''
	pump_value(uservo, -90.0)

def pump_off(uservo):
	'''气泵关闭'''
	pump_value(uservo, 0.0) 
	time.sleep(0.1)
	pump_value(uservo, 90.0) 
	time.sleep(0.5)
	pump_value(uservo, 0.0) 


pump_on(uservo)
time.sleep(5)
pump_off(uservo)