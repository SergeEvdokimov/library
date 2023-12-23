import sys
import sqlite3
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtWidgets import QApplication, QPushButton, QMainWindow, QComboBox, QTextEdit, QListWidget, QListWidgetItem,\
    QLabel

con = sqlite3.connect("films.db")
cur = con.cursor()


class ShowWidget(QMainWindow):
    def __init__(self, book, image='images/0.jpg'):
        super().__init__()
        self.setGeometry(300, 300, 800, 600)
        if len(book) == 5:
            unic, name, author, year, genre = book
        else:
            unic, name, author, year, genre, image = book
        self.unic = unic
        self.name = name
        self.author = author
        self.year = str(year)
        self.genre = genre
        self.image = image

        self.photo = QLabel(self)
        self.pix = QPixmap(image)
        self.pix = self.pix.scaled(450, 300)
        self.photo.setPixmap(self.pix)
        self.photo.move(200, 30)
        self.photo.resize(450, 300)

        font = QFont()
        font.setBold(True)
        font.setPixelSize(20)

        self.lbl1 = QLabel('Название', self)
        self.lbl1.move(350, 350)
        self.lbl1.resize(250, 50)
        self.lbl1.setFont(font)

        self.lbl2 = QLabel(self.name, self)
        self.lbl2.move(325, 380)
        self.lbl2.resize(250, 50)

        self.lbl3 = QLabel('Автор', self)
        self.lbl3.move(350, 400)
        self.lbl3.resize(250, 50)
        self.lbl3.setFont(font)

        self.lbl4 = QLabel(self.author, self)
        self.lbl4.move(325, 430)
        self.lbl4.resize(250, 50)

        self.lbl5 = QLabel('Год выпуска', self)
        self.lbl5.move(350, 450)
        self.lbl5.resize(250, 50)
        self.lbl5.setFont(font)

        self.lbl6 = QLabel(self.year, self)
        self.lbl6.move(325, 470)
        self.lbl6.resize(250, 50)

        self.lbl7 = QLabel('Жанр', self)
        self.lbl7.move(350, 490)
        self.lbl7.resize(250, 50)
        self.lbl7.setFont(font)

        self.lbl8 = QLabel(self.genre, self)
        self.lbl8.move(325, 520)
        self.lbl8.resize(250, 50)


class Library(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(300, 300, 500, 500)
        self.setWindowTitle('Каталог библиотеки')

        self.search_by = QComboBox(self)
        self.search_by.move(30, 30)
        self.search_by.resize(100, 30)
        self.search_by.addItems(['Автор', 'Название'])

        self.line = QTextEdit(self)
        self.line.move(30, 80)
        self.line.resize(150, 25)
        
        self.button = QPushButton('Искать', self)
        self.button.move(300, 20)
        self.button.resize(100, 50)
        self.button.clicked.connect(self.show_books)

        self.films = QListWidget(self)
        self.films.resize(480, 290)
        self.films.move(10, 200)
        self.films.itemClicked.connect(self.show_form)

        self.show_list = []

    def show_form(self, item):
        row = self.films.indexFromItem(item).row()
        book = cur.execute(f'select * from films where id == {self.show_list[row][0]}').fetchall()[0]
        if book[-1] == '':
            book = book[:-1]
        self.show_widget = ShowWidget(book)
        self.show_widget.show()

    def show_books(self):
        books = cur.execute('select * from films').fetchall()
        self.show_list.clear()
        if self.search_by.currentText() == 'Автор':
            for i in books:
                if self.line.toPlainText() in i[2]:
                    self.show_list.append([i[0], i[1]])
        else:
            for i in books:
                if self.line.toPlainText() in i[1]:
                    self.show_list.append([i[0], i[1]])
        self.films.clear()
        for item_text in self.show_list:
            item = QListWidgetItem(item_text[1])
            item.setTextAlignment(Qt.AlignHCenter)
            self.films.addItem(item)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Library()
    window.show()
    sys.exit(app.exec())