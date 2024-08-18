import sys
from PyQt5.QtWidgets import QApplication
from main_window import MainWindow
import style

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    style.update_theme(app)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())