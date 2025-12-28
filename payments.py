# المدفوعات
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QComboBox, QLineEdit,
    QPushButton, QTableWidget, QTableWidgetItem, QMessageBox
)
from database import db
from datetime import datetime


class PaymentsPage(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        form = QHBoxLayout()

        self.member_box = QComboBox()
        self.load_members()

        self.method_box = QComboBox()
        self.method_box.addItems(["Nakit", "Kredi Kart"])

        self.card_input = QLineEdit()
        self.card_input.setPlaceholderText("Abone Kart No ( İsteğe Bağlı )")

        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("Abonelik Harcı")

        pay_btn = QPushButton("KAYDET")
        pay_btn.clicked.connect(self.add_payment)

        form.addWidget(QLabel("Abone"))
        form.addWidget(self.member_box)
        form.addWidget(self.method_box)
        form.addWidget(self.card_input)
        form.addWidget(self.amount_input)
        form.addWidget(pay_btn)

        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(
            ["Adı soyadı", "Miktar", "Ödeme Yöntemi", "Tarih"]
        )

        layout.addLayout(form)
        layout.addWidget(self.table)

        self.load_payments()

    def load_members(self):
        self.member_box.clear()
        for m in db.members.find():
            self.member_box.addItem(m["name"])

    def add_payment(self):
        member = self.member_box.currentText()
        method = self.method_box.currentText()
        card = self.card_input.text()
        amount_text = self.amount_input.text()

        if not amount_text:
            QMessageBox.warning(self, "HATA", "Abone Harc Miktari Giriniz")
            return

        amount = float(amount_text)
        now = datetime.now()  

        #  منع تكرار الدفع في نفس اليوم
        existing = db.payments.find_one({
            "member": member,
            "date": {
                "$gte": datetime(now.year, now.month, now.day, 0, 0, 0),
                "$lt": datetime(now.year, now.month, now.day, 23, 59, 59)
            }
        })

        if existing:
            QMessageBox.warning(self, "Uyarı", "Bu Abone İçin Ödeme Bugün Kaydedildi.")
            return

        db.payments.insert_one({
            "member": member,
            "amount": amount,
            "method": method,
            "card": card if method == "Kart" else "",
            "date": now
        })

        self.amount_input.clear()
        self.card_input.clear()
        self.load_payments()

    def load_payments(self):
        self.table.setRowCount(0)
        for p in db.payments.find():
            row = self.table.rowCount()
            self.table.insertRow(row)

            self.table.setItem(row, 0, QTableWidgetItem(p["member"]))
            self.table.setItem(row, 1, QTableWidgetItem(str(p["amount"])))
            self.table.setItem(row, 2, QTableWidgetItem(p["method"]))
            self.table.setItem(row, 3, QTableWidgetItem(p["date"].strftime("%Y-%m-%d %H:%M")))
    # تعديلات من حسن : كود مهم لاعادة تحميل الصفحة
    def showEvent(self, event):
        self.load_members()
        super().showEvent(event)