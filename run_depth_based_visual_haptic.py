import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QCursor, QIcon, QPixmap

from PIL import Image
import numpy as np

class VisualHapticImage(QLabel):
    def __init__(self, obj, color_image, depth_image, most_far_depth):
        super().__init__(obj)
        self.setMouseTracking(True)

        # Prepare depth image.
        self.depth_image = np.array(Image.open(depth_image))
        self.depth_image[self.depth_image < most_far_depth] = most_far_depth
        self.depth_image = (self.depth_image - np.min(self.depth_image)) / (np.max(self.depth_image) - np.min(self.depth_image)) * 255
        self.depth_image = self.depth_image.astype(np.int)

        # Prepare cursor images.
        cursor = QPixmap('left_ptr.png')
        self.scaled_cursors = [cursor.scaled(i * 0.8 + 10, i * 0.8 + 10) for i in range(1, 256)]

        # Prepare color image.
        pixmap = QPixmap(color_image)
        self.setPixmap(pixmap)
        self.resize(pixmap.width(),pixmap.height())

    def mouseMoveEvent(self, event):
        depth = self.depth_image[int(event.y()), int(event.x())]
        qcursor = QCursor(self.scaled_cursors[depth])
        self.setCursor(qcursor)

class VisualHapticExampleApp(QWidget):
    def __init__(self, color_image, depth_image, most_far_depth):
        super().__init__()
        self.label = VisualHapticImage(self, color_image, depth_image, most_far_depth)

        self.setWindowTitle("Visual Haptics Example")
        self.setGeometry(0,0, 2000, 1000)

        self.resize(self.label.width(),self.label.height())
        self.show()


import click

@click.command()
@click.option("--color-image")
@click.option("--depth-image")
@click.option("--most-far-depth", default=20000)
def main(color_image, depth_image, most_far_depth):
    app = QApplication(sys.argv)
    ex = VisualHapticExampleApp(color_image, depth_image, most_far_depth)
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()