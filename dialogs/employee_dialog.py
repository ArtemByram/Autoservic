from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class EmployeeDialog(QDialog):
    def __init__(self, db, emp_id=None):
        super().__init__()
        self.db = db
        self.emp_id = emp_id
        self.setWindowTitle("Сотрудник" if emp_id else "Новый сотрудник")
        self.setFixedSize(450, 500)
        self.setStyleSheet(ClientDialog.styleSheet(self))
        self.setup_ui()
        
        if emp_id:
            self.load_data()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(30, 30, 30, 30)
        
        title = QLabel("👤 " + ("РЕДАКТИРОВАНИЕ СОТРУДНИКА" if self.emp_id else "НОВЫЙ СОТРУДНИК"))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #3498db; margin-bottom: 10px;")
        layout.addWidget(title)
        
        form = QFormLayout()
        form.setSpacing(15)
        form.setLabelAlignment(Qt.AlignRight)
        
        self.last_name = QLineEdit()
        self.last_name.setPlaceholderText("Петров")
        form.addRow("Фамилия:*", self.last_name)
        
        self.first_name = QLineEdit()
        self.first_name.setPlaceholderText("Петр")
        form.addRow("Имя:*", self.first_name)
        
        self.middle_name = QLineEdit()
        self.middle_name.setPlaceholderText("Петрович")
        form.addRow("Отчество:", self.middle_name)
        
        self.position = QLineEdit()
        self.position.setPlaceholderText("Мастер")
        form.addRow("Должность:*", self.position)
        
        self.phone = QLineEdit()
        self.phone.setPlaceholderText("+7 (999) 123-45-67")
        form.addRow("Телефон:*", self.phone)
        
        self.email = QLineEdit()
        self.email.setPlaceholderText("petrov@autoservice.ru")
        form.addRow("Email:", self.email)
        
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
            SELECT last_name, first_name, middle_name, position, phone, email
            FROM employees WHERE id = ?
        ''', (self.emp_id,))
        
        if data:
            self.last_name.setText(data[0])
            self.first_name.setText(data[1])
            self.middle_name.setText(data[2] or "")
            self.position.setText(data[3])
            self.phone.setText(data[4])
            self.email.setText(data[5] or "")
    
    def save(self):
        if not all([self.last_name.text(), self.first_name.text(), 
                   self.position.text(), self.phone.text()]):
            QMessageBox.warning(self, "Ошибка", "Заполните обязательные поля")
            return
        
        if self.emp_id:
            query = '''
                UPDATE employees 
                SET last_name=?, first_name=?, middle_name=?, position=?, phone=?, email=?
                WHERE id=?
            '''
            params = (self.last_name.text(), self.first_name.text(), self.middle_name.text(),
                     self.position.text(), self.phone.text(), self.email.text(), self.emp_id)
        else:
            query = '''
                INSERT INTO employees (last_name, first_name, middle_name, position, phone, email)
                VALUES (?, ?, ?, ?, ?, ?)
            '''
            params = (self.last_name.text(), self.first_name.text(), self.middle_name.text(),
                     self.position.text(), self.phone.text(), self.email.text())
        
        self.db.execute_query(query, params)
        self.accept()