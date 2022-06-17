from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QLabel, QPushButton, QListWidget, QHBoxLayout, \
    QVBoxLayout, QStyle
from PyQt5.QtCore import Qt  # Qt.KeepAspectRatio константа для зміни розмірів зі збереженням пропорцій
from PyQt5.QtGui import QPixmap, QIcon  # картинка оптимізована для відображення на екрані
from PIL import Image
from PIL.ImageFilter import SHARPEN
import os


class ImageProcessor:
    def __init__(self):
        self.image = None
        self.dir = None
        self.filename = None
        self.save_dir = "Modified/"

    def load(self, filename):
        self.filename = filename
        fullname = os.path.join(workdir, filename)
        self.image = Image.open(fullname)

    def save(self):
        path = os.path.join(workdir, self.save_dir)
        if not (os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        fullname = os.path.join(path, self.filename)
        self.image.save(fullname)

    def bw(self):
        if self.image:
            self.image = self.image.convert("L")
            self.save()
            image_path = os.path.join(workdir, self.save_dir, self.filename)
            draw_image(image_path)

    def left(self):
        if self.image:
            self.image = self.image.transpose(Image.Transpose.ROTATE_90)
            self.save()
            image_path = os.path.join(workdir, self.save_dir, self.filename)
            draw_image(image_path)

    def right(self):
        if self.image:
            self.image = self.image.transpose(Image.Transpose.ROTATE_270)
            self.save()
            image_path = os.path.join(workdir, self.save_dir, self.filename)
            draw_image(image_path)

    def flip(self):
        if self.image:
            self.image = self.image.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
            self.save()
            image_path = os.path.join(workdir, self.save_dir, self.filename)
            draw_image(image_path)

    def sharpen(self):
        if self.image:
            self.image = self.image.filter(SHARPEN)
            self.save()
            image_path = os.path.join(workdir, self.save_dir, self.filename)
            draw_image(image_path)


def filter_files(fs, extensions):
    result = []
    for filename in fs:
        for ext in extensions:
            if filename.endswith(ext):
                result.append(filename)
    return result


def choose_dir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()


def show_files():
    extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
    choose_dir()
    filenames = filter_files(os.listdir(workdir), extensions)
    files.clear()
    for filename in filenames:
        files.addItem(filename)


def show_image():
    if files.currentRow() >= 0:
        filename = files.currentItem().text()
        workimage.load(filename)
        draw_image(os.path.join(workdir, workimage.filename))


def draw_image(path):
    image.hide()
    pix = QPixmap(path)
    w, h = image.width(), image.height()
    pix = pix.scaled(w, h, Qt.KeepAspectRatio)
    image.setPixmap(pix)
    image.show()


app = QApplication([])
w = QWidget()
w.resize(700, 500)
w.setWindowTitle('Easy Editor')
w.setWindowIcon(QIcon('brush.ico'))
btn_dir = QPushButton("Папка")
files = QListWidget()
image = QLabel("Картинка")
btn_left = QPushButton("Ліво")
btn_right = QPushButton("Право")
btn_flip = QPushButton("Дзеркало")
btn_sharp = QPushButton("Різкість")
btn_bw = QPushButton("Ч/Б")

row = QHBoxLayout()
col1 = QVBoxLayout()
col2 = QVBoxLayout()
col1.addWidget(btn_dir)
col1.addWidget(files)
col2.addWidget(image, 95)
row_tools = QHBoxLayout()
row_tools.addWidget(btn_left)
row_tools.addWidget(btn_right)
row_tools.addWidget(btn_flip)
row_tools.addWidget(btn_sharp)
row_tools.addWidget(btn_bw)
col2.addLayout(row_tools)

row.addLayout(col1, 20)
row.addLayout(col2, 80)
w.setLayout(row)

workdir = ''
workimage = ImageProcessor()
files.currentRowChanged.connect(show_image)
btn_dir.clicked.connect(show_files)
btn_bw.clicked.connect(workimage.bw)
btn_left.clicked.connect(workimage.left)
btn_right.clicked.connect(workimage.right)
btn_sharp.clicked.connect(workimage.sharpen)
btn_flip.clicked.connect(workimage.flip)

w.show()
app.setStyle('Fusion')
app.exec()
