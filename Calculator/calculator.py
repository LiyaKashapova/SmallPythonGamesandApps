from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QFont, QIcon
from pygame import *

app = QApplication([])
s = QWidget()
s.resize(370, 600)
s.setWindowTitle('Calculator')
s.setWindowIcon(QIcon('calculator.png'))
s.show()
main = QVBoxLayout()

mixer.init()
hit = mixer.Sound('click.mp3')
hit.set_volume(0.4)

enter = QLabel('')
font = QFont()
font.setFamily('Arial')
font.setPointSize(15)
enter.setFont(font)
result = QLabel('')
result.setFont(font)

b = {
    '1': QPushButton('1'), '0': QPushButton('0'), '2': QPushButton('2'), '3': QPushButton('3'), '4': QPushButton('4'),
    '5': QPushButton('5'), '6': QPushButton('6'), '7': QPushButton('7'), '8': QPushButton('8'), '9': QPushButton('9'),
    'ac': QPushButton('AC'), '.': QPushButton('.'), '*': QPushButton('*'), '/': QPushButton('/'), '-': QPushButton('-'),
    '+': QPushButton('+'), '=': QPushButton('='), '(': QPushButton('('), ')': QPushButton(')')
}

hl1 = QHBoxLayout()  # AC, (, ), /
hl2 = QHBoxLayout()  # 7, 8, 9, *
hl3 = QHBoxLayout()  # 4, 5, 6, -
hl4 = QHBoxLayout()  # 1, 2, 3, +
hl5 = QHBoxLayout()  # 0, ., =

hl1.addWidget(b['ac'])
hl1.addWidget(b['('])
hl1.addWidget(b[')'])
hl1.addWidget(b['/'])

hl2.addWidget(b['7'])
hl2.addWidget(b['8'])
hl2.addWidget(b['9'])
hl2.addWidget(b['*'])

hl3.addWidget(b['4'])
hl3.addWidget(b['5'])
hl3.addWidget(b['6'])
hl3.addWidget(b['-'])

hl4.addWidget(b['1'])
hl4.addWidget(b['2'])
hl4.addWidget(b['3'])
hl4.addWidget(b['+'])

hl5.addWidget(b['0'])
hl5.addWidget(b['.'])
hl5.addWidget(b['='])

main.addWidget(enter, alignment=Qt.AlignRight)
main.addWidget(result, alignment=Qt.AlignCenter)
main.addLayout(hl1)
main.addLayout(hl2)
main.addLayout(hl3)
main.addLayout(hl4)
main.addLayout(hl5)
s.setLayout(main)

symbols = ['+', '-', '*', '/', '.']


def check():
    exp = enter.text()
    if len(exp) > 1:
        # Першим або останнім був оператор
        if exp[0] in symbols or exp[-1] in symbols:
            return False
        # Якщо 2 оператори підряд
        for i in range(len(exp)-1):
            if exp[i] in symbols and exp[i+1] in symbols:
                return False
        # Якщо не парна кількість дужок ( != )
        if exp.count('(') != exp.count(')'):
            return False
        # Якщо дужки переплутані )(
        if exp.find(')') < exp.find('('):
            return False
        # Якщо дужки пусті ()
        for i in range(len(exp) - 1):
            if exp[i] == '(' and exp[i + 1] == ')':
                return False
        # Якщо число перед дужкою
            if exp[i] not in symbols and exp[i + 1] == '(':
                return False
        # Якщо після символа стоїть знак, крім -
            if not exp[i].isdigit() and exp[i + 1] in symbols and exp[i + 1] != '-':
                return False
        # Коли / 0
            if exp[i] == '/' and exp[i + 1] == '0':
                return False
    return True


def addsymb(button):
    hit.play()
    e = enter.text()
    b = button.text()
    if b == 'AC':
        enter.setText(e[:-1])
        return
    if len(e) < 25:
        if b == '=':
            if check():
                result.setText(str(eval(enter.text())))
            else:
                result.setText('Error')
            return
    enter.setText(e + b)


for k in b.keys():
    b[k].setMaximumWidth(70)
    b[k].setMinimumHeight(70)
    if k.isdigit():
        b[k].setStyleSheet('background-color: lightgrey')
    elif k == '=':
        b[k].setStyleSheet('background-color: darkslateblue')
    elif k == '.' or k == '(' or k == ')':
        b[k].setStyleSheet('background-color: darkgrey')
    else:
        b[k].setStyleSheet('background-color: lightsteelblue')
    b[k].clicked.connect(lambda checked, button=b[k]: addsymb(button))

b['0'].setMaximumWidth(155)
app.setStyle('Fusion')
app.exec()