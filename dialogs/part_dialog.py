from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class PartDialog(QDialog):
    def __init__(self, db, part_id=None):
        super().__init__()
        self.db = db
        self.part_id = part_id
        self.setWindowTitle("Запчасть" if part_id else "Новая запчасть")
        self.setFixedSize(450, 500)
        self.setStyleSheet(ClientDialog.styleSheet(self))
        self.setup_ui()
        
        if part_id:
            self.load_data()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(30, 30, 30, 30)
        
        title = QLabel("⚙️ " + ("РЕДАКТИРОВАНИЕ ЗАПЧАСТИ" if self.part_id else "НОВАЯ ЗАПЧАСТЬ"))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #3498db; margin-bottom: 10px;")
        layout.addWidget(title)
        
        form = QFormLayout()
        form.setSpacing(15)
        form.setLabelAlignment(Qt.AlignRight)
        
        self.code = QLineEdit()
        self.code.setPlaceholderText("P001")
        form.addRow("Код:*", self.code)
        
        self.name = QLineEdit()
        self.name.setPlaceholderText("Масляный фильтр")
        form.addRow("Название:*", self.name)
        
        self.price = QDoubleSpinBox()
        self.price.setRange(0, 100000)
        self.price.setPrefix("₽ ")
        self.price.setValue(500)
        form.addRow("Цена:*", self.price)
        
        self.quantity = QSpinBox()
        self.quantity.setRange(0, 99999)
        self.quantity.setValue(10)
        form.addRow("Количество:", self.quantity)
        
        self.min_qty = QSpinBox()
        self.min_qty.setRange(0, 99999)
        self.min_qty.setValue(5)
        form.addRow("Мин. количество:", self.min_qty)
        
        self.supplier = QLineEdit()
        self.supplier.setPlaceholderText("ООО Автозапчасти")
        form.addRow("Поставщик:", self.supplier)
        
        layout.addLayout(form)
        layout.addStretch()
        
        info = QLabel("Поля, отмеченные , обязательны для заполнения")
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
            SELECT code, name, price, quantity, min_quantity, supplier
            FROM parts WHERE id = ?
        ''', (self.part_id,))
        
        if data:
            self.code.setText(data[0])
            self.name.setText(data[1])
            self.price.setValue(data[2])
            self.quantity.setValue(data[3])
            self.min_qty.setValue(data[4])
            self.supplier.setText(data[5] or "")
    
    def save(self):
        if not self.code.text() or not self.name.text() or self.price.value() <= 0:
            QMessageBox.warning(self, "Ошибка", "Заполните обязательные поля")
            return
        
        if self.part_id:
            query = '''
                UPDATE parts 
                SET code=?, name=?, price=?, quantity=?, min_quantity=?, supplier=?
                WHERE id=?
            '''
            params = (self.code.text(), self.name.text(), self.price.value(),
                     self.quantity.value(), self.min_qty.value(), self.supplier.text(),
                     self.part_id)
        else:
            query = '''
                INSERT INTO parts (code, name, price, quantity, min_quantity, supplier)
                VALUES (?, ?, ?, ?, ?, ?)
            '''
            params = (self.code.text(), self.name.text(), self.price.value(),
                     self.quantity.value(), self.min_qty.value(), self.supplier.text())
        
        try:
            self.db.execute_query(query, params)
            self.accept()
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", "Запчасть с таким кодом уже существует")