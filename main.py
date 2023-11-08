import shutil
import sys
import io
import os
import fitz
import csv
from datetime import datetime
from kashimo import Wplace
from PIL import Image

from PyQt5 import uic  # Импортируем uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QFileDialog, QMessageBox, QPushButton, QWidget
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

        self.folder_path = 'D:\project\empt'
        self.i = 1

        self.corner = ''
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

        self.completeButton.clicked.connect(self.set_watermark)

        self.fname = None
        self.iname = None
        self.wname = None

        # установил картинку
        self.completeButton.clicked.connect(self.menu_calculation)

        self.filebox.stateChanged.connect(self.file)
        self.img_box.stateChanged.connect(self.image)

        self.filebox.clicked.connect(self.check)
        self.img_box.clicked.connect(self.check)
        self.waterButton.clicked.connect(self.watermarkb)
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
        if not (any([self.filebox.isChecked(), self.img_box.isChecked()])):
            self.completeButton.setDisabled(True)

        if self.img_box.isChecked():
            self.waterButton.setDisabled(False)
        else:
            self.waterButton.setDisabled(True)

        if self.img_box.isChecked() and (self.wname != None) and (self.iname != None):
            self.completeButton.setDisabled(False)

        if self.filebox.isChecked() and self.fname:
            self.completeButton.setDisabled(False)

        elif not (self.fname) and self.filebox.isChecked():
            self.completeButton.setDisabled(True)

    def choose_object(self):

        if not self.img_box.isEnabled():
            self.fname = QFileDialog.getOpenFileName(self, 'Выбрать файл', '', filter='csv (*.csv)')[0]
            try:
                destination_path = os.path.join('D:\project', os.path.basename(self.fname))
                shutil.copy(self.iname, destination_path)
                self.fname = self.fname.split('/')[-1]
                self.iname = None
                if not self.fname.endswith('.csv'):
                    self.show_error_message("Ошибка формата файла", "Выбранный файл должен быть формата CSV.")
                    return
            except Exception as e:
                print(e)
            self.check()
        if not self.filebox.isEnabled():
            self.iname = QFileDialog.getOpenFileName(self, 'Выбрать картинку', '')[0]
            try:
                destination_path = os.path.join(self.folder_path, os.path.basename(self.iname))
                shutil.copy(self.iname, destination_path)

                # self.iname = self.iname.split('/')[-1]
                self.fname = None
                if not (self.iname.endswith('.jpg') or self.iname.endswith('.png')):
                    self.show_error_message("Ошибка формата файла", "Выбранный файл должен быть формата jpg либо png.")
                    return
            except Exception as e:
                print(e)
            self.check()

        # возможность выбирать файл/изображение

    def watermarkb(self):
        self.wname = QFileDialog.getOpenFileName(self, 'Выбрать водяной знак', '')[0]
        try:
            destination_path = os.path.join(self.folder_path, os.path.basename(self.wname))
            shutil.copy(self.wname, destination_path)
            # self.wname = self.wname.split('/')[-1]

            if not (self.wname.endswith('.jpg') or self.wname.endswith('.png')):
                self.show_error_message("Ошибка формата файла", "Выбранный файл должен быть формата jpg либо png.")
                return
            self.check()
            self.water_mark_place()
        except Exception as e:
            print(e)

    def wrong_size(self, title, message):
        size_error = QMessageBox(self)
        size_error.setIcon(QMessageBox.Critical)
        size_error.setWindowTitle(title)
        size_error.setText(message)
        size_error.exec_()

    def set_watermark(self):

        if self.wname and self.iname:
            os.chmod(self.wname, 0o644)
            os.chmod(self.iname, 0o644)

            if os.access(self.wname, os.R_OK):
                print("У вас есть права на чтение файла.")
            else:
                print("У вас нет прав на чтение файла.")

            main_image = Image.open(self.iname)
            insert_image = Image.open(self.wname)
            width, height = main_image.size
            width_i, height_i = insert_image.size

            if ((width_i >= width) or (height_i >= height)):
                self.wrong_size("Ошибка", 'Размер водяного знака должен быть меньше изображения.')
            else:

                result_path = 'D:\project\imagefolder\output_image.jpg'
                if self.corner == 'lt':

                    main_image.paste(insert_image, (0, 0))

                    if os.path.exists(result_path):

                        # Генерируйте уникальное имя для нового файла
                        base_name, ext = os.path.splitext(result_path)

                        self.i += 1
                        result_path = f"{base_name}_{self.i}{ext}"
                        main_image.save(result_path)
                        self.pix = QPixmap(result_path)
                        self.itog_label.setPixmap(self.pix)
                    else:
                        main_image.save(result_path)
                        self.pix = QPixmap(result_path)
                        self.itog_label.setPixmap(self.pix)


                elif self.corner == 'mt':
                    main_image.paste(insert_image, ((width // 2) - width_i, 0))

                    if os.path.exists(result_path):

                        # Генерируйте уникальное имя для нового файла
                        base_name, ext = os.path.splitext(result_path)
                        self.i += 1
                        result_path = f"{base_name}_{self.i}{ext}"
                        main_image.save(result_path)
                        self.pix = QPixmap(result_path)
                        self.itog_label.setPixmap(self.pix)
                    else:
                        main_image.save(result_path)
                        self.pix = QPixmap(result_path)
                        self.itog_label.setPixmap(self.pix)
                elif self.corner == 'rt':
                    main_image.paste(insert_image, (width - width_i, 0))
                    if os.path.exists(result_path):

                        # Генерируйте уникальное имя для нового файла
                        base_name, ext = os.path.splitext(result_path)
                        self.i += 1
                        result_path = f"{base_name}_{self.i}{ext}"
                        main_image.save(result_path)
                        self.pix = QPixmap(result_path)
                        self.itog_label.setPixmap(self.pix)
                    else:
                        main_image.save(result_path)
                        self.pix = QPixmap(result_path)
                        self.itog_label.setPixmap(self.pix)

                elif self.corner == 'lm':
                    main_image.paste(insert_image, (0, (height // 2)))

                    if os.path.exists(result_path):

                        # Генерируйте уникальное имя для нового файла
                        base_name, ext = os.path.splitext(result_path)
                        self.i += 1
                        result_path = f"{base_name}_{self.i}{ext}"
                        main_image.save(result_path)
                        self.pix = QPixmap(result_path)
                        self.itog_label.setPixmap(self.pix)
                    else:
                        main_image.save(result_path)
                        self.pix = QPixmap(result_path)
                        self.itog_label.setPixmap(self.pix)
                elif self.corner == 'mm':
                    main_image.paste(insert_image, ((width // 2) - width_i, (height // 2)))

                    if os.path.exists(result_path):

                        # Генерируйте уникальное имя для нового файла
                        base_name, ext = os.path.splitext(result_path)
                        self.i += 1
                        result_path = f"{base_name}_{self.i}{ext}"
                        main_image.save(result_path)
                        self.pix = QPixmap(result_path)
                        self.itog_label.setPixmap(self.pix)
                    else:
                        main_image.save(result_path)
                        self.pix = QPixmap(result_path)
                        self.itog_label.setPixmap(self.pix)
                elif self.corner == 'rm':
                    main_image.paste(insert_image, (width - width_i, (height // 2)))

                    if os.path.exists(result_path):

                        # Генерируйте уникальное имя для нового файла
                        base_name, ext = os.path.splitext(result_path)
                        self.i += 1
                        result_path = f"{base_name}_{self.i}{ext}"
                        main_image.save(result_path)
                        self.pix = QPixmap(result_path)
                        self.itog_label.setPixmap(self.pix)
                    else:
                        main_image.save(result_path)
                        self.pix = QPixmap(result_path)
                        self.itog_label.setPixmap(self.pix)
                elif self.corner == 'ld':
                    main_image.paste(insert_image, (0, height - height_i))

                    if os.path.exists(result_path):

                        # Генерируйте уникальное имя для нового файла
                        base_name, ext = os.path.splitext(result_path)
                        self.i += 1
                        result_path = f"{base_name}_{self.i}{ext}"
                        main_image.save(result_path)
                        self.pix = QPixmap(result_path)
                        self.itog_label.setPixmap(self.pix)
                    else:
                        main_image.save(result_path)
                        self.pix = QPixmap(result_path)
                        self.itog_label.setPixmap(self.pix)
                elif self.corner == 'ld':
                    main_image.paste(insert_image, (0, height - height_i))

                    if os.path.exists(result_path):

                        # Генерируйте уникальное имя для нового файла
                        base_name, ext = os.path.splitext(result_path)
                        self.i += 1
                        result_path = f"{base_name}_{self.i}{ext}"
                        main_image.save(result_path)
                        self.pix = QPixmap(result_path)
                        self.itog_label.setPixmap(self.pix)
                    else:
                        main_image.save(result_path)
                        self.pix = QPixmap(result_path)
                        self.itog_label.setPixmap(self.pix)
                elif self.corner == 'md':
                    main_image.paste(insert_image, ((width // 2) - width_i, height - height_i))

                    if os.path.exists(result_path):

                        # Генерируйте уникальное имя для нового файла
                        base_name, ext = os.path.splitext(result_path)
                        self.i += 1
                        result_path = f"{base_name}_{self.i}{ext}"
                        main_image.save(result_path)
                        self.pix = QPixmap(result_path)
                        self.itog_label.setPixmap(self.pix)
                    else:
                        main_image.save(result_path)
                        self.pix = QPixmap(result_path)
                        self.itog_label.setPixmap(self.pix)
                elif self.corner == 'rd':
                    main_image.paste(insert_image, (width - width_i, height - height_i))

                    if os.path.exists(result_path):

                        # Генерируйте уникальное имя для нового файла
                        base_name, ext = os.path.splitext(result_path)
                        self.i += 1
                        result_path = f"{base_name}_{self.i}{ext}"
                        main_image.save(result_path)
                        self.pix = QPixmap(result_path)
                        self.itog_label.setPixmap(self.pix)
                    else:
                        main_image.save(result_path)
                        self.pix = QPixmap(result_path)
                        self.itog_label.setPixmap(self.pix)

    def water_mark_place(self):
        if self.wname:
            self.app1 = Wplace(self)
            self.app1.show()

    def menu_calculation(self):
        if self.fname:

            with open(self.fname, 'r') as menu:
                data = list(csv.reader(menu, delimiter=';', quotechar='"'))
                self.date = data[0][-1]

                data = list(filter(lambda x: len(set(x)) > 6, data))

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

                doc = DocxTemplate("wordprime1.docx")
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
                    'total_u': total[4],
                    'school_n': "Иванов Иван николаевич",
                    'direct_n': 'Петров Александр Юрьевич',
                    'cook_n': 'Васильева Анна Григорьевна'
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
