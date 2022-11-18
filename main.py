import sys
import sqlite3

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from qcrop.ui import QCrop


# ╔════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
# ║Блок авторизации                                                                                                    ║
# ╚════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╝


class Authorization(QDialog):
    def __init__(self):
        super().__init__()
        self.setupUi()
        self.pushButtonSingUp.clicked.connect(self.singUp)
        self.pushButtonLogin.clicked.connect(self.login)
        self.dataBase = "files/scm.db"

    def setupUi(self):
        self.setWindowTitle('Авторизацию')
        self.setObjectName("Dialog")
        self.resize(240, 189)
        self.tabWidget = QTabWidget(self)
        self.tabWidget.setGeometry(QRect(0, 0, 241, 191))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QWidget()
        self.tab.setObjectName("tab")
        self.pushButtonSingUp = QPushButton(self.tab)
        self.pushButtonSingUp.setGeometry(QRect(50, 100, 141, 28))
        self.pushButtonSingUp.setObjectName("pushButtonSingUp")
        self.lineEditName = QLineEdit(self.tab)
        self.lineEditName.setGeometry(QRect(10, 10, 211, 22))
        self.lineEditName.setObjectName("lineEditName")
        self.lineEditLogin1 = QLineEdit(self.tab)
        self.lineEditLogin1.setGeometry(QRect(10, 40, 211, 22))
        self.lineEditLogin1.setObjectName("lineEditLogin1")
        self.lineEditPassword1 = QLineEdit(self.tab)
        self.lineEditPassword1.setGeometry(QRect(10, 70, 211, 22))
        self.lineEditPassword1.setObjectName("lineEditPassword1")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName("tab_2")
        self.pushButtonLogin = QPushButton(self.tab_2)
        self.pushButtonLogin.setGeometry(QRect(70, 80, 101, 28))
        self.pushButtonLogin.setObjectName("pushButtonLogin")
        self.lineEditLogin2 = QLineEdit(self.tab_2)
        self.lineEditLogin2.setGeometry(QRect(10, 10, 211, 22))
        self.lineEditLogin2.setObjectName("lineEditLogin2")
        self.lineEditPassword2 = QLineEdit(self.tab_2)
        self.lineEditPassword2.setGeometry(QRect(10, 40, 211, 22))
        self.lineEditPassword2.setObjectName("lineEditPassword2")
        self.labelOut = QLabel(self.tab_2)
        self.labelOut.setGeometry(QRect(0, 110, 241, 16))
        self.labelOut.setText("")
        self.labelOut.setObjectName("labelOut")
        self.tabWidget.addTab(self.tab_2, "")

        self.retranslateUi()
        self.tabWidget.setCurrentIndex(1)
        QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QCoreApplication.translate
        self.setWindowTitle(_translate("Dialog", "Dialog"))
        self.pushButtonSingUp.setText(_translate("Dialog", "Зарегистрироваться"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Dialog", "Регистрация"))
        self.pushButtonLogin.setText(_translate("Dialog", "Войти"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Dialog", "Вход"))

    def singUp(self):
        self.con = sqlite3.connect("scm.db")
        self.cur = self.con.cursor()
        name, login, password = self.lineEditName.text(), self.lineEditLogin1.text(), self.lineEditPassword1.text()
        if not name or not login or not password:
            return
        try:
            ex = self.cur.execute(f"""INSERT INTO users (login, password, name) 
                                  VALUES {login, password, name}""").fetchall()
        except sqlite3.IntegrityError:
            return
        self.con.commit()
        self.con.close()

    def login(self):
        self.con = sqlite3.connect("scm.db")
        self.cur = self.con.cursor()
        try:
            login, password = self.lineEditLogin2.text(), self.lineEditPassword2.text()
            print(login, password)
            user1 = self.cur.execute(f"""SELECT name, login FROM users
                                        WHERE login = '{login}'""").fetchone()
            print(user1)
            user2 = self.cur.execute(f"""SELECT name, login FROM users
                                      WHERE password = '{password}'""").fetchone()
            print(user2)
            try:
                if user1 == user2:
                    self.labelOut.setText(f"Добро пожаловать, {user1[0]}")
            except TypeError:
                self.labelOut.setText("Нет такого пользователя")
            self.con.commit()
            self.con.close()
        except sqlite3.OperationalError:
            self.labelOut.setText("Нет такого пользователя")


# ╔════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
# ║Блок сохранения                                                                                                     ║
# ╚════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╝


class Saving(QDialog):
    def __init__(self, pixmap):
        super().__init__()
        self.setupUi(self)
        self.pixmap = pixmap
        self.spinBoxSizeX.setMaximum(2147483647)
        self.spinBoxSizeY.setMaximum(2147483647)
        self.toolButtonSave.clicked.connect(self.save)

    def setupUi(self, Saving):
        Saving.setObjectName("Saving")
        Saving.resize(240, 320)
        self.label_2 = QLabel(Saving)
        self.label_2.setGeometry(QRect(10, 0, 221, 21))
        self.label_2.setObjectName("label_2")
        self.spinBoxSizeX = QSpinBox(Saving)
        self.spinBoxSizeX.setGeometry(QRect(10, 30, 221, 22))
        self.spinBoxSizeX.setObjectName("spinBoxSizeX")
        self.spinBoxSizeY = QSpinBox(Saving)
        self.spinBoxSizeY.setGeometry(QRect(10, 50, 221, 22))
        self.spinBoxSizeY.setObjectName("spinBoxSizeY")
        self.label_3 = QLabel(Saving)
        self.label_3.setGeometry(QRect(10, 80, 121, 21))
        self.label_3.setObjectName("label_3")
        self.comboBoxRotate = QComboBox(Saving)
        self.comboBoxRotate.setGeometry(QRect(10, 110, 221, 22))
        self.comboBoxRotate.setObjectName("comboBoxRotate")
        self.comboBoxRotate.addItem("")
        self.comboBoxRotate.addItem("")
        self.comboBoxRotate.addItem("")
        self.comboBoxRotate.addItem("")
        self.toolButtonSave = QToolButton(Saving)
        self.toolButtonSave.setGeometry(QRect(160, 270, 71, 31))
        self.toolButtonSave.setObjectName("toolButtonSave")

        self.retranslateUi(Saving)
        QMetaObject.connectSlotsByName(Saving)

    def retranslateUi(self, Saving):
        _translate = QCoreApplication.translate
        Saving.setWindowTitle(_translate("Saving", "Сохранение"))
        self.label_2.setText(_translate("Saving", "Изменить размер"))
        self.label_3.setText(_translate("Saving", "Повернуть"))
        self.comboBoxRotate.setItemText(0, _translate("Saving", "Исходное изображение"))
        self.comboBoxRotate.setItemText(1, _translate("Saving", "Повернуть на 90 градусов"))
        self.comboBoxRotate.setItemText(2, _translate("Saving", "Повернуть на 180 градусов"))
        self.comboBoxRotate.setItemText(3, _translate("Saving", "Повернуть на 270 градусов"))
        self.toolButtonSave.setText(_translate("Saving", "Сохранить"))

    def save(self):
        sizeX, sizeY = self.spinBoxSizeX.value(), self.spinBoxSizeY.value()
        if sizeX == 0:
            sizeX = self.pixmap.width()
        if sizeY == 0:
            sizeY = self.pixmap.height()
        rotation = 0
        if self.comboBoxRotate.currentText() == "Повернуть на 90 градусов":
            rotation = 90
        elif self.comboBoxRotate.currentText() == "Повернуть на 180 градусов":
            rotation = 180
        elif self.comboBoxRotate.currentText() == "Повернуть на 270 градусов":
            rotation = 270
        transform = QTransform().rotate(rotation)
        self.pixmap = self.pixmap.transformed(transform, Qt.SmoothTransformation)

        self.pixmap = self.pixmap.scaled(sizeX, sizeY, Qt.IgnoreAspectRatio)

        filePath = QFileDialog.getSaveFileName(self, "Сохранить картинку", "", "(*.png);;(*.jpg *.jpeg);;All Files(*.*)")[0]
        self.pixmap.save(filePath)



class MainWindow(QMainWindow):
# ╔════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
# ║Блок инициализации                                                                                                  ║
# ╚════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╝

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.setWindowIcon(QIcon("files/Icons/troll.png"))

        self.scale = 1
        self.file = None
        self.drawingFlag = False
        self.pipetteFlag = False
        self.grabFlag = False
        self.color = Qt.black
        self.pen = QPen(self.color)
        self.brush = QBrush()
        self.brushWidth = 0
        self.labelCoordX = 0
        self.labelCoordY = 102
        self.shape = "Кисть"
        self.startPoint = QPoint()
        self.endPoint = QPoint()
        self.text = ""

        self.toolButtonSave.clicked.connect(self.saveFile)
        self.shortcutLoad = QShortcut(QKeySequence("Ctrl+S"), self)
        self.shortcutLoad.activated.connect(self.saveFile)

        self.toolButtonLoad.clicked.connect(self.openFile)
        self.shortcutLoad = QShortcut(QKeySequence("Ctrl+L"), self)
        self.shortcutLoad.activated.connect(self.openFile)

        self.toolButtonCanvas.clicked.connect(self.createCanvas)

        self.toolButtonCrop.clicked.connect(self.crop)

        self.toolButtonZoom1.clicked.connect(self.scaleImageBigger)
        self.toolButtonZoom2.clicked.connect(self.scaleImageSmaller)

        self.toolButtonReturn.clicked.connect(self.scaleImageReturn)
        self.shortcutReturn = QShortcut(QKeySequence("Ctrl+Z"), self)
        self.shortcutReturn.activated.connect(self.scaleImageReturn)

        self.toolButtonColorChoose.clicked.connect(self.chooseColor)
        self.shortcutReturn = QShortcut(QKeySequence("Ctrl+C"), self)
        self.shortcutReturn.activated.connect(self.chooseColor)

        self.toolButtonPaint.clicked.connect(self.changeDrawingFlag)
        self.shortcutReturn = QShortcut(QKeySequence("Ctrl+P"), self)
        self.shortcutReturn.activated.connect(self.changeDrawingFlag)

        self.toolButtonErase.clicked.connect(self.clearMap)

        self.toolButtonText.clicked.connect(self.setText)

        self.spinBoxWidth.valueChanged.connect(self.editPenWidth)

        self.toolButtonAuth.clicked.connect(self.auth)

        self.comboBoxShape.currentTextChanged.connect(self.choseShape)

        self.setMouseTracking(True)

        self.initUI()

    def initUI(self):
        self.setWindowTitle('MemeCreator++')
        self.pixmap = QPixmap(self.file)

        self.width = self.pixmap.width()
        self.height = self.pixmap.height()
        self.startWidth = self.pixmap.width()
        self.startHeight = self.pixmap.height()

        self.labelSize.setText(f"{self.width}x{self.height}")
        self.labelImage.resize(self.width, self.height)

    def setupUi(self, MemeCreator):
        MemeCreator.setObjectName("MemeCreator")
        MemeCreator.resize(1925, 1035)
        self.centralwidget = QWidget(MemeCreator)
        self.centralwidget.setObjectName("centralwidget")
        self.lineh2 = QFrame(self.centralwidget)
        self.lineh2.setGeometry(QRect(0, 101, 1921, 3))
        self.lineh2.setFrameShape(QFrame.HLine)
        self.lineh2.setFrameShadow(QFrame.Sunken)
        self.lineh2.setObjectName("lineh2")
        self.labelImage = QLabel(self.centralwidget)
        self.labelImage.setGeometry(QRect(0, 102, 81, 81))
        self.labelImage.setText("")
        self.labelImage.setObjectName("labelImage")
        self.toolButtonZoom2 = QToolButton(self.centralwidget)
        self.toolButtonZoom2.setGeometry(QRect(250, 10, 51, 22))
        self.toolButtonZoom2.setObjectName("toolButtonZoom2")
        self.buttonGroup_2 = QButtonGroup(MemeCreator)
        self.buttonGroup_2.setObjectName("buttonGroup_2")
        self.buttonGroup_2.addButton(self.toolButtonZoom2)
        self.labelCoords = QLabel(self.centralwidget)
        self.labelCoords.setGeometry(QRect(320, 10, 351, 21))
        self.labelCoords.setText("")
        self.labelCoords.setObjectName("labelCoords")
        self.toolButtonReturn = QToolButton(self.centralwidget)
        self.toolButtonReturn.setGeometry(QRect(200, 31, 51, 22))
        self.toolButtonReturn.setObjectName("toolButtonReturn")
        self.buttonGroup_2.addButton(self.toolButtonReturn)
        self.toolButtonErase = QToolButton(self.centralwidget)
        self.toolButtonErase.setGeometry(QRect(250, 31, 51, 22))
        self.toolButtonErase.setObjectName("toolButtonErase")
        self.buttonGroup_2.addButton(self.toolButtonErase)
        self.labelSize = QLabel(self.centralwidget)
        self.labelSize.setGeometry(QRect(320, 30, 351, 21))
        self.labelSize.setText("")
        self.labelSize.setObjectName("labelSize")
        self.label3 = QLabel(self.centralwidget)
        self.label3.setGeometry(QRect(310, 80, 371, 22))
        self.label3.setObjectName("label3")
        self.linev3 = QFrame(self.centralwidget)
        self.linev3.setGeometry(QRect(680, 0, 3, 101))
        self.linev3.setFrameShape(QFrame.VLine)
        self.linev3.setFrameShadow(QFrame.Sunken)
        self.linev3.setObjectName("linev3")
        self.linev2 = QFrame(self.centralwidget)
        self.linev2.setGeometry(QRect(310, 0, 3, 101))
        self.linev2.setFrameShape(QFrame.VLine)
        self.linev2.setFrameShadow(QFrame.Sunken)
        self.linev2.setObjectName("linev2")
        self.linev1 = QFrame(self.centralwidget)
        self.linev1.setGeometry(QRect(190, 0, 3, 101))
        self.linev1.setFrameShape(QFrame.VLine)
        self.linev1.setFrameShadow(QFrame.Sunken)
        self.linev1.setObjectName("linev1")
        self.labelSelectSize = QLabel(self.centralwidget)
        self.labelSelectSize.setGeometry(QRect(320, 50, 351, 21))
        self.labelSelectSize.setText("")
        self.labelSelectSize.setObjectName("labelSelectSize")
        self.spinBoxWidth = QSpinBox(self.centralwidget)
        self.spinBoxWidth.setGeometry(QRect(750, 10, 121, 22))
        self.spinBoxWidth.setObjectName("spinBoxWidth")
        self.linev4 = QFrame(self.centralwidget)
        self.linev4.setGeometry(QRect(1250, 0, 3, 101))
        self.linev4.setFrameShape(QFrame.VLine)
        self.linev4.setFrameShadow(QFrame.Sunken)
        self.linev4.setObjectName("linev4")
        self.label1 = QLabel(self.centralwidget)
        self.label1.setGeometry(QRect(0, 80, 191, 22))
        self.label1.setObjectName("label1")
        self.toolButtonColorChoose = QToolButton(self.centralwidget)
        self.toolButtonColorChoose.setGeometry(QRect(750, 40, 121, 21))
        self.toolButtonColorChoose.setObjectName("toolButtonColorChoose")
        self.comboBoxShape = QComboBox(self.centralwidget)
        self.comboBoxShape.setGeometry(QRect(881, 11, 119, 19))
        self.comboBoxShape.setObjectName("comboBoxShape")
        self.comboBoxShape.addItem("")
        self.comboBoxShape.addItem("")
        self.comboBoxShape.addItem("")
        self.label4 = QLabel(self.centralwidget)
        self.label4.setGeometry(QRect(680, 80, 571, 22))
        self.label4.setObjectName("label4")
        self.toolButtonZoom1 = QToolButton(self.centralwidget)
        self.toolButtonZoom1.setGeometry(QRect(200, 10, 51, 22))
        self.toolButtonZoom1.setObjectName("toolButtonZoom1")
        self.buttonGroup_2.addButton(self.toolButtonZoom1)
        self.toolButtonPaint = QToolButton(self.centralwidget)
        self.toolButtonPaint.setGeometry(QRect(690, 10, 51, 51))
        self.toolButtonPaint.setObjectName("toolButtonPaint")
        self.label2 = QLabel(self.centralwidget)
        self.label2.setGeometry(QRect(190, 80, 121, 22))
        self.label2.setObjectName("label2")
        self.toolButtonText = QToolButton(self.centralwidget)
        self.toolButtonText.setGeometry(QRect(880, 40, 121, 21))
        self.toolButtonText.setObjectName("toolButtonText")
        self.buttonGroup_2.addButton(self.toolButtonText)
        self.fontComboBox = QFontComboBox(self.centralwidget)
        self.fontComboBox.setGeometry(QRect(1010, 10, 231, 18))
        self.fontComboBox.setObjectName("fontComboBox")
        self.toolButtonAuth = QToolButton(self.centralwidget)
        self.toolButtonAuth.setGeometry(QRect(1260, 10, 141, 22))
        self.toolButtonAuth.setObjectName("toolButtonAuth")
        self.linev4_2 = QFrame(self.centralwidget)
        self.linev4_2.setGeometry(QRect(1410, 0, 3, 101))
        self.linev4_2.setFrameShape(QFrame.VLine)
        self.linev4_2.setFrameShadow(QFrame.Sunken)
        self.linev4_2.setObjectName("linev4_2")
        self.toolButtonCanvas = QToolButton(self.centralwidget)
        self.toolButtonCanvas.setGeometry(QRect(70, 10, 51, 51))
        self.toolButtonCanvas.setObjectName("toolButtonCanvas")
        self.toolButtonLoad = QToolButton(self.centralwidget)
        self.toolButtonLoad.setGeometry(QRect(130, 10, 51, 51))
        self.toolButtonLoad.setObjectName("toolButtonLoad")
        self.toolButtonSave = QToolButton(self.centralwidget)
        self.toolButtonSave.setGeometry(QRect(10, 10, 51, 51))
        self.toolButtonSave.setObjectName("toolButtonSave")
        self.toolButtonCrop = QToolButton(self.centralwidget)
        self.toolButtonCrop.setGeometry(QRect(200, 52, 101, 22))
        self.toolButtonCrop.setObjectName("toolButtonCrop")
        MemeCreator.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MemeCreator)
        self.menubar.setGeometry(QRect(0, 0, 1925, 26))
        self.menubar.setObjectName("menubar")
        MemeCreator.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MemeCreator)
        self.statusbar.setObjectName("statusbar")
        MemeCreator.setStatusBar(self.statusbar)

        self.retranslateUi(MemeCreator)
        QMetaObject.connectSlotsByName(MemeCreator)

    def retranslateUi(self, MemeCreator):
        _translate = QCoreApplication.translate
        MemeCreator.setWindowTitle(_translate("MemeCreator", "MainWindow"))
        icon = QIcon()
        self.toolButtonZoom2.setIcon(QIcon("files/icons/icons8-zoom-to-extents-24.png"))
        self.toolButtonReturn.setIcon(QIcon("files/icons/icons8-u-turn-to-left-24.png"))
        self.toolButtonErase.setIcon(QIcon("files/icons/icons8-eraser-24.png"))
        self.label3.setText(_translate("MemeCreator", "<html><head/><body><p align=\"center\">Информация</p></body></html>"))
        self.label1.setText(_translate("MemeCreator", "<html><head/><body><p align=\"center\">Изображение</p></body></html>"))
        self.toolButtonColorChoose.setIcon(QIcon("files/icons/icons8-paint-palette-24.png"))
        self.comboBoxShape.setItemText(0, _translate("MemeCreator", "Кисть"))
        self.comboBoxShape.setItemText(1, _translate("MemeCreator", "Линия"))
        self.comboBoxShape.setItemText(2, _translate("MemeCreator", "Текст"))
        self.label4.setText(_translate("MemeCreator", "<html><head/><body><p align=\"center\">Кисть</p></body></html>"))
        self.toolButtonZoom1.setIcon(QIcon("files/icons/icons8-zoom-to-extents-24.png"))
        self.toolButtonPaint.setIcon(QIcon("files/icons/icons8-paint-24.png"))
        self.label2.setText(_translate("MemeCreator", "<html><head/><body><p align=\"center\">Инструменты</p></body></html>"))
        self.toolButtonText.setIcon(QIcon("files/icons/icons8-text-24.png"))
        self.toolButtonAuth.setText(_translate("MemeCreator", "Авторизация"))
        self.toolButtonCanvas.setIcon(QIcon("files/icons/icons8-easel-24.png"))
        self.toolButtonLoad.setIcon(QIcon("files/icons/icons8-file-download-24.png"))
        self.toolButtonSave.setIcon(QIcon("files/icons/icons8-file-explorer-24.png"))
        self.toolButtonCrop.setText(_translate("MemeCreator", "Обрезать"))

# ╔════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
# ║Блок функций                                                                                                        ║
# ╚════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╝

    def openFile(self):
        self.file = QFileDialog.getOpenFileName(
            self, "Выбрать картинку", "",
            "(*.jpg);;(*.png);;Все файлы (*)")[0]
        self.initUI()

    def createCanvas(self):
        self.width = QInputDialog().getText(self, "Создание холста",
                                            "Ширина:", QLineEdit.Normal,
                                            QDir().home().dirName())[0]
        self.width = int(self.width)
        self.height = QInputDialog().getText(self, "Создание холста",
                                             "Высота:", QLineEdit.Normal,
                                             QDir().home().dirName())[0]
        self.height = int(self.height)

        self.pixmap = QPixmap(self.width, self.height)
        self.pixmap.fill(Qt.white)

        self.startWidth = self.pixmap.width()
        self.startHeight = self.pixmap.height()

        self.labelSize.setText(f"{self.width}x{self.height}")
        self.labelImage.resize(self.width, self.height)

    def saveFile(self):
        self.save = Saving(self.pixmap)
        self.save.show()


    def crop(self):
        cropTool = QCrop(self.pixmap)
        status = cropTool.exec()

        if status == Qt.Accepted:
            croppedImage = cropTool.image
        else: croppedImage = self.pixmap
        self.pixmap = croppedImage
        self.initUI()

    def clearMap(self):
        self.pixmap = QPixmap(self.file)
        self.scaleImageReturn()
        self.update()

    def scaleImageBigger(self):
        if self.width < 5001 and self.height < 5001:
            self.scale += 1
            self.width = self.startWidth * self.scale
            self.height = self.startHeight * self.scale

            self.pixmap = self.pixmap.scaledToWidth(self.width)

            self.labelImage.resize(self.width, self.height)
            self.labelImage.move(0, 102)
            print(self.scale, self.width)

    def scaleImageSmaller(self):
        if self.scale > 1:
            self.width -= self.startWidth
            self.height -= self.startHeight
            self.scale -= 1
            self.pixmap = self.pixmap.scaledToWidth(self.width)

            self.labelImage.resize(self.width, self.height)
            self.labelImage.move(0, 102)
            print(self.scale, self.width)

    def scaleImageReturn(self):
        self.width = self.startWidth
        self.height = self.startHeight
        self.scale = 1
        self.pixmap = self.pixmap.scaledToWidth(self.width)

        self.labelImage.resize(self.width, self.height)
        self.labelImage.move(0, 102)

    def changeDrawingFlag(self):
        self.drawingFlag = not self.drawingFlag

    def editPenWidth(self):
        self.brushWidth = self.spinBoxWidth.value()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(QRect(0, 102, self.width, self.height), self.pixmap)
        self.update()

    def chooseColor(self):
        self.color = QColorDialog.getColor()

    def changeCursorFlag(self):
        self.grabFlag = not self.grabFlag

    def choseShape(self):
        self.shape = self.comboBoxShape.currentText()

    def setText(self):
        self.text, flag = QInputDialog().getText(self, "Рисование текста",
                                                 "Текст:", QLineEdit.Normal,
                                                  QDir().home().dirName())

    def auth(self):
        self.auth = Authorization()
        self.auth.show()

# ╔════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
# ║Блок управления                                                                                                     ║
# ╚════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╝

    def mousePressEvent(self, event):
        self.coordX = event.x()
        self.coordY = event.y() - 102
        if self.coordY < 0:
            self.coordY = 0

        if (event.button() == Qt.LeftButton) and self.drawingFlag:
            self.lastPoint = QPoint(self.coordX, self.coordY)
            self.startPoint = QPoint(self.coordX, self.coordY)
            self.endPoint = QPoint(self.coordX, self.coordY)
            self.pixmapCopy = self.pixmap
            self.update()

    def mouseMoveEvent(self, event):
        self.coordX = event.x()
        self.coordY = event.y() - 102
        if self.coordY < 0:
            self.coordY = 0
        if self.coordY > self.height:
            self.coordY = self.height
        if self.coordX > self.width:
            self.coordX = self.width
        self.labelCoords.setText(f"{self.coordX // self.scale}, {self.coordY // self.scale}")

        if (event.buttons() and Qt.LeftButton) and self.drawingFlag:
            painter = QPainter(self.pixmap)
            painter.setPen(QPen(self.color, self.brushWidth * self.scale,
                                Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            if self.shape == "Кисть":
                painter.drawLine(self.lastPoint, QPoint(self.coordX, self.coordY))
                self.lastPoint = self.endPoint
                print("draw point connect")

            if self.shape == "Линия":
                painter = QPainter(self.pixmapCopy)
                painter.setPen(QPen(self.color, self.brushWidth * self.scale,
                                    Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
                painter.drawLine(self.startPoint, QPoint(self.coordX, self.coordY))
                print(self.startPoint, QPoint(self.coordX, self.coordY))

            if self.shape == "Текст":
                painter = QPainter(self.pixmapCopy)
                painter.setPen(QPen(self.color, self.brushWidth * self.scale,
                                    Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
                font = QFont(self.fontComboBox.currentFont())
                font.setPointSize(self.brushWidth * self.scale)
                self.rect = QRect(self.startPoint, QPoint(self.coordX, self.coordY))
                painter.drawText(self.rect, Qt.AlignCenter, self.text)
                print(self.startPoint, QPoint(self.coordX, self.coordY))

        self.lastPoint = QPoint(self.coordX, self.coordY)
        self.update()

    def mouseReleaseEvent(self, event):
        self.endPoint = QPoint(event.x(), event.y() - 102)
        painter = QPainter(self.pixmap)
        painter.setPen(QPen(self.color, self.brushWidth * self.scale,
                            Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        if self.shape == "Линия":
            painter.drawLine(self.startPoint, self.endPoint)
            print("draw line connect")
        if self.shape == "Текст":
            font = QFont(self.fontComboBox.currentFont())
            font.setPointSize(self.brushWidth * self.scale)
            painter.setFont(font)
            self.rect = QRect(self.startPoint, self.endPoint)
            painter.drawText(self.rect, Qt.AlignCenter, self.text)
            print("draw text connect")


    def wheelEvent(self, event):
        numDegrees = event.angleDelta().y() / 8
        numSteps = numDegrees // 15
        if numSteps > 0:
            self.scaleImageBigger()
        elif numSteps < 0:
            self.scaleImageSmaller()

# ╔════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
# ║Блок запуска                                                                                                        ║
# ╚════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╝

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())
