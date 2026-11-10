import logging
import sys
from pathlib import Path

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

from .main_window import MainWindow

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(name)s: %(message)s',
    datefmt='%H:%M:%S',
)

def main():
    app = QApplication(sys.argv)

    if hasattr(sys, '_MEIPASS'):
        icon_path = Path(sys._MEIPASS) / 'app.ico'
    else:
        icon_path = Path(__file__).resolve().parents[3] / 'app.ico'
    app.setWindowIcon(QIcon(str(icon_path)))

    window = MainWindow()
    window.setWindowIcon(QIcon(str(icon_path)))
    window.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
