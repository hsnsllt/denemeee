import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QPushButton, QHBoxLayout, QStackedWidget
)
from utils.styles import APP_STYLE
from views.dashboard import Dashboard
from views.members import MembersPage
from views.subscriptions import SubscriptionsPage
from views.payments import PaymentsPage

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gym Management ")
        self.resize(1200, 700)

        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QHBoxLayout(central)

        # القائمة الجانبية
        menu = QVBoxLayout()
        btn_dashboard = QPushButton("DASHBOARD") # لوحة التحكم Kontrol Paneli
        btn_members = QPushButton("MEMBERS") # المشتركين Aboneler
        btn_subs = QPushButton("SUBSCRIPTIONS") # الاشتراكات Abonelikler
        btn_pay = QPushButton("PAYMENTS") # المدفوعات Ödemeler

        menu.addWidget(btn_dashboard)
        menu.addWidget(btn_members)
        menu.addWidget(btn_subs)
        menu.addWidget(btn_pay)
        menu.addStretch()

        # الصفحات
        self.pages = QStackedWidget()
        self.pages.addWidget(Dashboard())
        self.pages.addWidget(MembersPage())
        self.pages.addWidget(SubscriptionsPage())
        self.pages.addWidget(PaymentsPage())

        btn_dashboard.clicked.connect(lambda: self.pages.setCurrentIndex(0))
        btn_members.clicked.connect(lambda: self.pages.setCurrentIndex(1))
        btn_subs.clicked.connect(lambda: self.pages.setCurrentIndex(2))
        btn_pay.clicked.connect(lambda: self.pages.setCurrentIndex(3))

        main_layout.addLayout(menu, 1)
        main_layout.addWidget(self.pages, 4)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(APP_STYLE)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())