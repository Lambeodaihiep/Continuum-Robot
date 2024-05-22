import pandas as pd
import time

# Cái này để gửi tọa độ cho robot
import serial
import serial.tools.list_ports
mySerial = serial.Serial()
mySerial.baudrate = 115200
mySerial.port = 'COM4'
mySerial.open()

motor_position = pd.read_excel("continuum/image_processing/data.xlsx", sheet_name="Motor")

for i in range(len(motor_position)):
    msg = str(motor_position['motor 1'][i]) + "," + str(motor_position['motor 2'][i]) + "," + str(motor_position['motor 3'][i]) + "," + str(motor_position['motor 4'][i])
    print(msg)
    mySerial.write(msg.encode("utf-8"))
    time.sleep(1)
