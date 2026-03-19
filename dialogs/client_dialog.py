from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from datetime import datetime

class ClientDialog(QDialog):
    def __init__(self, db, client_id=None):
        super().__init__()
        self.db = db
        self.client_id = client_id
        self.setWindowTitle("Клиент" if client_id else "Новый клиент")
        self.setFixedSize(450, 550)
        self.setStyleSheet("""
            QDialog {
                background-color: white;
                font-family: 'Segoe UI', Arial;
            }
            QLabel {
                color: #2c3e50;
                font-size: 13px;
            }
            QLineEdit, QTextEdit {
                border: 2px solid #dee2e6;
                border-radius: 5px;
                padding: 8px 15px;
                font-size: 12px;
            }
            QLineEdit:focus, QTextEdit:focus {
                border: 2px solid #3498db;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 20px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton#addBtn {
                background-color: #27ae60;
            }
            QPushButton#addBtn:hover {
                background-color: #229954;
            }
        """)
        self.setup_ui()
        
        if client_id:
            self.load_data()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(30, 30, 30, 30)
        
        title = QLabel("👤 " + ("РЕДАКТИРОВАНИЕ КЛИЕНТА" if self.client_id else "НОВЫЙ КЛИЕНТ"))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #3498db; margin-bottom: 10px;")
        layout.addWidget(title)
        
        form = QFormLayout()
        form.setSpacing(15)
        form.setLabelAlignment(Qt.AlignRight)
        
        self.last_name = QLineEdit()
        self.last_name.setPlaceholderText("Иванов")
        form.addRow("Фамилия:*", self.last_name)
        
        self.first_name = QLineEdit()
        self.first_name.setPlaceholderText("Иван")
        form.addRow("Имя:*", self.first_name)
        
        self.middle_name = QLineEdit()
        self.middle_name.setPlaceholderText("Иванович")
        form.addRow("Отчество:", self.middle_name)
        
        self.phone = QLineEdit()
        self.phone.setPlaceholderText("+7 (999) 123-45-67")
        form.addRow("Телефон:*", self.phone)
        
        self.email = QLineEdit()
        self.email.setPlaceholderText("ivanov@mail.ru")
        form.addRow("Email:", self.email)
        
        self.address = QTextEdit()
        self.address.setMaximumHeight(80)
        self.address.setPlaceholderText("г. Москва, ул. Ленина, д. 1")
        form.addRow("Адрес:", self.address)
        
        layout.addLayout(form)
        layout.addStretch()
        
        info = QLabel("Поля, отмеченные *, обязательны для заполнения")
        info.setStyleSheet("color: #6c757d; font-size: 10px;")
        info.setAlignment(Qt.AlignCenter)
        layout.addWidget(info)
        
        btn_layout = QHBoxLayout()
        
        save_btn = QPushButton("✅ СОХРАНИТЬ")
        save_btn.setObjectName("addBtn")
        save_btn.clicked.connect(self.save)
        btn_layout.addWidget(save_btn)
        
        cancel_btn = QPushButton("✖ ОТМЕНА")
        cancel_btn.setStyleSheet("background-color: #e74c3c; color: white;")
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)
        
        layout.addLayout(btn_layout)
        self.setLayout(layout)
    
    def load_data(self):
        data = self.db.fetch_one('''
            SELECT last_name, first_name, middle_name, phone, email, address 
            FROM clients WHERE id = ?
        ''', (self.client_id,))
        
        if data:
            self.last_name.setText(data[0])
            self.first_name.setText(data[1])
            self.middle_name.setText(data[2] or "")
            self.phone.setText(data[3] or "")
            self.email.setText(data[4] or "")
            self.address.setText(data[5] or "")
    
    def save(self):
        if not self.last_name.text() or not self.first_name.text() or not self.phone.text():
            QMessageBox.warning(self, "Ошибка", "Заполните обязательные поля")
            return
        
        if self.client_id:
            query = '''
                UPDATE clients 
                SET last_name=?, first_name=?, middle_name=?, phone=?, email=?, address=?
                WHERE id=?
            '''
            params = (self.last_name.text(), self.first_name.text(), self.middle_name.text(),
                     self.phone.text(), self.email.text(), self.address.toPlainText(), self.client_id)
        else:
            query = '''
                INSERT INTO clients (last_name, first_name, middle_name, phone, email, address, created_date)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            '''
            params = (self.last_name.text(), self.first_name.text(), self.middle_name.text(),
                     self.phone.text(), self.email.text(), self.address.toPlainText(),
                     datetime.now().strftime("%Y-%m-%d"))
        
        self.db.execute_query(query, params)
        self.accept()