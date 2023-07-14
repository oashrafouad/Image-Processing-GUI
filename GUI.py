from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic
from PyQt5 import QtWidgets

from normalization import normalization
from powerLaw import powerLaw
from cvt2gray import cvt2gray
from negative import negative
from ButterworthHighPassFilter import butterworthHighPassFilter
from average import average
from sharpening import sharpening
from edge import edgeDetection
from unsharpMask import unsharp
from ButterworthLowPassFilter import butterworthLowPassFilter
from DarkBright import DarkBright
from DM_0 import dm_0
from DM_1 import DM_1_order
from RM_0 import RM_0_order
from histogramDrawing import histogram
from add import add
from quantization import quantization
from gaussianLowPassFilter import gaussianLowPassFilter
from GaussianHighPassFilterformula import gaussianHighPassFilter
from HistogramEqualization import histogramEqualization
from IdealLowPassFilter import idealLowPassFilter
from IdealHighPassFilter import idealHighPassFilter
from sub import sub
from histogramMatching import histogramMatching
from WeightedFilter import weightedFilter

imagePath = ""
firstImagePath = ""
secondImagePath = ""

# Class for the main app window
class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Load the UI file into the class
        uic.loadUi("mainwindow.ui", self)

    def chooseClicked(self):
        # Get the button that was clicked
        clickedButton = self.sender()

        # global keyword to enable modifying the global imagePath not creating a local one
        global imagePath
        global firstImagePath
        global secondImagePath

        if clickedButton == chooseButton:
            # Get the path of the image that the user selects. imageName is a tuple of two values. The first value is the path of the image and is stored in imagePath
            imageName = QFileDialog.getOpenFileName(None, '', '', 'Image Files (*.png *.jpg *.jpeg *.bmp)')
            imagePath = imageName[0]
            # Set that image to be the image label
            imageLabel.setPixmap(QPixmap(imagePath))
            # Remove the border and rounded corners from the image label
            imageLabel.setStyleSheet("")
        elif clickedButton == chooseFirstButton:
            firstImageName = QFileDialog.getOpenFileName(None, '', '', 'Image Files (*.png *.jpg *.jpeg *.bmp)')
            firstImagePath = firstImageName[0]
            # Set that image to be the image label
            firstImageLabel.setPixmap(QPixmap(firstImagePath))
            # Remove the border from the image label
            firstImageLabel.setStyleSheet("")
        elif clickedButton == chooseSecondButton:
            secondImageName = QFileDialog.getOpenFileName(None, '', '', 'Image Files (*.png *.jpg *.jpeg *.bmp)')
            secondImagePath = secondImageName[0]
            # Set that image to be the image label
            secondImageLabel.setPixmap(QPixmap(secondImagePath))
            # Remove the border from the image label
            secondImageLabel.setStyleSheet("")

    def applyClicked(self):
        selectedFilter = filterComboBox.currentText()
        if selectedFilter == "Add two images" or filterComboBox.currentText() == "Subtract two images" or filterComboBox.currentText() == "Histogram Matching":
            filters[selectedFilter](path1 = firstImagePath, path2 = secondImagePath)
        else:
            filters[selectedFilter](path = imagePath)
        outputImageLabel.setPixmap(QPixmap("./edited.jpg"))
        outputImageLabel.setStyleSheet("")

    def clearClicked(self):
        # Reset labels to original style
        imageLabel.setStyleSheet("border: 2px solid gray; border-radius: 10px; background-color: rgb(59, 59, 59); color: rgb(161, 161, 161)")
        imageLabel.setText("No image selected")

        firstImageLabel.setStyleSheet("border: 2px solid gray; border-radius: 10px; background-color: rgb(59, 59, 59); color: rgb(161, 161, 161)")
        firstImageLabel.setText("No image selected")

        secondImageLabel.setStyleSheet("border: 2px solid gray; border-radius: 10px; background-color: rgb(59, 59, 59); color: rgb(161, 161, 161)")
        secondImageLabel.setText("No image selected")

        outputImageLabel.setStyleSheet("border: 2px solid gray; border-radius: 10px; background-color: rgb(59, 59, 59); color: rgb(161, 161, 161)")
        outputImageLabel.setText("Apply a filter to see the result")

        global imagePath
        global firstImagePath
        global secondImagePath
        imagePath = ""
        firstImagePath = ""
        secondImagePath = ""
        filterComboBox.setCurrentIndex(-1)

    def filterChanged(self, filterName):
        if filterName == "Add two images" or filterName == "Subtract two images" or filterName == "Histogram Matching":
            # Switch to two images view
            inputStackedWidget.setCurrentIndex(1)
        else:
            # Switch to single image view
            inputStackedWidget.setCurrentIndex(0)


