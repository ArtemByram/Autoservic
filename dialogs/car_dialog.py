from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from datetime import datetime

class CarDialog(QDialog):
    def __init__(self, db, car_id=None):
        super().__init__()
        self.db = db
        self.car_id = car_id
        self.setWindowTitle("Автомобиль" if car_id else "Новый автомобиль")
        self.setFixedSize(500, 600)
        self.setStyleSheet(ClientDialog.styleSheet(self))
        self.setup_ui()
        
        if car_id:
            self.load_data()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(30, 30, 30, 30)
        
        title = QLabel("🚗 " + ("РЕДАКТИРОВАНИЕ АВТОМОБИЛЯ" if self.car_id else "НОВЫЙ АВТОМОБИЛЬ"))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #3498db; margin-bottom: 10px;")
        layout.addWidget(title)
        
        form = QFormLayout()
        form.setSpacing(15)
        form.setLabelAlignment(Qt.AlignRight)
        
        self.client_combo = QComboBox()
        self.load_clients()
        form.addRow("Владелец:*", self.client_combo)
        
        self.brand = QLineEdit()
        self.brand.setPlaceholderText("Toyota")
        form.addRow("Марка:*", self.brand)
        
        self.model = QLineEdit()
        self.model.setPlaceholderText("Camry")
        form.addRow("Модель:*", self.model)
        
        self.year = QSpinBox()
        self.year.setRange(1900, datetime.now().year + 1)
        self.year.setValue(2020)
        form.addRow("Год выпуска:", self.year)
        
        self.vin = QLineEdit()
        self.vin.setPlaceholderText("VIN номер")
        form.addRow("VIN:", self.vin)
        
        self.license = QLineEdit()
        self.license.setPlaceholderText("А123ВС777")
        form.addRow("Госномер:*", self.license)
        
        self.color = QLineEdit()
        self.color.setPlaceholderText("Черный")
        form.addRow("Цвет:", self.color)
        
        self.mileage = QSpinBox()
        self.mileage.setRange(0, 999999)
        self.mileage.setSingleStep(1000)
        self.mileage.setSuffix(" км")
        form.addRow("Пробег:", self.mileage)
        
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
    
    def load_clients(self):
        clients = self.db.fetch_all("SELECT id, last_name || ' ' || first_name || ' (' || phone || ')' FROM clients")
        self.client_combo.clear()
        self.client_combo.addItem("-- Выберите владельца --", None)
        for cid, name in clients:
            self.client_combo.addItem(name, cid)
    
    def load_data(self):
        data = self.db.fetch_one('''
            SELECT client_id, brand, model, year, vin, license_plate, color, mileage
            FROM cars WHERE id = ?
        ''', (self.car_id,))
        
        if data:
            idx = self.client_combo.findData(data[0])
            if idx >= 0:
                self.client_combo.setCurrentIndex(idx)
            self.brand.setText(data[1])
            self.model.setText(data[2])
            self.year.setValue(data[3] or 2020)
            self.vin.setText(data[4] or "")
            self.license.setText(data[5] or "")
            self.color.setText(data[6] or "")
            self.mileage.setValue(data[7] or 0)
    
    def save(self):
        if not self.brand.text() or not self.model.text() or not self.license.text():
            QMessageBox.warning(self, "Ошибка", "Заполните обязательные поля")
            return
        
        client_id = self.client_combo.currentData()
        if not client_id:
            QMessageBox.warning(self, "Ошибка", "Выберите владельца")
            return
        
        if self.car_id:
            query = '''
                UPDATE cars 
                SET client_id=?, brand=?, model=?, year=?, vin=?, license_plate=?, color=?, mileage=?
                WHERE id=?
            '''
            params = (client_id, self.brand.text(), self.model.text(), self.year.value(),
                     self.vin.text(), self.license.text(), self.color.text(),
                     self.mileage.value(), self.car_id)
        else:
            query = '''
                INSERT INTO cars (client_id, brand, model, year, vin, license_plate, color, mileage)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            '''
            params = (client_id, self.brand.text(), self.model.text(), self.year.value(),
                     self.vin.text(), self.license.text(), self.color.text(),
                     self.mileage.value())
        
        try:
            self.db.execute_query(query, params)
            self.accept()
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", "Автомобиль с таким номером уже существует")