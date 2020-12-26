from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt, QPoint
from Code.config import buttonWindowClose as bWC
from Code.config import buttonWindowHide as bWH


class MyBar(QWidget):

    def __init__(self, parent):
        super(MyBar, self).__init__()
        self.parent = parent
        self.layout = QHBoxLayout()
        self.title = QLabel()
        self.btn_close = QPushButton("x")
        self.btn_min = QPushButton("-")
        self.pressing = False
        self.start = QPoint(0, 0)
        self.end = 0
        self.movement = 0
        self.button()

        self.btn_close.clicked.connect(self.btn_close_clicked)
        self.btn_min.clicked.connect(self.btn_min_clicked)

    def button(self):
        self.layout.setContentsMargins(0, 0, 0, 0)

        btn_size = 35

        self.btn_close.setFixedSize(btn_size, btn_size)
        self.btn_close.setStyleSheet(bWC)

        self.btn_min.setFixedSize(btn_size, btn_size)
        self.btn_min.setStyleSheet(bWH)

        self.title.setFixedHeight(35)
        self.title.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.btn_min)
        self.layout.addWidget(self.btn_close)

        self.title.setStyleSheet("""
            color: white;""")
        self.setLayout(self.layout)

    def resizeEvent(self, event):
        super(MyBar, self).resizeEvent(event)

    def mousePressEvent(self, event):
        self.start = self.mapToGlobal(event.pos())
        self.pressing = True

    def mouseMoveEvent(self, event):
        if self.pressing:
            self.end = self.mapToGlobal(event.pos())
            self.movement = self.end - self.start
            self.parent.setGeometry(self.mapToGlobal(self.movement).x(),
                                    self.mapToGlobal(self.movement).y(),
                                    self.parent.width(),
                                    self.parent.height())
            self.start = self.end

    def mouseReleaseEvent(self, event):
        self.pressing = False

    def btn_close_clicked(self):
        self.parent.close()

    def btn_min_clicked(self):
        self.parent.showMinimized()
