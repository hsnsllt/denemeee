# الاشتراكات
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QComboBox, QPushButton,
    QTableWidget, QTableWidgetItem
)
from database import db
from datetime import datetime, timedelta

class SubscriptionsPage(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        form = QHBoxLayout()

        self.member_box = QComboBox()
        self.load_members()

        self.duration_box = QComboBox()
        self.duration_box.addItems(["1 AY", "3 AY", "6 AY"])

        add_btn = QPushButton("Abone Ekle")
        add_btn.clicked.connect(self.add_subscription)

        form.addWidget(QLabel("Abone"))
        form.addWidget(self.member_box)
        form.addWidget(self.duration_box)
        form.addWidget(add_btn)

        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(
            ["Adı Soyadı", "Başlangıç", "Bitiş", "Durum"]
        )

        layout.addLayout(form)
        layout.addWidget(self.table)

        self.load_subscriptions()

    def load_members(self):
        self.member_box.clear()
        for m in db.members.find():
            self.member_box.addItem(m["name"], m["_id"])

    def add_subscription(self):
        member_name = self.member_box.currentText()
        start = datetime.now()

        months = {"1 AY": 30, "3 AY": 90, "6 AY": 180}
        days = months[self.duration_box.currentText()]
        end = start + timedelta(days=days)

        db.subscriptions.insert_one({
            "member": member_name,
            "start_date": start,
            "end_date": end
        })

        self.load_subscriptions()

    def load_subscriptions(self):
        self.table.setRowCount(0)
        now = datetime.now()

        for s in db.subscriptions.find():
            status = "Aktif" if s["end_date"] >= now else "Aktif Değil"

            row = self.table.rowCount()
            self.table.insertRow(row)

            self.table.setItem(row, 0, QTableWidgetItem(s["member"]))
            self.table.setItem(row, 1, QTableWidgetItem(str(s["start_date"].date())))
            self.table.setItem(row, 2, QTableWidgetItem(str(s["end_date"].date())))
            self.table.setItem(row, 3, QTableWidgetItem(status))

    def showEvent(self, event):
        self.load_members()
        super().showEvent(event)