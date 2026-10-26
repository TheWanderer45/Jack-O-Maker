from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys

class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        #Window
        self.setWindowTitle("Jack-O-Maker")
        self.setGeometry(100, 100, 800, 600)
        self.image = QImage(self.size(), QImage.Format_RGB32)
        self.image.fill(Qt.white)

        #Vars
        self.drawing = False
        self.brushSize = 2
        self.brushColor = Qt.gray

        self.lastPoint = QPoint()

        mainMenu = self.menuBar()

        fileMenu = mainMenu.addMenu("File")

        b_size = mainMenu.addMenu("Brush Size")

        b_color = mainMenu.addMenu("Brush Color")

        island_tools = mainMenu.addMenu("Island Tools")

        #Save action
        saveAction = QAction("Save", self)
        #Save shortcut
        saveAction.setShortcut("Ctrl+S")
        fileMenu.addAction(saveAction)
        saveAction.triggered.connect(self.save)

        #Load action
        loadAction = QAction("Load", self)
        fileMenu.addAction(loadAction)
        loadAction.triggered.connect(self.load)

        #clear
        clearAction = QAction("Clear", self)
        #Shortcut
        #clearAction.setShortcut("Ctrl+C")
        fileMenu.addAction(clearAction)
        clearAction.triggered.connect(self.clear)

        #Island check
        islandAction = QAction("Island Check", self)
        #Shortcut
        islandAction.setShortcut("Ctrl+I")
        island_tools.addAction(islandAction)
        islandAction.triggered.connect(self.island_check)

        #Brush sizes
        #4
        pix_4 = QAction("4px", self)
        b_size.addAction(pix_4)
        pix_4.triggered.connect(self.Pixel_4)
        #7
        pix_7 = QAction("7px", self)
        b_size.addAction(pix_7)
        pix_7.triggered.connect(self.Pixel_7)
        #9
        pix_9 = QAction("9px", self)
        b_size.addAction(pix_9)
        pix_9.triggered.connect(self.Pixel_9)
        #12
        pix_12 = QAction("12px", self)
        b_size.addAction(pix_12)
        pix_12.triggered.connect(self.Pixel_12)

        #Brush colors
        #grey
        grey = QAction("Grey", self)
        b_color.addAction(grey)
        grey.triggered.connect(self.greyColor)
        #white
        white = QAction("White", self)
        b_color.addAction(white)
        white.triggered.connect(self.whiteColor)

    #Check mouse clicks
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            #Update last point
            self.lastPoint = event.pos()

    #Track mouse movement
    def mouseMoveEvent(self, event):
        #Check if the left mouse button is pressed and the drawing flag is true
        if (event.buttons() & Qt.LeftButton) & self.drawing:
            #Create the painter object
            painter = QPainter(self.image)
            #Set the painter's pen
            painter.setPen(QPen(self.brushColor, self.brushSize, Qt.SolidLine, Qt. RoundCap, Qt.RoundJoin))
            #Draw a line from the last to the current points
            painter.drawLine(self.lastPoint, event.pos())

            #Update the last point
            self.lastPoint = event.pos()
            self.update()


    #On left mouse button release
    def mouseReleaseEvent(self, event):
        if event.button == Qt.LeftButton:
            self.drawing = False


    #Paint event
    def paintEvent(self, event):
        canvasPainter = QPainter(self)
        #Draw a rectangle
        canvasPainter.drawImage(self.rect(), self.image, self.image.rect())


    #Save
    def save(self):
        filePath, _ = QFileDialog.getSaveFileName(self, "Save Image", "", "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ")

        if filePath == "":
            return
        self.image.save(filePath)


    #Load
    def load(self):
        #filePath, _ = QFileDialog.getSaveFileName(self, "Load image", "", "PNG(*.png);;JPEG(*.jpg *.jpeg) ")
        filePath, _ = QFileDialog.getOpenFileName(self, "Load Image", "", "PNG(*.png);;JPEG(*.jpg *.jpeg) ")

        if filePath == "":
            return
        self.image.load(filePath)


    #Clear
    def clear(self):
        self.image.fill(Qt.white)
        self.update()


    #Change pixel sizes
    def Pixel_4(self):
        self.brushSize = 4
    def Pixel_7(self):
        self.brushSize = 7
    def Pixel_9(self):
        self.brushSize = 9
    def Pixel_12(self):
        self.brushSize = 12


    #Change brush color
    def greyColor(self):
        self.brushColor = Qt.gray
    def whiteColor(self):
        self.brushColor = Qt.white


    #Island Check Algorithm
    def island_check(self):
        #Draw white borders
        image = self.image
        painter = QPainter(image)
        painter.setPen(QPen(Qt.white, 2))
        painter.drawLine(0, 0, image.width(), 0) #Top
        painter.drawLine(0, 0, 0, image.height()) #Left
        painter.drawLine(image.width()-1, 0, image.width()-1, image.height()) #Right
        painter.drawLine(0, image.height()-1, image.width(), image.height()-1) #Bottom
        self.update()

        #Flood fill
        def flood_fill(x, y, fill_color):
            #Convert image to bytes
            w, h = image.width(), image.height()
            s = image.bits().asstring(w * h * 4)
            
            #Get 3-byte value of a given pixel
            def get_pixel(x1, y1):
                i = (x1 + (y1 * w)) * 4
                return s[i:i+3]
            target_color = get_pixel(x, y)

            #Search & Fill
            #painter = QPainter(image)
            painter.setPen(QPen(fill_color))
            
            have_seen = set()
            queue = [(x, y)]

            def get_cardinal_points(have_seen, center_pos):
                points = []
                cx, cy = center_pos
                for x2, y2 in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
                    xx, yy = cx +x2, cy + y2
                    if (xx >= 0 and xx < w and yy >= 0 and yy < h and (xx, yy) not in have_seen):
                        points.append((xx, yy))
                        have_seen.add((xx, yy))
                return points

            while queue:
                x, y = queue.pop()
                if get_pixel(x, y) == target_color:
                    painter.drawPoint(QPoint(x, y))
                    queue.extend(get_cardinal_points(have_seen, (x, y)))

            self.update()

        def search_and_fill(color_search: QColor, color_replace: QColor):
            for y in range(image.height()):
                for x in range(image.width()):
                    if image.pixelColor(x, y) == color_search:
                        flood_fill(x, y, color_replace)

        #Reset red pixels
        search_and_fill(Qt.red, Qt.white)
        #Flood fill once
        flood_fill(0, 0, Qt.blue)
        #Check for remaining white pixels and replace with red pixels
        search_and_fill(Qt.white, Qt.red)
        #for y in range(image.height()):
        #    for x in range(image.width()):
        #        if image.pixelColor(x, y) == Qt.white:
        #            flood_fill(x, y, Qt.red)
        #Reset blue pixels back to white
        flood_fill(0, 0, Qt.white)


App = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(App.exec())
