import numpy as np
import cv2
import sys
sys.path.insert(1, 'continuum/image_processing')
import image_processing as imp
# import platform
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import (QCoreApplication, QPropertyAnimation, QDate, QDateTime, QMetaObject, QObject, QPoint, QRect, QSize, QTime, QUrl, Qt, QEvent, QThread, pyqtSignal)
# from PyQt5.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient)
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi

# Cái này để gửi tọa độ cho robot
import serial
import serial.tools.list_ports
mySerial = serial.Serial()

### Load parameter ###
camera_matrix1 = np.load('continuum/cameraCalibration/saveData/cam1/camera_matrix.npy')
dist_coeffs1 = np.load('continuum/cameraCalibration/saveData/cam1/dist_coeffs.npy')

camera_matrix2 = np.load('continuum/cameraCalibration/saveData/cam2/camera_matrix.npy')
dist_coeffs2 = np.load('continuum/cameraCalibration/saveData/cam2/dist_coeffs.npy')

# GUI FILE
# from ui_main import Ui_MainWindow

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        # self = Ui_MainWindow()
        loadUi("continuum/main/ui_main.ui",self)
        self.browse.clicked.connect(self.browsefiles)
        self.process.clicked.connect(self.process_image)
        self.clearInput.clicked.connect(self.clear_input)
        self.clearOutput.clicked.connect(self.clear_output)
        self.confirm_cam_1.clicked.connect(self.Confirm_cam_1)
        self.stop_cam_1.clicked.connect(self.Stop_cam_1)
        self.confirm_cam_2.clicked.connect(self.Confirm_cam_2)
        self.stop_cam_2.clicked.connect(self.Stop_cam_2)
        self.confirm_position.clicked.connect(self.Confirm_position)
        self.confirm_microcontroller.clicked.connect(self.Confirm_microcontroller)
        self.scan_port.clicked.connect(self.Scan_port)
        self.motor_1.editingFinished.connect(self.edit_motor_1)
        self.motor_2.editingFinished.connect(self.edit_motor_2)
        self.motor_3.editingFinished.connect(self.edit_motor_3)
        self.motor_4.editingFinished.connect(self.edit_motor_4)
        self.motor_1_slider.valueChanged.connect(self.Motor_1_slider)
        self.motor_2_slider.valueChanged.connect(self.Motor_2_slider)
        self.motor_3_slider.valueChanged.connect(self.Motor_3_slider)
        self.motor_4_slider.valueChanged.connect(self.Motor_4_slider)

        # Chả biết này là gì nhưng nó quan trọng
        self.thread = {}
        # self.setupUi(self)

        ## TOGGLE/BURGUER MENU
        ########################################################################
        self.Btn_Toggle.clicked.connect(lambda: UIFunctions.toggleMenu(self, 250, True))

        ## PAGES
        # PAGE 1
        self.btn_page_1.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_1))
        # PAGE 2
        self.btn_page_2.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_2))
        # PAGE 3
        self.btn_page_3.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_3))

        ## SHOW ==> MAIN WINDOW
        ########################################################################
        self.show()
        ## ==> END ##

    def browsefiles(self):
        fname=QFileDialog.getOpenFileName(self, 'Open file', 'D:\codefirst.io\PyQt5 tutorials\Browse Files', 'Images (*.*)')
        self.path.setText(fname[0])
        self.input_image.setPixmap(QtGui.QPixmap(fname[0]))
        self.input_image.setScaledContents(True)

    def process_image(self):
        self.image = cv2.imread(self.path.property("text"))
        self.gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        # self.image = QtGui.QImage(self.image.data, self.image.shape[1], self.image.shape[0], QtGui.QImage.Format_RGB888).rgbSwapped()
        self.output_image.setPixmap(self.convert_cv_qt(self.gray))
        self.output_image.setScaledContents(True)
    
    def clear_input(self):
        self.input_image.clear()
        self.input_image.setText("Input")
    
    def clear_output(self):
        self.output_image.clear()
        self.output_image.setText("Output")

    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(640, 480, QtCore.Qt.KeepAspectRatio)
        return QtGui.QPixmap.fromImage(p)
                   
    # def closeEvent1(self, event):
    #     self.Stop_cam_1()

    def Stop_cam_1(self):
        self.thread[1].stop()
        self.cam_1.clear()
        self.cam_1.setText("No signal")

    def Confirm_cam_1(self):
        self.thread[1] = capture_video(index=int(self.checkbox_1.currentText()[-1]))
        self.thread[1].start()
        self.thread[1].signal.connect(self.show_webcam1)

    def show_webcam1(self, cv_img):
        """Updates the image_label with a new opencv image"""
        cv_img = cv2.undistort(cv_img, camera_matrix1, dist_coeffs1)
        cv_img = imp.getContours(cv_img, (15,128), 427, [70, 255], 100, 0.3, "y", True)
        qt_img = self.convert_cv_qt(cv_img)
        self.cam_1.setPixmap(qt_img)

    def Stop_cam_2(self):
        self.thread[2].stop()
        self.cam_2.clear()
        self.cam_2.setText("No signal")

    def Confirm_cam_2(self):
        self.thread[2] = capture_video(index=int(self.checkbox_2.currentText()[-1]))
        self.thread[2].start()
        self.thread[2].signal.connect(self.show_webcam2)

    def show_webcam2(self, cv_img):
        """Updates the image_label with a new opencv image"""
        cv_img = cv2.undistort(cv_img, camera_matrix2, dist_coeffs2)
        cv_img = imp.getContours(cv_img, (18,143), 427, [85, 255], 100, 0.3, "x", True)
        qt_img = self.convert_cv_qt(cv_img)
        self.cam_2.setPixmap(qt_img)

    def Confirm_position(self):
        msg = self.motor_1.text() + "," + self.motor_2.text() + "," + self.motor_3.text() + "," + self.motor_4.text()
        # print(msg)
        mySerial.write(msg.encode("utf-8"))

    def Confirm_microcontroller(self):
        # print(self.baudrate_box.currentText())
        # print(self.port_box.currentText().split("-")[0][:-1])
        mySerial.baudrate = int(self.baudrate_box.currentText())
        mySerial.port = self.port_box.currentText().split("-")[0][:-1]
        mySerial.open()

    def Scan_port(self):
        self.port_box.clear()
        portData = serial.tools.list_ports.comports()
        if len(portData) == 0:
            self.port_box.addItem("No port available")
        else:
            for i in range(len(portData)):
                self.port_box.addItem(str(portData[i]))
                # print(type(portData[i]))

    def edit_motor_1(self):
        self.motor_1_slider.setValue(int(self.motor_1.text()))
    def edit_motor_2(self):
        self.motor_2_slider.setValue(int(self.motor_2.text()))
    def edit_motor_3(self):
        self.motor_3_slider.setValue(int(self.motor_3.text()))
    def edit_motor_4(self):
        self.motor_4_slider.setValue(int(self.motor_4.text()))

    def Motor_1_slider(self, value):
        self.motor_1.setText(str(value))
    def Motor_2_slider(self, value):
        self.motor_2.setText(str(value))
    def Motor_3_slider(self, value):
        self.motor_3.setText(str(value))
    def Motor_4_slider(self, value):
        self.motor_4.setText(str(value))


class capture_video(QThread):
    signal = pyqtSignal(np.ndarray)
    def __init__(self, index):
        self.index = index
        print("start threading", self.index)
        super(capture_video, self).__init__()
        
    def run(self):
        cap = cv2.VideoCapture(self.index, cv2.CAP_DSHOW)
        while True:
            ret, cv_img = cap.read()
            if ret:
                self.signal.emit(cv_img)
    
    def stop(self):
        print("stop threading", self.index)
        self.terminate()

class UIFunctions(MainWindow):
    def toggleMenu(self, maxWidth, enable):
        if enable:

            # GET WIDTH
            width = self.frame_left_menu.width()
            maxExtend = maxWidth
            standard = 70

            # SET MAX WIDTH
            if width == 70:
                widthExtended = maxExtend
            else:
                widthExtended = standard

            # ANIMATION
            self.animation = QPropertyAnimation(self.frame_left_menu, b"minimumWidth")
            self.animation.setDuration(400)
            self.animation.setStartValue(width)
            self.animation.setEndValue(widthExtended)
            self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animation.start()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
