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
    save_dir = "Modified/"

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
            self.image = Image.open(os.path.join(self.dir, self.filename))
            draw_image(os.path.join(self.dir, workimage.filename))

    def save(self):
        path = os.path.join(self.dir, self.save_dir)
        if not (os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        fullname = os.path.join(path, self.filename)
        self.image.save(fullname)

    def bw(self):
        if self.image:
            self.image = self.image.convert("L")
            self.save()
            image_path = os.path.join(self.dir, self.save_dir, self.filename)
            draw_image(image_path)

    def left(self):
        if self.image:
            self.image = self.image.transpose(Image.Transpose.ROTATE_90)
            self.save()
            image_path = os.path.join(self.dir, self.save_dir, self.filename)
            draw_image(image_path)

    def right(self):
        if self.image:
            self.image = self.image.transpose(Image.Transpose.ROTATE_270)
            self.save()
            image_path = os.path.join(self.dir, self.save_dir, self.filename)
            draw_image(image_path)

    def flip(self):
        if self.image:
            self.image = self.image.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
            self.save()
            image_path = os.path.join(self.dir, self.save_dir, self.filename)
            draw_image(image_path)

    def sharpen(self):
        if self.image:
            self.image = self.image.filter(SHARPEN)
            self.save()
            image_path = os.path.join(self.dir, self.save_dir, self.filename)
            draw_image(image_path)


def draw_image(path):
    image.hide()
    image.setPixmap(QPixmap(path).scaled(image.width(), image.height(), Qt.KeepAspectRatio))
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
col2.addWidget(image, 95, alignment=Qt.AlignHCenter)
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

workimage = ImageProcessor()
files.currentRowChanged.connect(workimage.show_image)
btn_dir.clicked.connect(workimage.show_files)
btn_bw.clicked.connect(workimage.bw)
btn_left.clicked.connect(workimage.left)
btn_right.clicked.connect(workimage.right)
btn_sharp.clicked.connect(workimage.sharpen)
btn_flip.clicked.connect(workimage.flip)

w.show()
app.setStyle('Fusion')
app.exec()