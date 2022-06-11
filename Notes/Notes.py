from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QListWidget, QLineEdit, QTextEdit, \
    QInputDialog, QHBoxLayout, QVBoxLayout
import json
import os

app = QApplication([])
w = QWidget()
w.setWindowTitle('Розумні замітки')
w.setWindowIcon(QIcon('icon.png'))
w.resize(900, 600)

note_field = QTextEdit()
notes_ll = QLabel('Список заміток')
notes_l = QListWidget()
note_create = QPushButton('Створити замітку')
note_del = QPushButton('Видалити замітку')
note_save = QPushButton('Зберегти замітку')
tags_ll = QLabel('Список тегів')
tags_l = QListWidget()
tag_field = QLineEdit('')
tag_field.setPlaceholderText('Введіть тег')
tag_add = QPushButton('Додати до замітки')
tag_del = QPushButton('Відкріпити від замітки')
tag_search = QPushButton('Шукати замітки по тегу')

notes_layout = QHBoxLayout()
col1 = QVBoxLayout()
col1.addWidget(note_field)
col2 = QVBoxLayout()
col2.addWidget(notes_ll)
col2.addWidget(notes_l)
row1 = QHBoxLayout()
row1.addWidget(note_create)
row1.addWidget(note_del)
row2 = QHBoxLayout()
row2.addWidget(note_save)
col2.addLayout(row1)
col2.addLayout(row2)
col2.addWidget(tags_ll)
col2.addWidget(tags_l)
col2.addWidget(tag_field)
row3 = QHBoxLayout()
row3.addWidget(tag_add)
row3.addWidget(tag_del)
row4 = QHBoxLayout()
row4.addWidget(tag_search)
col2.addLayout(row3)
col2.addLayout(row4)
notes_layout.addLayout(col1, stretch=2)
notes_layout.addLayout(col2, stretch=1)
w.setLayout(notes_layout)


def add_note():
    note_name, ok = QInputDialog.getText(w, "Додати замітку", "Назва замітки: ")
    if ok and note_name != "":
        notes[note_name] = {"текст": "", "теги": []}
        notes_l.addItem(note_name)
        tags_l.addItems(notes[note_name]["теги"])


def show_note():
    key = notes_l.selectedItems()[0].text()
    note_field.setText(notes[key]["текст"])
    tags_l.clear()
    tags_l.addItems(notes[key]["теги"])


def save_note():
    if notes_l.selectedItems():
        key = notes_l.selectedItems()[0].text()
        notes[key]["текст"] = note_field.toPlainText()
        with open("notes.json", "w") as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=True)


def del_note():
    if notes_l.selectedItems():
        key = notes_l.selectedItems()[0].text()
        del notes[key]
        notes_l.clear()
        tags_l.clear()
        note_field.clear()
        notes_l.addItems(notes)
        with open("notes.json", "w") as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=True)


def add_tag():
    if notes_l.selectedItems():
        key = notes_l.selectedItems()[0].text()
        tag = tag_field.text()
        if not tag in notes[key]["теги"] and tag != '':
            notes[key]["теги"].append(tag)
            tags_l.addItem(tag)
            tag_field.clear()
        with open("notes.json", "w") as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)


def del_tag():
    if tags_l.selectedItems():
        key = notes_l.selectedItems()[0].text()
        tag = tags_l.selectedItems()[0].text()
        notes[key]["теги"].remove(tag)
        tags_l.clear()
        tags_l.addItems(notes[key]["теги"])
        with open("notes.json", "w") as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)


def search_tag():
    tag = tag_field.text()
    if tag_search.text() == "Шукати замітки по тегу" and tag:
        notes_filtered = {}
        for note in notes:
            if tag in notes[note]["теги"]:
                notes_filtered[note] = notes[note]
        tag_search.setText("Скинути пошук")
        notes_l.clear()
        tags_l.clear()
        notes_l.addItems(notes_filtered)
    elif tag_search.text() == "Скинути пошук":
        tag_field.clear()
        notes_l.clear()
        tags_l.clear()
        notes_l.addItems(notes)
        tag_search.setText("Шукати замітки по тегу")


note_create.clicked.connect(add_note)
notes_l.itemClicked.connect(show_note)
note_save.clicked.connect(save_note)
note_del.clicked.connect(del_note)
tag_add.clicked.connect(add_tag)
tag_del.clicked.connect(del_tag)
tag_search.clicked.connect(search_tag)
w.show()

global notes
if not os.path.exists("notes.json"):
    with open("notes.json", "w") as file:
        notes = {'1': {"текст": "...", "теги": []}}
        json.dump(notes, file, sort_keys=True, ensure_ascii=False)
elif os.path.exists("notes.json"):
    with open("notes.json", "r") as file:
        notes = json.load(file)
    notes_l.addItems(notes)
app.setStyle('Fusion')
app.exec_()
