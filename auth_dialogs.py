from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from database import PasswordHasher
from dialogs.register_dialog import RegisterDialog

class LoginDialog(QDialog):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.setWindowTitle("АВТОСЕРВИС")
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
            QPushButton#registerBtn {
                background-color: #6c757d;
                color: white;
            }
            QPushButton#registerBtn:hover {
                background-color: #5a6268;
            }
        """)
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(30, 40, 30, 30)
        
        logo = QLabel("🚗 АВТОСЕРВИС")
        logo.setAlignment(Qt.AlignCenter)
        logo.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: white;
            margin-bottom: 20px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        """)
        layout.addWidget(logo)
        
        form = QFormLayout()
        form.setSpacing(15)
        form.setLabelAlignment(Qt.AlignRight)
        
        self.username = QLineEdit()
        self.username.setPlaceholderText("Введите логин")
        form.addRow("Логин:", self.username)
        
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setPlaceholderText("Введите пароль")
        form.addRow("Пароль:", self.password)
        
        layout.addLayout(form)
        layout.addStretch()
        
        self.login_btn = QPushButton("🚪 ВОЙТИ В СИСТЕМУ")
        self.login_btn.clicked.connect(self.check_login)
        layout.addWidget(self.login_btn)
        
        self.change_btn = QPushButton("🔄 СМЕНИТЬ ПАРОЛЬ")
        self.change_btn.setObjectName("registerBtn")
        self.change_btn.clicked.connect(self.change_password)
        layout.addWidget(self.change_btn)
        
        self.exit_btn = QPushButton("✖ ВЫХОД")
        self.exit_btn.setStyleSheet("""
            QPushButton {
                background-color: #dc3545;
                color: white;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
        """)
        self.exit_btn.clicked.connect(self.reject)
        layout.addWidget(self.exit_btn)
        
        self.setLayout(layout)
    
    def check_login(self):
        username = self.username.text().strip()
        password = self.password.text()
        
        if not username or not password:
            QMessageBox.warning(self, "Ошибка", "Введите логин и пароль")
            return
        
        user = self.db.fetch_one('''
            SELECT id, username, password, role, full_name 
            FROM users WHERE LOWER(username) = LOWER(?)
        ''', (username,))
        
        if user and PasswordHasher.verify_password(password, user[2]):
            self.user_data = {
                'id': user[0],
                'username': user[1],
                'role': user[3],
                'full_name': user[4]
            }
            self.accept()
        else:
            QMessageBox.warning(self, "Ошибка", "Неверный логин или пароль")
    
    def change_password(self):
        dialog = ChangePasswordDialog(self.db)
        dialog.exec_()

class ChangePasswordDialog(QDialog):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.setWindowTitle("Смена пароля")
        self.setFixedSize(350, 400)
        self.setStyleSheet(LoginDialog.styleSheet(self))
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(30, 30, 30, 30)
        
        title = QLabel("🔄 СМЕНА ПАРОЛЯ")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: white;")
        layout.addWidget(title)
        
        form = QFormLayout()
        form.setSpacing(15)
        form.setLabelAlignment(Qt.AlignRight)
        
        self.username = QLineEdit()
        self.username.setPlaceholderText("Введите логин")
        form.addRow("Логин:", self.username)
        
        self.old_pass = QLineEdit()
        self.old_pass.setEchoMode(QLineEdit.Password)
        self.old_pass.setPlaceholderText("Старый пароль")
        form.addRow("Старый пароль:", self.old_pass)
        
        self.new_pass = QLineEdit()
        self.new_pass.setEchoMode(QLineEdit.Password)
        self.new_pass.setPlaceholderText("Новый пароль")
        form.addRow("Новый пароль:", self.new_pass)
        
        self.confirm = QLineEdit()
        self.confirm.setEchoMode(QLineEdit.Password)
        self.confirm.setPlaceholderText("Подтверждение")
        form.addRow("Подтверждение:", self.confirm)
        
        layout.addLayout(form)
        layout.addStretch()
        
        info = QLabel("Все поля обязательны для заполнения")
        info.setStyleSheet("color: #ffd166; font-size: 10px;")
        info.setAlignment(Qt.AlignCenter)
        layout.addWidget(info)
        
        btn_layout = QHBoxLayout()
        
        save_btn = QPushButton("✅ СОХРАНИТЬ")
        save_btn.clicked.connect(self.save_password)
        btn_layout.addWidget(save_btn)
        
        cancel_btn = QPushButton("✖ ОТМЕНА")
        cancel_btn.setStyleSheet("background-color: #dc3545; color: white;")
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)
        
        layout.addLayout(btn_layout)
        self.setLayout(layout)
    
    def save_password(self):
        username = self.username.text().strip()
        old = self.old_pass.text()
        new = self.new_pass.text()
        confirm = self.confirm.text()
        
        if not all([username, old, new, confirm]):
            QMessageBox.warning(self, "Ошибка", "Заполните все поля")
            return
        
        if new != confirm:
            QMessageBox.warning(self, "Ошибка", "Новые пароли не совпадают")
            return
        
        user = self.db.fetch_one('''
            SELECT id, password FROM users WHERE LOWER(username) = LOWER(?)
        ''', (username,))
        
        if not user:
            QMessageBox.warning(self, "Ошибка", "Пользователь не найден")
            return
        
        if not PasswordHasher.verify_password(old, user[1]):
            QMessageBox.warning(self, "Ошибка", "Неверный старый пароль")
            return
        
        hashed = PasswordHasher.hash_password(new)
        self.db.execute_query('UPDATE users SET password = ? WHERE id = ?', (hashed, user[0]))
        
        QMessageBox.information(self, "Успех", "Пароль успешно изменен")
        self.accept()