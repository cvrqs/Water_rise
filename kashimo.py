import sys
import io
import fitz
import csv
from datetime import datetime

from PyQt5 import uic  # Импортируем uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QFileDialog, QMessageBox
from PyQt5.QtGui import QPixmap
from docxtpl import DocxTemplate
from docx2pdf import convert

template = """<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>Form</class>
 <widget class="QWidget" name="Form">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>770</width>
    <height>500</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>Form</string>
  </property>
  <widget class="QWidget" name="verticalLayoutWidget">
   <property name="geometry">
    <rect>
     <x>60</x>
     <y>20</y>
     <width>661</width>
     <height>411</height>
    </rect>
   </property>
   <layout class="QVBoxLayout" name="verticalLayout">
    <item>
     <widget class="QTabWidget" name="tabWidget">
      <property name="enabled">
       <bool>true</bool>
      </property>
      <property name="currentIndex">
       <number>0</number>
      </property>
      <widget class="QWidget" name="tab_7">
       <attribute name="title">
        <string>Tab 1</string>
       </attribute>
       <widget class="QCheckBox" name="filebox">
        <property name="geometry">
         <rect>
          <x>30</x>
          <y>40</y>
          <width>70</width>
          <height>17</height>
         </rect>
        </property>
        <property name="text">
         <string>Файл</string>
        </property>
       </widget>
       <widget class="QCheckBox" name="img_box">
        <property name="geometry">
         <rect>
          <x>30</x>
          <y>70</y>
          <width>91</width>
          <height>17</height>
         </rect>
        </property>
        <property name="text">
         <string>Изображение</string>
        </property>
       </widget>
       <widget class="QPushButton" name="filebutton">
        <property name="geometry">
         <rect>
          <x>110</x>
          <y>340</y>
          <width>111</width>
          <height>23</height>
         </rect>
        </property>
        <property name="text">
         <string>Выбрать файл</string>
        </property>
       </widget>
       <widget class="QPushButton" name="waterButton">
        <property name="geometry">
         <rect>
          <x>490</x>
          <y>340</y>
          <width>111</width>
          <height>23</height>
         </rect>
        </property>
        <property name="text">
         <string>Выбрать watermark</string>
        </property>
       </widget>
       <widget class="QPushButton" name="completeButton">
        <property name="geometry">
         <rect>
          <x>290</x>
          <y>340</y>
          <width>111</width>
          <height>23</height>
         </rect>
        </property>
        <property name="text">
         <string>Выполнить</string>
        </property>
       </widget>
       <widget class="QLabel" name="name_label">
        <property name="geometry">
         <rect>
          <x>520</x>
          <y>0</y>
          <width>211</width>
          <height>16</height>
         </rect>
        </property>
        <property name="text">
         <string>Приложение по установке вотермарок.</string>
        </property>
       </widget>
       <widget class="QLabel" name="img_label_1">
        <property name="geometry">
         <rect>
          <x>596</x>
          <y>155</y>
          <width>47</width>
          <height>13</height>
         </rect>
        </property>
        <property name="text">
         <string/>
        </property>
       </widget>
      </widget>
      <widget class="QWidget" name="tab_8">
       <attribute name="title">
        <string>Tab 2</string>
       </attribute>
       <widget class="QLabel" name="img_label">
        <property name="geometry">
         <rect>
          <x>370</x>
          <y>220</y>
          <width>47</width>
          <height>16</height>
         </rect>
        </property>
        <property name="text">
         <string/>
        </property>
       </widget>
      </widget>
     </widget>
    </item>
   </layout>
  </widget>
 </widget>
 <resources/>
 <connections/>
</ui>
"""


