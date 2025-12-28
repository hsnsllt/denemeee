# لوحة التحكم
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame
from database import db
from datetime import datetime

class Dashboard(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setSpacing(20)

        members_count = db.members.count_documents({})
        active_subs = db.subscriptions.count_documents(
            {"end_date": {"$gte": datetime.now()}}
        )
        income = sum(p["amount"] for p in db.payments.find({}))

        layout.addWidget(self.card("Abone Sayısı", members_count))
        layout.addWidget(self.card("Aktif Abonelikler", active_subs))
        layout.addWidget(self.card("Toplam Gelir", f"{income} ₺"))

    def card(self, title, value):
        frame = QFrame()
        frame.setStyleSheet("""
        QFrame {
            background-color: #1e293b;
            border-radius: 15px;
            padding: 25px;
        }""")
        v = QVBoxLayout(frame)
        v.addWidget(QLabel(title))
        v.addWidget(QLabel(str(value)))
        return frame
