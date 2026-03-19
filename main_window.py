from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from datetime import datetime
from dialogs import *

class MainWindow(QMainWindow):
    def __init__(self, db, user_data):
        super().__init__()
        self.db = db
        self.user_data = user_data
        self.setWindowTitle(f"АВТОСЕРВИС - {user_data['full_name']} ({'Администратор' if user_data['role'] == 'admin' else 'Менеджер'})")
        self.setGeometry(100, 100, 1300, 800)
        
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f8f9fa;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QMenuBar {
                background-color: #2c3e50;
                color: #ecf0f1;
                font-size: 13px;
                padding: 5px;
            }
            QMenuBar::item {
                padding: 8px 15px;
                border-radius: 5px;
            }
            QMenuBar::item:selected {
                background-color: #3498db;
                color: white;
            }
            QMenu {
                background-color: #2c3e50;
                color: #ecf0f1;
                border: 1px solid #34495e;
                border-radius: 5px;
            }
            QMenu::item {
                padding: 8px 25px;
                border-radius: 3px;
            }
            QMenu::item:selected {
                background-color: #3498db;
                color: white;
            }
            QToolBar {
                background-color: white;
                border-bottom: 2px solid #3498db;
                padding: 8px;
                spacing: 10px;
            }
            QToolButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 15px;
                font-size: 12px;
                font-weight: bold;
            }
            QToolButton:hover {
                background-color: #2980b9;
            }
            QStatusBar {
                background-color: #2c3e50;
                color: #ecf0f1;
                font-size: 12px;
                padding: 5px;
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
            QTableWidget::item {
                padding: 8px;
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
            QPushButton#deleteBtn {
                background-color: #e74c3c;
            }
            QPushButton#deleteBtn:hover {
                background-color: #c0392b;
            }
            QGroupBox {
                background-color: white;
                border: 2px solid #3498db;
                border-radius: 8px;
                margin-top: 15px;
                font-size: 13px;
                font-weight: bold;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 10px;
                color: #3498db;
            }
            QComboBox {
                border: 2px solid #dee2e6;
                border-radius: 5px;
                padding: 8px 15px;
                font-size: 12px;
                min-width: 150px;
            }
            QLineEdit {
                border: 2px solid #dee2e6;
                border-radius: 5px;
                padding: 8px 15px;
                font-size: 12px;
            }
            QLineEdit:focus {
                border: 2px solid #3498db;
            }
            QTabWidget::pane {
                background-color: white;
                border: 2px solid #3498db;
                border-radius: 8px;
            }
            QTabBar::tab {
                background-color: #e9ecef;
                color: #495057;
                border: none;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
                padding: 10px 20px;
                margin-right: 2px;
                font-size: 12px;
                font-weight: bold;
            }
            QTabBar::tab:selected {
                background-color: #3498db;
                color: white;
            }
            QTabBar::tab:hover {
                background-color: #5faee3;
                color: white;
            }
        """)
        
        self.setup_menu()
        self.setup_toolbar()
        self.setup_statusbar()
        self.setup_central()
        self.show_table("clients")
    
    def setup_menu(self):
        menubar = self.menuBar()
        
        ref_menu = menubar.addMenu("📋 СПРАВОЧНИКИ")
        
        clients = QAction("👥 Клиенты", self)
        clients.triggered.connect(lambda: self.show_table("clients"))
        ref_menu.addAction(clients)
        
        cars = QAction("🚗 Автомобили", self)
        cars.triggered.connect(lambda: self.show_table("cars"))
        ref_menu.addAction(cars)
        
        employees = QAction("👤 Сотрудники", self)
        employees.triggered.connect(lambda: self.show_table("employees"))
        ref_menu.addAction(employees)
        
        ref_menu.addSeparator()
        
        services = QAction("🔧 Услуги", self)
        services.triggered.connect(lambda: self.show_table("services"))
        ref_menu.addAction(services)
        
        parts = QAction("⚙️ Запчасти", self)
        parts.triggered.connect(lambda: self.show_table("parts"))
        ref_menu.addAction(parts)
        
        orders_menu = menubar.addMenu("📦 ЗАКАЗЫ")
        
        new_order = QAction("➕ Новый заказ", self)
        new_order.triggered.connect(self.new_order)
        orders_menu.addAction(new_order)
        
        orders_list = QAction("📋 Журнал заказов", self)
        orders_list.triggered.connect(lambda: self.show_table("orders"))
        orders_menu.addAction(orders_list)
        
        stock_menu = menubar.addMenu("🏭 СКЛАД")
        
        stock = QAction("📊 Остатки", self)
        stock.triggered.connect(self.show_stock)
        stock_menu.addAction(stock)
        
        movement = QAction("📈 Движение", self)
        movement.triggered.connect(self.show_movement)
        stock_menu.addAction(movement)
        
        reports_menu = menubar.addMenu("📊 ОТЧЕТЫ")
        
        revenue = QAction("💰 Выручка", self)
        revenue.triggered.connect(self.revenue_report)
        reports_menu.addAction(revenue)
        
        services_report = QAction("🔧 Услуги", self)
        services_report.triggered.connect(self.services_report)
        reports_menu.addAction(services_report)
        
        if self.user_data['role'] == 'admin':
            admin_menu = menubar.addMenu("⚙️ АДМИНИСТРИРОВАНИЕ")
            
            users = QAction("👥 Пользователи", self)
            users.triggered.connect(self.manage_users)
            admin_menu.addAction(users)
        
        service_menu = menubar.addMenu("🔧 СЕРВИС")
        
        change_pass = QAction("🔄 Сменить пароль", self)
        change_pass.triggered.connect(self.change_password)
        service_menu.addAction(change_pass)
        
        service_menu.addSeparator()
        
        logout = QAction("🚪 Выход", self)
        logout.triggered.connect(self.logout)
        service_menu.addAction(logout)
        
        exit_action = QAction("✖ Завершение работы", self)
        exit_action.triggered.connect(lambda: sys.exit())
        service_menu.addAction(exit_action)
    
    def setup_toolbar(self):
        toolbar = self.addToolBar("Панель инструментов")
        toolbar.setMovable(False)
        
        add_client = QAction("➕ НОВЫЙ КЛИЕНТ", self)
        add_client.triggered.connect(lambda: self.add_record("clients"))
        toolbar.addAction(add_client)
        
        add_car = QAction("➕ НОВЫЙ АВТО", self)
        add_car.triggered.connect(lambda: self.add_record("cars"))
        toolbar.addAction(add_car)
        
        add_order = QAction("➕ НОВЫЙ ЗАКАЗ", self)
        add_order.triggered.connect(self.new_order)
        toolbar.addAction(add_order)
        
        toolbar.addSeparator()
        
        refresh = QAction("🔄 ОБНОВИТЬ", self)
        refresh.triggered.connect(lambda: self.show_table(self.current_table))
        toolbar.addAction(refresh)
        
        toolbar.addSeparator()
        
        logout_btn = QAction("🚪 ВЫЙТИ", self)
        logout_btn.triggered.connect(self.logout)
        toolbar.addAction(logout_btn)
    
    def setup_statusbar(self):
        status = self.statusBar()
        
        user_label = QLabel(f"👤 {self.user_data['full_name']} | Роль: {'Администратор' if self.user_data['role'] == 'admin' else 'Менеджер'}")
        status.addPermanentWidget(user_label)
        
        self.time_label = QLabel()
        self.update_time()
        status.addPermanentWidget(self.time_label)
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)
    
    def update_time(self):
        self.time_label.setText(f"📅 {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}")
    
    def setup_central(self):
        central = QWidget()
        self.setCentralWidget(central)
        
        layout = QVBoxLayout(central)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        self.title = QLabel("📋 СПРАВОЧНИК: КЛИЕНТЫ")
        self.title.setStyleSheet("""
            font-size: 22px;
            font-weight: bold;
            color: #2c3e50;
            background: white;
            padding: 15px;
            border-radius: 8px;
            border-left: 5px solid #3498db;
        """)
        layout.addWidget(self.title)
        
        self.table = QTableWidget()
        self.table.setAlternatingRowColors(True)
        self.table.setSortingEnabled(True)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        layout.addWidget(self.table)
        
        panel = QWidget()
        panel.setStyleSheet("background-color: white; border-radius: 8px; padding: 10px;")
        panel_layout = QHBoxLayout(panel)
        panel_layout.setSpacing(5)  
        
        self.add_btn = QPushButton("➕ ДОБАВИТЬ")
        self.add_btn.setObjectName("addBtn")
        self.add_btn.setFixedHeight(40)
        self.add_btn.setFixedWidth(120)
        self.add_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 15px;
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #229954;
            }
        """)
        self.add_btn.clicked.connect(lambda: self.add_record(self.current_table))
        panel_layout.addWidget(self.add_btn)
        
        self.edit_btn = QPushButton("✏️ РЕДАКТИРОВАТЬ")
        self.edit_btn.setFixedHeight(40)
        self.edit_btn.setFixedWidth(140)
        self.edit_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 15px;
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        self.edit_btn.clicked.connect(self.edit_record)
        panel_layout.addWidget(self.edit_btn)
        
        self.delete_btn = QPushButton("🗑️ УДАЛИТЬ")
        self.delete_btn.setObjectName("deleteBtn")
        self.delete_btn.setFixedHeight(40)
        self.delete_btn.setFixedWidth(120)
        self.delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 15px;
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        self.delete_btn.clicked.connect(self.delete_record)
        panel_layout.addWidget(self.delete_btn)
        
        panel_layout.addStretch()
        
        layout.addWidget(panel)
    
    def show_table(self, table_name):
        self.current_table = table_name
        
        titles = {
            "clients": "КЛИЕНТЫ",
            "cars": "АВТОМОБИЛИ",
            "employees": "СОТРУДНИКИ",
            "services": "УСЛУГИ",
            "parts": "ЗАПЧАСТИ",
            "orders": "ЗАКАЗЫ"
        }
        self.title.setText(f"📋 СПРАВОЧНИК: {titles.get(table_name, '')}")
        
        if table_name == "clients":
            data = self.db.fetch_all("SELECT id, last_name, first_name, middle_name, phone, email, address FROM clients")
            headers = ["ID", "Фамилия", "Имя", "Отчество", "Телефон", "Email", "Адрес"]
        elif table_name == "cars":
            data = self.db.fetch_all('''
                SELECT cars.id, cars.brand, cars.model, cars.license_plate, cars.vin,
                       clients.last_name || ' ' || clients.first_name, cars.color, cars.mileage
                FROM cars LEFT JOIN clients ON cars.client_id = clients.id
            ''')
            headers = ["ID", "Марка", "Модель", "Госномер", "VIN", "Владелец", "Цвет", "Пробег"]
        elif table_name == "employees":
            data = self.db.fetch_all("SELECT id, last_name, first_name, middle_name, position, phone, email FROM employees")
            headers = ["ID", "Фамилия", "Имя", "Отчество", "Должность", "Телефон", "Email"]
        elif table_name == "services":
            data = self.db.fetch_all("SELECT id, code, name, price, duration, category FROM services")
            headers = ["ID", "Код", "Услуга", "Цена", "Мин", "Категория"]
        elif table_name == "parts":
            data = self.db.fetch_all("SELECT id, code, name, price, quantity, min_quantity, supplier FROM parts")
            headers = ["ID", "Код", "Запчасть", "Цена", "Кол-во", "Мин", "Поставщик"]
        elif table_name == "orders":
            data = self.db.fetch_all('''
                SELECT orders.id, orders.order_number, clients.last_name,
                       orders.total_cost, orders.status, orders.payment_status,
                       orders.created_date
                FROM orders LEFT JOIN clients ON orders.client_id = clients.id
                ORDER BY orders.id DESC
            ''')
            headers = ["ID", "Номер", "Клиент", "Сумма", "Статус", "Оплата", "Дата"]
        else:
            return
        
        self.table.setRowCount(len(data))
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        
        for i, row in enumerate(data):
            for j, value in enumerate(row):
                item = QTableWidgetItem(str(value if value is not None else ""))
                if j == 0:
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                if table_name == "parts" and j == 4 and value < row[5]:
                    item.setBackground(QColor(255, 230, 230))
                self.table.setItem(i, j, item)
        
        self.table.resizeColumnsToContents()
        self.table.horizontalHeader().setStretchLastSection(True)
    
    def add_record(self, table_name):
        if table_name == "clients":
            dlg = ClientDialog(self.db)
        elif table_name == "cars":
            dlg = CarDialog(self.db)
        elif table_name == "employees":
            dlg = EmployeeDialog(self.db)
        elif table_name == "services":
            dlg = ServiceDialog(self.db)
        elif table_name == "parts":
            dlg = PartDialog(self.db)
        else:
            return
        
        if dlg.exec_():
            self.show_table(table_name)
    
    def edit_record(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Ошибка", "Выберите запись для редактирования")
            return
        
        record_id = int(self.table.item(row, 0).text())
        
        if self.current_table == "clients":
            dlg = ClientDialog(self.db, record_id)
        elif self.current_table == "cars":
            dlg = CarDialog(self.db, record_id)
        elif self.current_table == "employees":
            dlg = EmployeeDialog(self.db, record_id)
        elif self.current_table == "services":
            dlg = ServiceDialog(self.db, record_id)
        elif self.current_table == "parts":
            dlg = PartDialog(self.db, record_id)
        elif self.current_table == "orders":
            dlg = OrderDialog(self.db, record_id)
        else:
            return
        
        if dlg.exec_():
            self.show_table(self.current_table)
    
    def delete_record(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Ошибка", "Выберите запись для удаления")
            return
        
        record_id = int(self.table.item(row, 0).text())
        
        reply = QMessageBox.question(self, "Подтверждение", 
                                     "Вы уверены, что хотите удалить запись?",
                                     QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            try:
                self.db.execute_query(f"DELETE FROM {self.current_table} WHERE id = ?", (record_id,))
                self.show_table(self.current_table)
            except Exception as e:
                QMessageBox.warning(self, "Ошибка", f"Нельзя удалить запись: {str(e)}")
    
    def new_order(self):
        dlg = OrderDialog(self.db)
        if dlg.exec_():
            self.show_table("orders")
    
    def show_stock(self):
        data = self.db.fetch_all("SELECT code, name, quantity, min_quantity, price, supplier FROM parts ORDER BY name")
        
        dlg = QDialog(self)
        dlg.setWindowTitle("Остатки на складе")
        dlg.setGeometry(200, 200, 900, 600)
        dlg.setStyleSheet(self.styleSheet())
        
        layout = QVBoxLayout(dlg)
        layout.setContentsMargins(20, 20, 20, 20)
        
        title = QLabel("📊 ОСТАТКИ НА СКЛАДЕ")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #2c3e50; padding: 10px;")
        layout.addWidget(title)
        
        table = QTableWidget()
        table.setRowCount(len(data))
        table.setColumnCount(6)
        table.setHorizontalHeaderLabels(["Код", "Наименование", "Кол-во", "Мин", "Цена", "Поставщик"])
        table.setAlternatingRowColors(True)
        
        for i, row in enumerate(data):
            for j, val in enumerate(row):
                item = QTableWidgetItem(str(val))
                if j == 2 and val < row[3]:
                    item.setBackground(QColor(255, 230, 230))
                table.setItem(i, j, item)
        
        table.resizeColumnsToContents()
        layout.addWidget(table)
        
        btn = QPushButton("Закрыть")
        btn.setFixedWidth(150)
        btn.clicked.connect(dlg.accept)
        layout.addWidget(btn, alignment=Qt.AlignCenter)
        
        dlg.exec_()
    
    def show_movement(self):
        data = self.db.fetch_all('''
            SELECT parts_movement.date, parts.name, parts_movement.type, 
                   parts_movement.quantity, orders.order_number
            FROM parts_movement 
            JOIN parts ON parts_movement.part_id = parts.id
            LEFT JOIN orders ON parts_movement.order_id = orders.id
            ORDER BY parts_movement.date DESC LIMIT 100
        ''')
        
        dlg = QDialog(self)
        dlg.setWindowTitle("Движение товаров")
        dlg.setGeometry(200, 200, 900, 600)
        dlg.setStyleSheet(self.styleSheet())
        
        layout = QVBoxLayout(dlg)
        
        title = QLabel("📈 ДВИЖЕНИЕ ТОВАРОВ")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #2c3e50; padding: 10px;")
        layout.addWidget(title)
        
        table = QTableWidget()
        table.setRowCount(len(data))
        table.setColumnCount(5)
        table.setHorizontalHeaderLabels(["Дата", "Товар", "Тип", "Кол-во", "Заказ"])
        table.setAlternatingRowColors(True)
        
        for i, row in enumerate(data):
            for j, val in enumerate(row):
                item = QTableWidgetItem(str(val if val is not None else ""))
                table.setItem(i, j, item)
        
        table.resizeColumnsToContents()
        layout.addWidget(table)
        
        btn = QPushButton("Закрыть")
        btn.setFixedWidth(150)
        btn.clicked.connect(dlg.accept)
        layout.addWidget(btn, alignment=Qt.AlignCenter)
        
        dlg.exec_()
    
    def revenue_report(self):
        data = self.db.fetch_all('''
            SELECT date(orders.created_date), orders.order_number, 
                   clients.last_name || ' ' || clients.first_name,
                   orders.total_cost
            FROM orders 
            LEFT JOIN clients ON orders.client_id = clients.id
            WHERE orders.payment_status = 'оплачен'
            ORDER BY orders.created_date DESC
        ''')
        
        dlg = QDialog(self)
        dlg.setWindowTitle("Отчет по выручке")
        dlg.setGeometry(200, 200, 800, 600)
        dlg.setStyleSheet(self.styleSheet())
        
        layout = QVBoxLayout(dlg)
        
        title = QLabel("💰 ОТЧЕТ ПО ВЫРУЧКЕ")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #2c3e50; padding: 10px;")
        layout.addWidget(title)
        
        table = QTableWidget()
        table.setRowCount(len(data))
        table.setColumnCount(4)
        table.setHorizontalHeaderLabels(["Дата", "Номер", "Клиент", "Сумма"])
        table.setAlternatingRowColors(True)
        
        total = 0
        for i, row in enumerate(data):
            for j, val in enumerate(row):
                if j == 3:
                    item = QTableWidgetItem(f"{val:,.2f} ₽")
                    total += val
                else:
                    item = QTableWidgetItem(str(val))
                table.setItem(i, j, item)
        
        table.resizeColumnsToContents()
        layout.addWidget(table)
        
        total_label = QLabel(f"ИТОГО: {total:,.2f} ₽")
        total_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #2c3e50; padding: 10px;")
        layout.addWidget(total_label)
        
        btn = QPushButton("Закрыть")
        btn.setFixedWidth(150)
        btn.clicked.connect(dlg.accept)
        layout.addWidget(btn, alignment=Qt.AlignCenter)
        
        dlg.exec_()
    
    def services_report(self):
        data = self.db.fetch_all('''
            SELECT services.name, COUNT(*), SUM(order_services.price * order_services.quantity)
            FROM order_services
            JOIN services ON order_services.service_id = services.id
            GROUP BY services.id
            ORDER BY COUNT(*) DESC
        ''')
        
        dlg = QDialog(self)
        dlg.setWindowTitle("Отчет по услугам")
        dlg.setGeometry(200, 200, 700, 500)
        dlg.setStyleSheet(self.styleSheet())
        
        layout = QVBoxLayout(dlg)
        
        title = QLabel("🔧 ОТЧЕТ ПО УСЛУГАМ")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #2c3e50; padding: 10px;")
        layout.addWidget(title)
        
        table = QTableWidget()
        table.setRowCount(len(data))
        table.setColumnCount(3)
        table.setHorizontalHeaderLabels(["Услуга", "Кол-во", "Сумма"])
        table.setAlternatingRowColors(True)
        
        for i, row in enumerate(data):
            table.setItem(i, 0, QTableWidgetItem(row[0]))
            table.setItem(i, 1, QTableWidgetItem(str(row[1])))
            table.setItem(i, 2, QTableWidgetItem(f"{row[2]:,.2f} ₽"))
        
        table.resizeColumnsToContents()
        layout.addWidget(table)
        
        btn = QPushButton("Закрыть")
        btn.setFixedWidth(150)
        btn.clicked.connect(dlg.accept)
        layout.addWidget(btn, alignment=Qt.AlignCenter)
        
        dlg.exec_()
    
    def manage_users(self):
        from auth_dialogs import ChangePasswordDialog
        
        dlg = QDialog(self)
        dlg.setWindowTitle("Управление пользователями")
        dlg.setGeometry(200, 200, 700, 500)
        dlg.setStyleSheet(self.styleSheet())
        
        layout = QVBoxLayout(dlg)
        layout.setContentsMargins(20, 20, 20, 20)
        
        title = QLabel("👥 УПРАВЛЕНИЕ ПОЛЬЗОВАТЕЛЯМИ")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #2c3e50; padding: 10px;")
        layout.addWidget(title)
        
        table = QTableWidget()
        table.setColumnCount(4)
        table.setHorizontalHeaderLabels(["ID", "Логин", "Роль", "ФИО"])
        table.setAlternatingRowColors(True)
        
        users = self.db.fetch_all("SELECT id, username, role, full_name FROM users")
        table.setRowCount(len(users))
        
        for i, user in enumerate(users):
            for j, val in enumerate(user):
                item = QTableWidgetItem(str(val if val is not None else ""))
                table.setItem(i, j, item)
        
        table.resizeColumnsToContents()
        layout.addWidget(table)
        
        btn_layout = QHBoxLayout()
        
        add_btn = QPushButton("➕ ДОБАВИТЬ ПОЛЬЗОВАТЕЛЯ")
        add_btn.setObjectName("addBtn")
        add_btn.clicked.connect(lambda: self.add_user(table))
        btn_layout.addWidget(add_btn)
        
        edit_btn = QPushButton("✏️ РЕДАКТИРОВАТЬ")
        edit_btn.clicked.connect(lambda: self.edit_user(table))
        btn_layout.addWidget(edit_btn)
        
        delete_btn = QPushButton("🗑️ УДАЛИТЬ")
        delete_btn.setObjectName("deleteBtn")
        delete_btn.clicked.connect(lambda: self.delete_user(table))
        btn_layout.addWidget(delete_btn)
        
        layout.addLayout(btn_layout)
        
        close_btn = QPushButton("ЗАКРЫТЬ")
        close_btn.setFixedWidth(150)
        close_btn.clicked.connect(dlg.accept)
        layout.addWidget(close_btn, alignment=Qt.AlignCenter)
        
        dlg.exec_()
    
    def add_user(self, table):
        from dialogs.register_dialog import RegisterDialog
        dlg = RegisterDialog(self.db)
        if dlg.exec_():
            self.refresh_users_table(table)
    
    def edit_user(self, table):
        row = table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Ошибка", "Выберите пользователя")
            return
        
        user_id = int(table.item(row, 0).text())
        username = table.item(row, 1).text()
        role = table.item(row, 2).text()
        full_name = table.item(row, 3).text()
        
        dlg = QDialog(self)
        dlg.setWindowTitle("Редактирование пользователя")
        dlg.setFixedSize(400, 450)
        dlg.setStyleSheet(self.styleSheet())
        
        layout = QVBoxLayout(dlg)
        layout.setSpacing(15)
        layout.setContentsMargins(30, 30, 30, 30)
        
        title = QLabel("✏️ РЕДАКТИРОВАНИЕ ПОЛЬЗОВАТЕЛЯ")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #3498db; margin-bottom: 10px;")
        layout.addWidget(title)
        
        form = QFormLayout()
        form.setSpacing(15)
        form.setLabelAlignment(Qt.AlignRight)
        
        full_name_edit = QLineEdit()
        full_name_edit.setText(full_name)
        full_name_edit.setPlaceholderText("Иванов Иван Иванович")
        form.addRow("ФИО:*", full_name_edit)
        
        username_edit = QLineEdit()
        username_edit.setText(username)
        username_edit.setEnabled(False)
        form.addRow("Логин:", username_edit)
        
        role_combo = QComboBox()
        role_combo.addItems(["manager", "admin"])
        role_combo.setCurrentText(role)
        form.addRow("Роль:", role_combo)
        
        password = QLineEdit()
        password.setEchoMode(QLineEdit.Password)
        password.setPlaceholderText("Оставьте пустым, если не меняете")
        form.addRow("Новый пароль:", password)
        
        layout.addLayout(form)
        
        info = QLabel("Оставьте пароль пустым, если не хотите его менять")
        info.setStyleSheet("color: #6c757d; font-size: 10px;")
        info.setAlignment(Qt.AlignCenter)
        layout.addWidget(info)
        
        layout.addStretch()
        
        btn_layout = QHBoxLayout()
        
        save_btn = QPushButton("✅ СОХРАНИТЬ")
        save_btn.clicked.connect(lambda: self.save_user_edit(dlg, user_id, full_name_edit.text(), role_combo.currentText(), password.text()))
        btn_layout.addWidget(save_btn)
        
        cancel_btn = QPushButton("✖ ОТМЕНА")
        cancel_btn.setStyleSheet("background-color: #e74c3c; color: white;")
        cancel_btn.clicked.connect(dlg.reject)
        btn_layout.addWidget(cancel_btn)
        
        layout.addLayout(btn_layout)
        dlg.exec_()
    
    def save_user_edit(self, dlg, user_id, full_name, role, password):
        if not full_name:
            QMessageBox.warning(dlg, "Ошибка", "Введите ФИО")
            return
        
        if password:
            hashed = PasswordHasher.hash_password(password)
            self.db.execute_query('''
                UPDATE users SET full_name = ?, role = ?, password = ? WHERE id = ?
            ''', (full_name, role, hashed, user_id))
        else:
            self.db.execute_query('''
                UPDATE users SET full_name = ?, role = ? WHERE id = ?
            ''', (full_name, role, user_id))
        
        dlg.accept()
    
    def delete_user(self, table):
        row = table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Ошибка", "Выберите пользователя")
            return
        
        user_id = int(table.item(row, 0).text())
        username = table.item(row, 1).text()
        
        if username == 'admin':
            QMessageBox.warning(self, "Ошибка", "Нельзя удалить администратора")
            return
        
        reply = QMessageBox.question(self, "Подтверждение", 
                                     f"Удалить пользователя {username}?",
                                     QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            self.db.execute_query("DELETE FROM users WHERE id = ?", (user_id,))
            self.refresh_users_table(table)
    
    def refresh_users_table(self, table):
        users = self.db.fetch_all("SELECT id, username, role, full_name FROM users")
        table.setRowCount(len(users))
        for i, user in enumerate(users):
            for j, val in enumerate(user):
                table.setItem(i, j, QTableWidgetItem(str(val if val is not None else "")))
        table.resizeColumnsToContents()
    
    def change_password(self):
        from auth_dialogs import ChangePasswordDialog
        dlg = ChangePasswordDialog(self.db)
        dlg.exec_()
    
    def logout(self):
        reply = QMessageBox.question(self, "Выход", "Вы уверены, что хотите выйти?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.close()