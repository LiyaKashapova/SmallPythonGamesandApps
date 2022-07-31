from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QLabel, QPushButton, QListWidget, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import Qt  # Qt.KeepAspectRatio константа для зміни розмірів зі збереженням пропорцій
from PyQt5.QtGui import QPixmap, QIcon  # картинка оптимізована для відображення на екрані
from PIL import Image
from PIL.ImageFilter import SHARPEN
import os


class ImageProcessor:
    image = None
    dir = None
    filename = None

    def show_files(self):
        extensions = ['jpg', 'jpeg', 'png', 'gif', 'bmp']
        self.dir = QFileDialog.getExistingDirectory()
        filenames = [filename for filename in os.listdir(self.dir) if filename.split('.')[-1] in extensions]
        files.clear()
        for filename in filenames:
            files.addItem(filename)

    def show_image(self):
        if files.currentRow() > -1:
            self.filename = files.currentItem().text()
            i = os.path.join(self.dir, self.filename)
            self.image = Image.open(i)
            image_label.setPixmap(QPixmap(i).scaled(image_label.width(), image_label.height(), Qt.KeepAspectRatio))

    def save(self):
        path = os.path.join(self.dir, 'Modified/')
        i = os.path.join(path, self.filename)
        if not (os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        self.image.save(i)
        image_label.setPixmap(QPixmap(i).scaled(image_label.width(), image_label.height(), Qt.KeepAspectRatio))

    def left(self):
        if self.image:
            self.image = self.image.transpose(Image.Transpose.ROTATE_90)
            self.save()

    def right(self):
        if self.image:
            self.image = self.image.transpose(Image.Transpose.ROTATE_270)
            self.save()

    def flip(self):
        if self.image:
            self.image = self.image.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
            self.save()

    def sharpen(self):
        if self.image:
            self.image = self.image.filter(SHARPEN)
            self.save()

    def bw(self):
        if self.image:
            self.image = self.image.convert('L')
            self.save()


app = QApplication([])
w = QWidget()
w.setFixedSize(700, 500)
w.setWindowTitle('Easy Editor')
w.setWindowIcon(QIcon('brush.ico'))
btn_dir = QPushButton('Папка')
files = QListWidget()
image_label = QLabel()
btn_left = QPushButton('Ліво')
btn_right = QPushButton('Право')
btn_flip = QPushButton('Дзеркало')
btn_sharp = QPushButton('Різкість')
btn_bw = QPushButton('Ч/Б')

row = QHBoxLayout()
col1 = QVBoxLayout()
col2 = QVBoxLayout()
col1.addWidget(btn_dir)
col1.addWidget(files)
col2.addWidget(image_label, 95)
row_tools = QHBoxLayout()
row_tools.addWidget(btn_left)
row_tools.addWidget(btn_right)
row_tools.addWidget(btn_flip)
row_tools.addWidget(btn_sharp)
row_tools.addWidget(btn_bw)
col2.addLayout(row_tools, 5)
row.addLayout(col1, 20)
row.addLayout(col2, 80)
w.setLayout(row)

workimage = ImageProcessor()
btn_dir.clicked.connect(workimage.show_files)
files.itemClicked.connect(workimage.show_image)
btn_left.clicked.connect(workimage.left)
btn_right.clicked.connect(workimage.right)
btn_sharp.clicked.connect(workimage.sharpen)
btn_flip.clicked.connect(workimage.flip)
btn_bw.clicked.connect(workimage.bw)

w.show()
app.setStyle('Fusion')
app.exec()