# Constantly check in the background if the user has selected an image and a filter to enable the apply and clear buttons
class CheckThread(QThread):
    def __init__(self):
        super().__init__()

    def run(self):
        while True:
            if (imagePath != "" and filterComboBox.currentText() != "") or (firstImagePath != "" and secondImagePath != "" and filterComboBox.currentText() != ""):
                applyPushButton.setDisabled(False)
                clearPushButton.setDisabled(False)
            else:
                applyPushButton.setDisabled(True)
                clearPushButton.setDisabled(True)

app = QApplication([])

window = MainWindow()

# For autocompletion when accessing those properties. This isn't needed
filterComboBox: QComboBox = window.filterComboBox
imageLabel: QLabel = window.imageLabel
applyPushButton: QPushButton = window.applyPushButton
clearPushButton: QPushButton = window.clearPushButton
chooseButton: QPushButton = window.chooseButton
inputStackedWidget: QStackedWidget = window.inputStackedWidget
chooseLabel: QLabel = window.chooseLabel
chooseFirstButton: QPushButton = window.chooseFirstButton
chooseSecondButton: QPushButton = window.chooseSecondButton
chooseFirstLabel: QLabel = window.chooseFirstLabel
chooseSecondLabel: QLabel = window.chooseSecondLabel
firstImageLabel: QLabel = window.firstImageLabel
secondImageLabel: QLabel = window.secondImageLabel
outputImageLabel: QLabel = window.outputImageLabel
outputLabel: QLabel = window.outputLabel
inputLabel: QLabel = window.inputLabel

filters = {
    "Direct Mapping 0-order": dm_0,
    "Direct Mapping 1-Order": DM_1_order,
    "Reverse Mapping 0-Order": RM_0_order,
    "Convert to gray": cvt2gray,
    "Draw the histogram": histogram,
    "Contrast Adjustment": normalization,
    "Brightness Adjustment": DarkBright,
    "Power Law": powerLaw,
    "Histogram Equalization": histogramEqualization,
    "Histogram Matching": histogramMatching,
    "Add two images": add,
    "Subtract two images": sub,
    "Image negatives": negative,
    "Quantization": quantization,
    "Average Filter": average,
    "Weighted (Gaussian) Filter": weightedFilter,
    "Sharpening Filter": sharpening,
    "Edge Detection Filter": edgeDetection,
    "Unsharpened Filter": unsharp,
    "Ideal low pass filter": idealLowPassFilter,
    "Ideal high pass filter": idealHighPassFilter,
    "Butterworth low pass filter": butterworthLowPassFilter,
    "Butterworth high pass filter": butterworthHighPassFilter,
    "Gaussian low pass filter": gaussianLowPassFilter,
    "Gaussian high pass filter": gaussianHighPassFilter
}

def main():
    # Connect each button with the function that should be called when it is clicked
    applyPushButton.clicked.connect(window.applyClicked)
    clearPushButton.clicked.connect(window.clearClicked)
    chooseButton.clicked.connect(window.chooseClicked)
    chooseFirstButton.clicked.connect(window.chooseClicked)
    chooseSecondButton.clicked.connect(window.chooseClicked)
    # This executes whenever the user changes the selected item in the combo box
    filterComboBox.currentTextChanged.connect(window.filterChanged)

    applyPushButton.setDisabled(True)
    clearPushButton.setDisabled(True)

    checkThread = CheckThread()
    checkThread.start()

    # Show the window and display the app
    window.show()
    app.exec()

if __name__ == "__main__":
    main()