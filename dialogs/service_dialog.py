from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class ServiceDialog(QDialog):
    def __init__(self, db, service_id=None):
        super().__init__()
        self.db = db
        self.service_id = service_id
        self.setWindowTitle("Услуга" if service_id else "Новая услуга")
        self.setFixedSize(450, 450)
        self.setStyleSheet(ClientDialog.styleSheet(self))
        self.setup_ui()
        
        if service_id:
            self.load_data()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(30, 30, 30, 30)
        
        title = QLabel("🔧 " + ("РЕДАКТИРОВАНИЕ УСЛУГИ" if self.service_id else "НОВАЯ УСЛУГА"))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #3498db; margin-bottom: 10px;")
        layout.addWidget(title)
        
        form = QFormLayout()
        form.setSpacing(15)
        form.setLabelAlignment(Qt.AlignRight)
        
        self.code = QLineEdit()
        self.code.setPlaceholderText("S001")
        form.addRow("Код:", self.code)
        
        self.name = QLineEdit()
        self.name.setPlaceholderText("Замена масла")
        form.addRow("Название:", self.name)
        
        self.price = QDoubleSpinBox()
        self.price.setRange(0, 100000)
        self.price.setPrefix("₽ ")
        self.price.setValue(1000)
        form.addRow("Цена:", self.price)
        
        self.duration = QSpinBox()
        self.duration.setRange(0, 1000)
        self.duration.setSuffix(" мин")
        self.duration.setValue(60)
        form.addRow("Длительность:", self.duration)
        
        self.category = QLineEdit()
        self.category.setPlaceholderText("ТО")
        form.addRow("Категория:", self.category)
        
        layout.addLayout(form)
        layout.addStretch()
        
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
            SELECT code, name, price, duration, category
            FROM services WHERE id = ?
        ''', (self.service_id,))
        
        if data:
            self.code.setText(data[0])
            self.name.setText(data[1])
            self.price.setValue(data[2])
            self.duration.setValue(data[3] or 0)
            self.category.setText(data[4] or "")
    
    def save(self):
        if not self.code.text() or not self.name.text() or self.price.value() <= 0:
            QMessageBox.warning(self, "Ошибка", "Заполните обязательные поля")
            return
        
        if self.service_id:
            query = '''
                UPDATE services 
                SET code=?, name=?, price=?, duration=?, category=?
                WHERE id=?
            '''
            params = (self.code.text(), self.name.text(), self.price.value(),
                     self.duration.value(), self.category.text(), self.service_id)
        else:
            query = '''
                INSERT INTO services (code, name, price, duration, category)
                VALUES (?, ?, ?, ?, ?)
            '''
            params = (self.code.text(), self.name.text(), self.price.value(),
                     self.duration.value(), self.category.text())
        
        try:
            self.db.execute_query(query, params)
            self.accept()
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", "Услуга с таким кодом уже существует")