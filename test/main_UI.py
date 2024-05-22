import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog
from PyQt5.uic import loadUi
import cv2

class MainWindow(QDialog):
    
    def __init__(self):
        super(MainWindow,self).__init__()
        loadUi("gui.ui",self)
        self.browse.clicked.connect(self.browsefiles)
        self.clearInput.clicked.connect(self.clear_input)
        self.clearOutput.clicked.connect(self.clear_output)
        self.process.clicked.connect(self.process_image)

    def browsefiles(self):
        fname=QFileDialog.getOpenFileName(self, 'Open file', 'D:\codefirst.io\PyQt5 tutorials\Browse Files', 'Images (*.png, *.xmp *.jpg)')
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
        p = convert_to_Qt_format.scaled(400, 300, QtCore.Qt.KeepAspectRatio)
        return QtGui.QPixmap.fromImage(p)

    

app = QApplication(sys.argv)
mainwindow=MainWindow()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setFixedWidth(830)
widget.setFixedHeight(600)
widget.show()
sys.exit(app.exec_())