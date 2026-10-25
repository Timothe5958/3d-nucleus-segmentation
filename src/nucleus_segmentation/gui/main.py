import sys
from pathlib import Path

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

from ..metadata_saver import MetadataCollector
from .main_window import MainWindow

metadata = MetadataCollector()


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
