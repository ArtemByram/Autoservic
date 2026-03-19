from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from database import PasswordHasher

class RegisterDialog(QDialog):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.setWindowTitle("Регистрация нового пользователя")
        self.setFixedSize(400, 500)
        self.setStyleSheet("""
            QDialog {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #667eea, stop:1 #764ba2);
                font-family: 'Segoe UI', Arial;
            }
            QLabel {
                color: white;
                font-size: 14px;
            }
            QLineEdit {
                background-color: rgba(255, 255, 255, 0.95);
                border: none;
                border-radius: 8px;
                padding: 12px;
                font-size: 14px;
                color: #333;
            }
            QLineEdit:focus {
                background-color: white;
                border: 2px solid #ffd166;
            }
            QPushButton {
                background-color: #ffd166;
                color: #333;
                border: none;
                border-radius: 8px;
                padding: 14px;
                font-size: 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #ffc233;
            }
            QPushButton#addBtn {
                background-color: #27ae60;
                color: white;
            }
            QPushButton#addBtn:hover {
                background-color: #229954;
            }
        """)
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(30, 30, 30, 30)
        
        title = QLabel("📝 РЕГИСТРАЦИЯ")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: white; margin-bottom: 10px;")
        layout.addWidget(title)
        
        form = QFormLayout()
        form.setSpacing(15)
        form.setLabelAlignment(Qt.AlignRight)
        
        self.full_name = QLineEdit()
        self.full_name.setPlaceholderText("Иванов Иван Иванович")
        form.addRow("ФИО:*", self.full_name)
        
        self.username = QLineEdit()
        self.username.setPlaceholderText("ivanov")
        form.addRow("Логин:*", self.username)
        
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setPlaceholderText("******")
        form.addRow("Пароль:*", self.password)
        
        self.confirm = QLineEdit()
        self.confirm.setEchoMode(QLineEdit.Password)
        self.confirm.setPlaceholderText("******")
        form.addRow("Подтверждение:*", self.confirm)
        
        self.role = QComboBox()
        self.role.addItems(["manager", "admin"])
        form.addRow("Роль:", self.role)
        
        layout.addLayout(form)
        layout.addStretch()
        
        info = QLabel("Поля, отмеченные *, обязательны для заполнения")
        info.setStyleSheet("color: #ffd166; font-size: 10px;")
        info.setAlignment(Qt.AlignCenter)
        layout.addWidget(info)
        
        btn_layout = QHBoxLayout()
        
        save_btn = QPushButton("✅ ЗАРЕГИСТРИРОВАТЬ")
        save_btn.setObjectName("addBtn")
        save_btn.clicked.connect(self.register)
        btn_layout.addWidget(save_btn)
        
        cancel_btn = QPushButton("✖ ОТМЕНА")
        cancel_btn.setStyleSheet("background-color: #dc3545; color: white;")
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)
        
        layout.addLayout(btn_layout)
        self.setLayout(layout)
    
    def register(self):
        full_name = self.full_name.text().strip()
        username = self.username.text().strip()
        password = self.password.text()
        confirm = self.confirm.text()
        role = self.role.currentText()
        
        if not all([full_name, username, password, confirm]):
            QMessageBox.warning(self, "Ошибка", "Заполните все обязательные поля")
            return
        
        if password != confirm:
            QMessageBox.warning(self, "Ошибка", "Пароли не совпадают")
            return
        
        existing = self.db.fetch_one("SELECT id FROM users WHERE LOWER(username) = LOWER(?)", (username,))
        if existing:
            QMessageBox.warning(self, "Ошибка", "Пользователь с таким логином уже существует")
            return
        
        hashed = PasswordHasher.hash_password(password)
        self.db.execute_query('''
            INSERT INTO users (username, password, role, full_name)
            VALUES (?, ?, ?, ?)
        ''', (username, hashed, role, full_name))
        
        QMessageBox.information(self, "Успех", "Пользователь успешно зарегистрирован")
        self.accept()