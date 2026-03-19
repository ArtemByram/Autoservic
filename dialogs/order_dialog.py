from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from datetime import datetime

class OrderDialog(QDialog):
    def __init__(self, db, order_id=None):
        super().__init__()
        self.db = db
        self.order_id = order_id
        self.setWindowTitle("Заказ-наряд" if order_id else "Новый заказ-наряд")
        self.setGeometry(200, 200, 1000, 700)
        self.setStyleSheet("""
            QDialog {
                background-color: white;
                font-family: 'Segoe UI', Arial;
            }
            QGroupBox {
                background-color: #f8f9fa;
                border: 2px solid #3498db;
                border-radius: 8px;
                margin-top: 15px;
                font-weight: bold;
                color: #3498db;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 10px;
            }
            QTableWidget {
                background-color: white;
                alternate-background-color: #f8f9fa;
                selection-background-color: #3498db;
                selection-color: white;
                gridline-color: #dee2e6;
                font-size: 12px;
                border: none;
                border-radius: 8px;
            }
            QHeaderView::section {
                background-color: #2c3e50;
                color: white;
                padding: 10px;
                font-size: 12px;
                font-weight: bold;
                border: none;
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
            QComboBox {
                border: 2px solid #dee2e6;
                border-radius: 5px;
                padding: 8px 15px;
                font-size: 12px;
            }
        """)
        self.setup_ui()
        
        if order_id:
            self.load_order()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        title = QLabel("📋 " + ("РЕДАКТИРОВАНИЕ ЗАКАЗА" if self.order_id else "НОВЫЙ ЗАКАЗ-НАРЯД"))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #3498db; margin-bottom: 10px;")
        layout.addWidget(title)
        
        info_group = QGroupBox("Информация о заказе")
        info_layout = QGridLayout(info_group)
        
        info_layout.addWidget(QLabel("Клиент:"), 0, 0)
        self.client_combo = QComboBox()
        self.client_combo.currentIndexChanged.connect(self.load_cars)
        info_layout.addWidget(self.client_combo, 0, 1)
        
        info_layout.addWidget(QLabel("Автомобиль:"), 0, 2)
        self.car_combo = QComboBox()
        info_layout.addWidget(self.car_combo, 0, 3)
        
        info_layout.addWidget(QLabel("Статус:"), 1, 2)
        self.status_combo = QComboBox()
        self.status_combo.addItems(["новый", "в работе", "готов", "закрыт"])
        info_layout.addWidget(self.status_combo, 1, 3)
        
        info_layout.addWidget(QLabel("Оплата:"), 2, 2)
        self.payment_combo = QComboBox()
        self.payment_combo.addItems(["не оплачен", "оплачен"])
        info_layout.addWidget(self.payment_combo, 2, 3)
        
        layout.addWidget(info_group)
        
        tabs = QTabWidget()
        
        services_tab = QWidget()
        services_layout = QVBoxLayout(services_tab)
        
        services_layout.addWidget(QLabel("🔧 Доступные услуги:"))
        
        self.services_table = QTableWidget()
        self.services_table.setColumnCount(5)
        self.services_table.setHorizontalHeaderLabels(["ID", "Код", "Услуга", "Цена", ""])
        self.services_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.services_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.load_services()
        services_layout.addWidget(self.services_table)
        
        services_layout.addWidget(QLabel("✅ Выбранные услуги:"))
        self.selected_services = QTableWidget()
        self.selected_services.setColumnCount(5)
        self.selected_services.setHorizontalHeaderLabels(["ID", "Услуга", "Кол-во", "Цена", ""])
        self.selected_services.setSelectionBehavior(QTableWidget.SelectRows)
        self.selected_services.itemChanged.connect(self.calc_total)
        services_layout.addWidget(self.selected_services)
        
        tabs.addTab(services_tab, "🔧 Услуги")
        
        parts_tab = QWidget()
        parts_layout = QVBoxLayout(parts_tab)
        
        parts_layout.addWidget(QLabel("⚙️ Доступные запчасти:"))
        
        self.parts_table = QTableWidget()
        self.parts_table.setColumnCount(6)
        self.parts_table.setHorizontalHeaderLabels(["ID", "Код", "Запчасть", "Цена", "В наличии", ""])
        self.parts_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.parts_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.load_parts()
        parts_layout.addWidget(self.parts_table)
        
        parts_layout.addWidget(QLabel("✅ Выбранные запчасти:"))
        self.selected_parts = QTableWidget()
        self.selected_parts.setColumnCount(5)
        self.selected_parts.setHorizontalHeaderLabels(["ID", "Запчасть", "Кол-во", "Цена", ""])
        self.selected_parts.setSelectionBehavior(QTableWidget.SelectRows)
        self.selected_parts.itemChanged.connect(self.calc_total)
        parts_layout.addWidget(self.selected_parts)
        
        tabs.addTab(parts_tab, "⚙️ Запчасти")
        
        layout.addWidget(tabs)
        
        total_widget = QWidget()
        total_widget.setStyleSheet("background-color: #2c3e50; color: white; border-radius: 8px; padding: 10px;")
        total_layout = QHBoxLayout(total_widget)
        total_layout.addStretch()
        total_layout.addWidget(QLabel("ИТОГО:"))
        self.total_label = QLabel("0.00 ₽")
        self.total_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #ffd166;")
        total_layout.addWidget(self.total_label)
        total_layout.addStretch()
        
        layout.addWidget(total_widget)
        
        notes_layout = QHBoxLayout()
        notes_layout.addWidget(QLabel("Примечание:"))
        self.notes = QLineEdit()
        self.notes.setPlaceholderText("Дополнительная информация по заказу")
        notes_layout.addWidget(self.notes)
        layout.addLayout(notes_layout)
        
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        save_btn = QPushButton("✅ СОХРАНИТЬ ЗАКАЗ")
        save_btn.setObjectName("addBtn")
        save_btn.clicked.connect(self.save_order)
        btn_layout.addWidget(save_btn)
        
        cancel_btn = QPushButton("✖ ОТМЕНА")
        cancel_btn.setStyleSheet("background-color: #e74c3c; color: white;")
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)
        btn_layout.addStretch()
        
        layout.addLayout(btn_layout)
        
        self.setLayout(layout)
        
        self.load_clients()
    
    def load_clients(self):
        clients = self.db.fetch_all("SELECT id, last_name || ' ' || first_name FROM clients ORDER BY last_name")
        self.client_combo.clear()
        self.client_combo.addItem("-- Выберите клиента --", None)
        for cid, name in clients:
            self.client_combo.addItem(name, cid)
    
    def load_cars(self):
        self.car_combo.clear()
        client_id = self.client_combo.currentData()
        if client_id:
            cars = self.db.fetch_all("SELECT id, brand || ' ' || model || ' (' || license_plate || ')' FROM cars WHERE client_id = ?", (client_id,))
            self.car_combo.addItem("-- Выберите автомобиль --", None)
            for cid, name in cars:
                self.car_combo.addItem(name, cid)
        else:
            self.car_combo.addItem("-- Сначала выберите клиента --", None)
    
    def load_services(self):
        services = self.db.fetch_all("SELECT id, code, name, price FROM services ORDER BY name")
        self.services_table.setRowCount(len(services))
        for i, s in enumerate(services):
            self.services_table.setItem(i, 0, QTableWidgetItem(str(s[0])))
            self.services_table.setItem(i, 1, QTableWidgetItem(s[1]))
            self.services_table.setItem(i, 2, QTableWidgetItem(s[2]))
            self.services_table.setItem(i, 3, QTableWidgetItem(f"{s[3]:.2f} ₽"))
            
            add_btn = QPushButton("➕")
            add_btn.setFixedSize(30, 30)
            add_btn.clicked.connect(lambda checked, sid=s[0], name=s[2], price=s[3]: self.add_service(sid, name, price))
            self.services_table.setCellWidget(i, 4, add_btn)
        
        self.services_table.resizeColumnsToContents()
        self.services_table.setColumnWidth(4, 40)
    
    def load_parts(self):
        parts = self.db.fetch_all("SELECT id, code, name, price, quantity FROM parts WHERE quantity > 0 ORDER BY name")
        self.parts_table.setRowCount(len(parts))
        for i, p in enumerate(parts):
            self.parts_table.setItem(i, 0, QTableWidgetItem(str(p[0])))
            self.parts_table.setItem(i, 1, QTableWidgetItem(p[1]))
            self.parts_table.setItem(i, 2, QTableWidgetItem(p[2]))
            self.parts_table.setItem(i, 3, QTableWidgetItem(f"{p[3]:.2f} ₽"))
            self.parts_table.setItem(i, 4, QTableWidgetItem(str(p[4])))
            
            add_btn = QPushButton("➕")
            add_btn.setFixedSize(30, 30)
            add_btn.clicked.connect(lambda checked, pid=p[0], name=p[2], price=p[3], qty=p[4]: self.add_part(pid, name, price, qty))
            self.parts_table.setCellWidget(i, 5, add_btn)
        
        self.parts_table.resizeColumnsToContents()
        self.parts_table.setColumnWidth(5, 40)
    
    def add_service(self, service_id, service_name, service_price):
        for i in range(self.selected_services.rowCount()):
            if self.selected_services.cellWidget(i, 4) and int(self.selected_services.item(i, 0).text()) == service_id:
                qty = int(self.selected_services.item(i, 2).text()) + 1
                self.selected_services.item(i, 2).setText(str(qty))
                self.calc_total()
                return
        
        row = self.selected_services.rowCount()
        self.selected_services.setRowCount(row + 1)
        
        self.selected_services.setItem(row, 0, QTableWidgetItem(str(service_id)))
        self.selected_services.setItem(row, 1, QTableWidgetItem(service_name))
        
        qty_item = QTableWidgetItem("1")
        qty_item.setFlags(qty_item.flags() | Qt.ItemIsEditable)
        self.selected_services.setItem(row, 2, qty_item)
        
        price_item = QTableWidgetItem(f"{service_price:.2f} ₽")
        price_item.setFlags(price_item.flags() & ~Qt.ItemIsEditable)
        self.selected_services.setItem(row, 3, price_item)
        
        del_btn = QPushButton("🗑️")
        del_btn.setFixedSize(30, 30)
        del_btn.setStyleSheet("background-color: #e74c3c; color: white;")
        del_btn.clicked.connect(lambda: self.remove_selected_row(self.selected_services, row))
        self.selected_services.setCellWidget(row, 4, del_btn)
        
        self.calc_total()
    
    def add_part(self, part_id, part_name, part_price, available):
        for i in range(self.selected_parts.rowCount()):
            if self.selected_parts.cellWidget(i, 4) and int(self.selected_parts.item(i, 0).text()) == part_id:
                qty = int(self.selected_parts.item(i, 2).text()) + 1
                if qty > available:
                    QMessageBox.warning(self, "Ошибка", f"Доступно только {available} шт.")
                    return
                self.selected_parts.item(i, 2).setText(str(qty))
                self.calc_total()
                return
        
        row = self.selected_parts.rowCount()
        self.selected_parts.setRowCount(row + 1)
        
        self.selected_parts.setItem(row, 0, QTableWidgetItem(str(part_id)))
        self.selected_parts.setItem(row, 1, QTableWidgetItem(part_name))
        
        qty_item = QTableWidgetItem("1")
        qty_item.setFlags(qty_item.flags() | Qt.ItemIsEditable)
        self.selected_parts.setItem(row, 2, qty_item)
        
        price_item = QTableWidgetItem(f"{part_price:.2f} ₽")
        price_item.setFlags(price_item.flags() & ~Qt.ItemIsEditable)
        self.selected_parts.setItem(row, 3, price_item)
        
        del_btn = QPushButton("🗑️")
        del_btn.setFixedSize(30, 30)
        del_btn.setStyleSheet("background-color: #e74c3c; color: white;")
        del_btn.clicked.connect(lambda: self.remove_selected_row(self.selected_parts, row))
        self.selected_parts.setCellWidget(row, 4, del_btn)
        
        self.calc_total()
    
    def remove_selected_row(self, table, row):
        table.removeRow(row)
        self.calc_total()
    
    def calc_total(self):
        total = 0
        
        for i in range(self.selected_services.rowCount()):
            qty_item = self.selected_services.item(i, 2)
            price_item = self.selected_services.item(i, 3)
            if qty_item and price_item:
                try:
                    qty = int(qty_item.text() or "1")
                    price = float(price_item.text().replace('₽', '').replace(',', '').strip() or "0")
                    total += qty * price
                except:
                    pass
        
        for i in range(self.selected_parts.rowCount()):
            qty_item = self.selected_parts.item(i, 2)
            price_item = self.selected_parts.item(i, 3)
            if qty_item and price_item:
                try:
                    qty = int(qty_item.text() or "1")
                    price = float(price_item.text().replace('₽', '').replace(',', '').strip() or "0")
                    total += qty * price
                except:
                    pass
        
        self.total_label.setText(f"{total:,.2f} ₽")
    
    def save_order(self):
        if not self.client_combo.currentData():
            QMessageBox.warning(self, "Ошибка", "Выберите клиента")
            return
        
        if not self.car_combo.currentData():
            QMessageBox.warning(self, "Ошибка", "Выберите автомобиль")
            return
        
        if self.selected_services.rowCount() == 0 and self.selected_parts.rowCount() == 0:
            QMessageBox.warning(self, "Ошибка", "Добавьте услуги или запчасти")
            return
        
        reply = QMessageBox.question(self, "Подтверждение", "Сохранить заказ?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply != QMessageBox.Yes:
            return
        
        try:
            number = f"ЗН-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
            total_text = self.total_label.text().replace('₽', '').replace(',', '').strip()
            total = float(total_text) if total_text else 0
            
            employee = self.db.fetch_one("SELECT id FROM employees LIMIT 1")
            employee_id = employee[0] if employee else None
            
            if self.order_id:
                query = '''
                    UPDATE orders SET
                        client_id=?, car_id=?, employee_id=?, status=?, payment_status=?, total_cost=?, notes=?
                    WHERE id=?
                '''
                params = (self.client_combo.currentData(), self.car_combo.currentData(), employee_id,
                         self.status_combo.currentText(), self.payment_combo.currentText(),
                         total, self.notes.text(), self.order_id)
            else:
                query = '''
                    INSERT INTO orders 
                    (order_number, client_id, car_id, employee_id, created_date, status, payment_status, total_cost, notes)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                '''
                params = (number, self.client_combo.currentData(), self.car_combo.currentData(), employee_id,
                         datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                         self.status_combo.currentText(), self.payment_combo.currentText(), total, self.notes.text())
            
            self.db.execute_query(query, params)
            
            if not self.order_id:
                self.order_id = self.db.cursor.lastrowid
            
            self.db.execute_query("DELETE FROM order_services WHERE order_id = ?", (self.order_id,))
            for i in range(self.selected_services.rowCount()):
                sid_item = self.selected_services.item(i, 0)
                qty_item = self.selected_services.item(i, 2)
                price_item = self.selected_services.item(i, 3)
                
                if sid_item and qty_item and price_item:
                    sid = int(sid_item.text())
                    qty = int(qty_item.text())
                    price = float(price_item.text().replace('₽', '').replace(',', '').strip())
                    self.db.execute_query('''
                        INSERT INTO order_services (order_id, service_id, quantity, price)
                        VALUES (?, ?, ?, ?)
                    ''', (self.order_id, sid, qty, price))
            
            self.db.execute_query("DELETE FROM order_parts WHERE order_id = ?", (self.order_id,))
            for i in range(self.selected_parts.rowCount()):
                pid_item = self.selected_parts.item(i, 0)
                qty_item = self.selected_parts.item(i, 2)
                price_item = self.selected_parts.item(i, 3)
                
                if pid_item and qty_item and price_item:
                    pid = int(pid_item.text())
                    qty = int(qty_item.text())
                    price = float(price_item.text().replace('₽', '').replace(',', '').strip())
                    
                    current = self.db.fetch_one("SELECT quantity FROM parts WHERE id = ?", (pid,))[0]
                    if current < qty:
                        QMessageBox.warning(self, "Ошибка", f"Недостаточно запчастей на складе")
                        return
                    
                    self.db.execute_query("UPDATE parts SET quantity = ? WHERE id = ?", (current - qty, pid))
                    
                    self.db.execute_query('''
                        INSERT INTO parts_movement (part_id, type, quantity, date, order_id, notes)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', (pid, 'расход', qty, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
                          self.order_id, f"Заказ {number}"))
                    
                    self.db.execute_query('''
                        INSERT INTO order_parts (order_id, part_id, quantity, price)
                        VALUES (?, ?, ?, ?)
                    ''', (self.order_id, pid, qty, price))
            
            QMessageBox.information(self, "Успех", f"Заказ сохранен\nНомер: {number}")
            self.accept()
            
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))
    
    def load_order(self):
        order = self.db.fetch_one('''
            SELECT client_id, car_id, status, payment_status, notes
            FROM orders WHERE id = ?
        ''', (self.order_id,))
        
        if order:
            idx = self.client_combo.findData(order[0])
            if idx >= 0:
                self.client_combo.setCurrentIndex(idx)
            
            self.load_cars()
            car_idx = self.car_combo.findData(order[1])
            if car_idx >= 0:
                self.car_combo.setCurrentIndex(car_idx)
            
            status_idx = self.status_combo.findText(order[2])
            if status_idx >= 0:
                self.status_combo.setCurrentIndex(status_idx)
            
            pay_idx = self.payment_combo.findText(order[3])
            if pay_idx >= 0:
                self.payment_combo.setCurrentIndex(pay_idx)
            
            self.notes.setText(order[4] or "")
            
            services = self.db.fetch_all('''
                SELECT order_services.service_id, services.name, order_services.quantity, order_services.price
                FROM order_services
                JOIN services ON order_services.service_id = services.id
                WHERE order_services.order_id = ?
            ''', (self.order_id,))
            
            for s in services:
                row = self.selected_services.rowCount()
                self.selected_services.setRowCount(row + 1)
                self.selected_services.setItem(row, 0, QTableWidgetItem(str(s[0])))
                self.selected_services.setItem(row, 1, QTableWidgetItem(s[1]))
                self.selected_services.setItem(row, 2, QTableWidgetItem(str(s[2])))
                self.selected_services.setItem(row, 3, QTableWidgetItem(f"{s[3]:.2f} ₽"))
                
                del_btn = QPushButton("🗑️")
                del_btn.setFixedSize(30, 30)
                del_btn.setStyleSheet("background-color: #e74c3c; color: white;")
                del_btn.clicked.connect(lambda checked, r=row: self.remove_selected_row(self.selected_services, r))
                self.selected_services.setCellWidget(row, 4, del_btn)
            
            parts = self.db.fetch_all('''
                SELECT order_parts.part_id, parts.name, order_parts.quantity, order_parts.price
                FROM order_parts
                JOIN parts ON order_parts.part_id = parts.id
                WHERE order_parts.order_id = ?
            ''', (self.order_id,))
            
            for p in parts:
                row = self.selected_parts.rowCount()
                self.selected_parts.setRowCount(row + 1)
                self.selected_parts.setItem(row, 0, QTableWidgetItem(str(p[0])))
                self.selected_parts.setItem(row, 1, QTableWidgetItem(p[1]))
                self.selected_parts.setItem(row, 2, QTableWidgetItem(str(p[2])))
                self.selected_parts.setItem(row, 3, QTableWidgetItem(f"{p[3]:.2f} ₽"))
                
                del_btn = QPushButton("🗑️")
                del_btn.setFixedSize(30, 30)
                del_btn.setStyleSheet("background-color: #e74c3c; color: white;")
                del_btn.clicked.connect(lambda checked, r=row: self.remove_selected_row(self.selected_parts, r))
                self.selected_parts.setCellWidget(row, 4, del_btn)
            
            self.calc_total()