# qt приложения
class WaterMarker(QMainWindow):
    def __init__(self):
        super().__init__()
        f = io.StringIO(template)
        uic.loadUi(f, self)

        self.waterButton.setDisabled(True)
        self.completeButton.setDisabled(True)
        self.pixmap = QPixmap("menu_img.jpg")
        self.img_label_2 = QLabel(self.tab_7)
        self.img_label_2.move(60, 120)
        self.img_label_2.resize(596, 155)
        self.img_label_2.setPixmap(self.pixmap)

        self.itog_label = QLabel(self.tab_8)
        self.itog_label.move(0, 0)
        self.itog_label.resize(700, 700)

        # установил картинку
        self.completeButton.clicked.connect(self.menu_calculation)

        self.filebox.stateChanged.connect(self.file)
        self.img_box.stateChanged.connect(self.image)

        self.filebox.clicked.connect(self.check)
        self.img_box.clicked.connect(self.check)

        # настроил кнопки выбора файла

        self.filebutton.clicked.connect(self.choose_object)

    def file(self, state):
        if state == 2:
            self.img_box.setDisabled(True)
            self.waterButton.setDisabled(True)

        else:
            self.img_box.setDisabled(False)
            self.waterButton.setDisabled(False)

    # отключил кнопку изображения при выборе кнокпи файла
    def image(self, state):
        if state == 2:
            self.filebox.setDisabled(True)

        else:
            self.filebox.setDisabled(False)

    def check(self):
        if (any([self.filebox.isChecked(), self.img_box.isChecked()])):
            self.completeButton.setDisabled(False)
        else:
            self.completeButton.setDisabled(True)

        if self.img_box.isChecked():
            self.waterButton.setDisabled(False)
        else:
            self.waterButton.setDisabled(True)

    # отключил кнопку файла при выборе кнокпи изображения

    def choose_object(self):

        if not self.img_box.isEnabled():
            self.fname = QFileDialog.getOpenFileName(self, 'Выбрать файл', '')[0]
            self.fname = self.fname.split('/')[-1]
            self.iname = None
            if not self.fname.endswith('.csv'):
                self.show_error_message("Ошибка формата файла", "Выбранный файл должен быть формата CSV.")
                return

        if not self.filebox.isEnabled():
            self.iname = QFileDialog.getOpenFileName(self, 'Выбрать картинку', '')[0]
            self.iname = self.iname.split('/')[-1]
            self.fname = None
            if not (self.iname.endswith('.jpg') or self.iname.endswith('.png')):
                self.show_error_message("Ошибка формата файла", "Выбранный файл должен быть формата jpg либо png.")
                return
        # возможность выбирать файл/изображение

    def menu_calculation(self):
        if self.fname:

            with open(self.fname, 'r') as menu:
                data = list(csv.reader(menu, delimiter=';', quotechar='"'))
                self.date = data[0][-1]

                data = list(filter(lambda x: len(set(x)) > 5, data))

                self.name_dinner = data[1][0]
                self.snack = data[1][1:]
                self.first_pose = data[2][1:]
                self.second_pose = data[3][1:]
                self.third_pose = data[4][1:]
                self.fourth_pose = data[5][1:]
                self.fifth_pose = data[6][1:]

                self.snack = list(map(lambda x: ''.join(x).replace(',', '.'), self.snack))[2:]
                self.first_pose = list(map(lambda x: ''.join(x).replace(',', '.'), self.first_pose))[2:]
                self.second_pose = list(map(lambda x: ''.join(x).replace(',', '.'), self.second_pose))[2:]
                self.third_pose = list(map(lambda x: ''.join(x).replace(',', '.'), self.third_pose))[2:]
                self.fourth_pose = list(map(lambda x: ''.join(x).replace(',', '.'), self.fourth_pose))[2:]
                self.fifth_pose = list(map(lambda x: ''.join(x).replace(',', '.'), self.fifth_pose))[2:]
                total = []

                for i in range(2, 7):
                    total.append(round(
                        float(self.snack[i]) + float(self.first_pose[i]) + float(self.second_pose[i]) + float(
                            self.third_pose[i]) + float(self.fourth_pose[i]) + float(self.fifth_pose[i]), 1))

                total_0 = total[0]
                total_1 = total[1]
                total_2 = total[2]
                total_3 = total[3]
                total_4 = total[4]
                date = datetime.strptime(self.date, "%d.%m.%Y")
                date = date.strftime("%d %B %Y")

                doc = DocxTemplate("wordprime.docx")
                context = {
                    'date': str(date),
                    'snack': self.snack[0],
                    'snackg': self.snack[1],
                    'snacks': self.snack[2],
                    'snackb': self.snack[3],
                    'snacke': self.snack[4],
                    'snackj': self.snack[5],
                    'snacku': self.snack[6],

                    'first_pose': self.first_pose[0],
                    'firstg': self.first_pose[1],
                    'first_s': self.first_pose[2],
                    'first_e': self.first_pose[3],
                    'first_b': self.first_pose[4],
                    'first_j': self.first_pose[5],
                    'first_u': self.first_pose[6],

                    'second_pose': self.second_pose[0],
                    'secg': self.second_pose[1],
                    'sec_s': self.second_pose[2],
                    'sec_e': self.second_pose[3],
                    'sec_b': self.second_pose[4],
                    'sec_j': self.second_pose[5],
                    'sec_u': self.second_pose[6],

                    'third_pose': self.third_pose[0],
                    'thirdg': self.third_pose[1],
                    'third_s': self.third_pose[2],
                    'third_e': self.third_pose[3],
                    'third_b': self.third_pose[4],
                    'third_j': self.third_pose[5],
                    'third_u': self.third_pose[6],

                    'fourth_pose': self.fourth_pose[0],
                    'fourthg': self.fourth_pose[1],
                    'four_s': self.fourth_pose[2],
                    'four_e': self.fourth_pose[3],
                    'four_b': self.fourth_pose[4],
                    'four_j': self.fourth_pose[5],
                    'four_u': self.fourth_pose[6],

                    'fifth_pose': self.fifth_pose[0],
                    'fifthg': self.fifth_pose[1],
                    'fifth_s': self.fifth_pose[2],
                    'fifth_e': self.fifth_pose[3],
                    'fifth_b': self.fifth_pose[4],
                    'fifthg_j': self.fifth_pose[5],
                    'fifth_u': self.fifth_pose[6],

                    'total_s': total[0],
                    'total_en': total[1],
                    'total_b': total[2],
                    'total_j': total[3],
                    'total_u': total[4]
                }

                doc.render(context)
                doc.save("final.docx")
            # записал данные

            self.img_f = 'final.docx'
            convert(self.img_f)
            # перевел получившийся файл в формат pdf
            self.pdf_to_image('final.pdf')

            self.pix = QPixmap("itog.png")
            self.itog_label.setPixmap(self.pix)
            # с помощью созданной функции перевел pdf файл в изображение

    def pdf_to_image(self, pdf_name):
        pdf_document = fitz.open(pdf_name)
        page = pdf_document.load_page(0)
        image = page.get_pixmap()
        image.save("itog.png")
        pdf_document.close()

    # функция по конвертированию pdf файлов в изображения

    def show_error_message(self, title, message):
        error_dialog = QMessageBox(self)
        error_dialog.setIcon(QMessageBox.Critical)
        error_dialog.setWindowTitle(title)
        error_dialog.setText(message)
        error_dialog.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = WaterMarker()
    ex.show()
    sys.exit(app.exec_())
