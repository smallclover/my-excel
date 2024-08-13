import sys
from PyQt6 import QtWidgets
from ui_cls.my_excel_main_window_cls import MyExcelMainWindow

if __name__ == "__main__":
    try:
        app = QtWidgets.QApplication(sys.argv)
        window = MyExcelMainWindow()
        window.show()
        sys.exit(app.exec())
    except Exception as e:
        print(e)
