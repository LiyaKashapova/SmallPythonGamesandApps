import os
from PyQt5.QtWidgets import (
    QApplication, QWidget,
    QFileDialog,
    QLabel, QPushButton, QListWidget,
    QHBoxLayout, QVBoxLayout
)
from PyQt5.QtCore import Qt  # нужна константа Qt.KeepAspectRatio для изменения размеров с сохранением пропорций
from PyQt5.QtGui import QPixmap, QIcon  # оптимизированная для показа на экране картинка

from PIL import Image
from PIL.ImageQt import ImageQt
from PIL import ImageFilter
from PIL.ImageFilter import (
    BLUR, CONTOUR, DETAIL, EDGE_ENHANCE, EDGE_ENHANCE_MORE,
    EMBOSS, FIND_EDGES, SMOOTH, SMOOTH_MORE, SHARPEN,
    GaussianBlur, UnsharpMask
)


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


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
        self.image = self.image.convert("L")
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.show(image_path)

    def left(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.show(image_path)

    def right(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.show(image_path)

    def flip(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.show(image_path)

    def sharpen(self):
        self.image = self.image.filter(SHARPEN)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.show(image_path)

    def show(self, path):
        image.hide()
        pix = QPixmap(path)
        w, h = image.width(), image.height()
        pix = pix.scaled(w, h, Qt.KeepAspectRatio)
        image.setPixmap(pix)
        image.show()


def filter(fs, extensions):
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
    filenames = filter(os.listdir(workdir), extensions)
    files.clear()
    for filename in filenames:
        files.addItem(filename)


def show_image():
    if files.currentRow() >= 0:
        filename = files.currentItem().text()
        workimage.load(filename)
        workimage.show(os.path.join(workdir, workimage.filename))


app = QApplication([])
win = QWidget()
win.resize(700, 500)
win.setWindowTitle('Easy Editor')
win.setWindowIcon(QIcon(resource_path('brush.ico')))
image = QLabel("Картинка")
btn_dir = QPushButton("Папка")
files = QListWidget()
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
win.setLayout(row)

workdir = ''

btn_dir.clicked.connect(show_files)

workimage = ImageProcessor()
files.currentRowChanged.connect(show_image)

btn_bw.clicked.connect(workimage.bw)
btn_left.clicked.connect(workimage.left)
btn_right.clicked.connect(workimage.right)
btn_sharp.clicked.connect(workimage.sharpen)
btn_flip.clicked.connect(workimage.flip)

win.show()
app.exec()
