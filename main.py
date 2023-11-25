import os
from PyQt5.QtWidgets import (
   QApplication, QWidget,
   QLabel, QPushButton, QListWidget,
   QHBoxLayout, QVBoxLayout, QFileDialog
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PIL.ImageFilter import (
   BLUR, CONTOUR, DETAIL, EDGE_ENHANCE, EDGE_ENHANCE_MORE,
   EMBOSS, FIND_EDGES, SMOOTH, SMOOTH_MORE, SHARPEN,
   GaussianBlur, UnsharpMask
)

from PIL import Image, ImageFilter


app = QApplication([])
win = QWidget()
win.resize(700,500)
win.setWindowTitle("easy editor")
lb_image = QLabel("Картина")
btn_dir = QPushButton('Папка')
lw_files =  QListWidget()

btn_left=QPushButton("left")
btn_right=QPushButton("Right")
btn_flip=QPushButton("Flip")
btn_sharp = QPushButton("Sharp")
btn_bw = QPushButton("blackWhite")
btn_blured = QPushButton("blured")

row = QHBoxLayout()
col1=QVBoxLayout()
col2=QVBoxLayout()
col1.addWidget(btn_dir)
col1.addWidget(lw_files)
col2.addWidget(lb_image)
row_tools=QHBoxLayout()
row_tools.addWidget(btn_left)
row_tools.addWidget(btn_right)
row_tools.addWidget(btn_flip)
row_tools.addWidget(btn_sharp)
row_tools.addWidget(btn_bw)
row_tools.addWidget(btn_blured)
col2.addLayout(row_tools)

row.addLayout(col1)
row.addLayout(col2)
win.setLayout(row)

win.show()

workdir = ""

def filter(files,extensions):
    result = []
    for filename in files:
        for ext in extensions:
            if filename.endswith(ext):
                result.append(filename)

    return result

def chooseWorkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()

def showFilenamesList():
    extensions=['.jpg','.jpeg','.png','.gif','.bmp']
    chooseWorkdir()
    filenames = filter(os.listdir(workdir),extensions)
    lw_files.clear()
    for filename in filenames:
        lw_files.addItem(filename)

btn_dir.clicked.connect(showFilenamesList)

class ImageProcessor():
    def __init__(self):
        self.image = None
        self.dir = None
        self.filename = None
        self.save_dir='black ni/'

    def loadImage(self,dir,filename):
        self.dir = dir
        self.filename = filename
        image_path = os.path.join(dir,filename)
        self.image = Image.open(image_path)

    def do_bw(self):
        self.image = self.image.convert('L')
        self.saveImage()
        image_path = os.path.join(self.dir,self.save_dir,self.filename)
        self.showImage(image_path)

    def do_sharp(self):
        self.image = self.image.filter(SHARPEN)
        self.saveImage()
        image_path = os.path.join(self.dir,self.save_dir,self.filename)
        self.showImage(image_path)

    def do_flip(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path = os.path.join(self.dir,self.save_dir,self.filename)
        self.showImage(image_path)   

    def do_left(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        image_path = os.path.join(self.dir,self.save_dir,self.filename)
        self.showImage(image_path) 

    def do_right(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        image_path = os.path.join(self.dir,self.save_dir,self.filename)
        self.showImage(image_path)      

    def do_blured(self):
        self.image = self.image.filter(ImageFilter.BLUR)
        self.saveImage()
        image_path = os.path.join(self.dir,self.save_dir,self.filename)
        self.showImage(image_path)      

    def saveImage(self):
        path = os.path.join(self.dir, self.save_dir)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        image_path = os.path.join(path, self.filename)
        self.image.save(image_path)

    def showImage(self, path):
        lb_image.hide()
        pixmapimage=QPixmap(path)
        w,h=lb_image.width(),lb_image.height()
        pixmapimage = pixmapimage.scaled(w,h, Qt.KeepAspectRatio)
        lb_image.setPixmap(pixmapimage)
        lb_image.show()

workimage = ImageProcessor()

def showChoseImage():
    if lw_files.currentRow() >= 0:
        filename=lw_files.currentItem().text()
        workimage.loadImage(workdir,filename)
        image_path = os.path.join(workimage.dir,workimage.filename)
        workimage.showImage(image_path)
lw_files.currentRowChanged.connect(showChoseImage)
btn_bw.clicked.connect(workimage.do_bw)
btn_flip.clicked.connect(workimage.do_flip)
btn_left.clicked.connect(workimage.do_left)
btn_right.clicked.connect(workimage.do_right)
btn_sharp.clicked.connect(workimage.do_sharp)
btn_blured.clicked.connect(workimage.do_blured)
app.exec()
