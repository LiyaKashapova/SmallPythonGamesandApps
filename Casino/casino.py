from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout
from random import randint

app = QApplication([])
w = QWidget()
w.setWindowTitle('Визначення переможця')
w.resize(400, 200)

b = QPushButton('Сгенерувати')
t = QLabel('Натисни для генерації')
n1 = QLabel('?')
n2 = QLabel('?')

l = QVBoxLayout()
l.addWidget(t, alignment=Qt.AlignCenter)
l.addWidget(n1, alignment=Qt.AlignCenter)
l.addWidget(n2, alignment=Qt.AlignCenter)
l.addWidget(b, alignment=Qt.AlignCenter)
w.setLayout(l)


def show():
    t1 = randint(0, 9)
    t2 = randint(0, 9)
    n1.setText(str(t1))
    n2.setText(str(t2))
    if t1 == t2:
        t.setText('Ви виграли, спробуйте знову!')
    else:
        t.setText('Ви програли, спробуйте знову!')


b.clicked.connect(show)
w.show()
app.exec_()