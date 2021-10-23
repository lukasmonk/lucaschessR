from random import randrange
from PySide2 import QtCore, QtGui, QtWidgets

class Example(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        layout = QtWidgets.QGridLayout(self)
        self.startButton = QtWidgets.QPushButton("Start")
        layout.addWidget(self.startButton)
        self.addPointButton = QtWidgets.QPushButton("Add target point")
        layout.addWidget(self.addPointButton, 0, 1)

        self.view = QtWidgets.QGraphicsView()
        layout.addWidget(self.view, 1, 0, 1, 2)
        self.scene = QtWidgets.QGraphicsScene()
        self.view.setScene(self.scene)
        self.scene.setSceneRect(-10, -10, 640, 480)

        pen = QtGui.QPen(QtCore.Qt.darkBlue, 5)
        self.ellipse = self.scene.addEllipse(0, 0, 10, 10, pen)

        self.queue = []

        self.startButton.clicked.connect(self.begin)
        self.addPointButton.clicked.connect(self.addPoint)
        self.anim = QtCore.QVariantAnimation()
        self.anim.setDuration(1000)
        self.anim.valueChanged.connect(self.ellipse.setPos)
        self.anim.setStartValue(self.ellipse.pos())
        self.anim.finished.connect(self.checkPoint)

    def begin(self):
        self.startButton.setEnabled(False)
        self.addPoint()

    def addPoint(self):
        self.queue.append(QtCore.QPointF(randrange(600), randrange(400)))
        self.checkPoint()

    def checkPoint(self):
        if not self.anim.state() and self.queue:
            if self.anim.currentValue():
                # a valid currentValue is only returned when the animation has
                # been started at least once
                self.anim.setStartValue(self.anim.currentValue())
            self.anim.setEndValue(self.queue.pop(0))
            self.anim.start()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ex = Example()
    ex.show()
    app.exec_()