# المشتركين
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton,
    QComboBox, QTableWidget, QTableWidgetItem
)
from database import db

class MembersPage(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        # ===== نموذج الإدخال =====
        form = QHBoxLayout()

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Abone Adı Soyadı")

        self.id_input = QLineEdit()
        self.id_input.setPlaceholderText("T.C. Kimlik No")

        self.gender_box = QComboBox()
        self.gender_box.addItems(["Erkek", "Kadın"])

        add_btn = QPushButton("Abone Ekle")
        add_btn.clicked.connect(self.add_member)

        form.addWidget(self.name_input)
        form.addWidget(self.id_input)
        form.addWidget(self.gender_box)
        form.addWidget(add_btn)

        # ===== جدول المشتركين =====
        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(
            ["Adı Soyadı", "T.C. Kimlik", "Cinsiyet"]
        )

        layout.addLayout(form) # النموذج 
        layout.addWidget(self.table) #الجدوال 

        self.load_members() #تحمييل جدول المشتركين وعرضهم فور فتح الصفحة

    def load_members(self):
        self.table.setRowCount(0) # مسح الجدول قبل قبل اعادة تحميل البيانات
        for member in db.members.find(): # جلب كل المشتركين من collection اسمها members
            row = self.table.rowCount() # معرفة رقم الصف الحالي
            self.table.insertRow(row) # اضافة صف جديد
            self.table.setItem(row, 0, QTableWidgetItem(member["name"]))
            self.table.setItem(row, 1, QTableWidgetItem(member["kimlik"]))
            self.table.setItem(row, 2, QTableWidgetItem(member["gender"]))

    def add_member(self):
        name = self.name_input.text()
        kimlik = self.id_input.text()
        gender = self.gender_box.currentText()

        if not name or not kimlik:
            return

        db.members.insert_one({
            "name": name,
            "kimlik": kimlik,
            "gender": gender
        })

            # تفريغ الحقول بعد الاضافة
        self.name_input.clear()
        self.id_input.clear()
            # تحديث الجدول فورا بدون اعادة تشغيل البرنامج
        self.load_members()
