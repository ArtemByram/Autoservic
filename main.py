import sys
from PyQt5.QtWidgets import QApplication, QDialog
from database import Database
from auth_dialogs import LoginDialog
from main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    db = Database()
    
    while True:
        login = LoginDialog(db)
        if login.exec_() == QDialog.Accepted:
            window = MainWindow(db, login.user_data)
            window.show()
            app.exec_()
        else:
            break
    
    sys.exit()

if __name__ == '__main__':
    main()