from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QCheckBox,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from ...output_options import OUTPUT_OPTIONS


class OutputSelectionPage(QWidget):
    back_requested = Signal()
    run_requested = Signal()

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        layout.addWidget(QLabel('Sélection des plots'))

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        content = QWidget()
        content_layout = QVBoxLayout(content)

        self.output_checkboxes = {}

        # Add the checkboxes (splitted in different sections)
        for section_name, option_names in OUTPUT_OPTIONS.items():
            group = QGroupBox(section_name)
            group_layout = QVBoxLayout()

            self.output_checkboxes[section_name] = {}

            for name in option_names:
                checkbox = QCheckBox(name.replace('_', ' ').capitalize())
                group_layout.addWidget(checkbox)

                self.output_checkboxes[section_name][name] = checkbox

            group.setLayout(group_layout)
            content_layout.addWidget(group)

        content_layout.addStretch()

        scroll_area.setWidget(content)
        layout.addWidget(scroll_area)

        # Add navigation buttons
        self.back_button = QPushButton('Retour')
        self.back_button.clicked.connect(self.back_requested.emit)

        self.run_button = QPushButton('Lancer')
        self.run_button.clicked.connect(self.run_requested.emit)

        navigation_layout = QHBoxLayout()
        navigation_layout.addWidget(self.back_button)
        navigation_layout.addWidget(self.run_button)

        layout.addLayout(navigation_layout)

        self.setLayout(layout)


    def get_output_options(self):
        return {
            section: {
                name: checkbox.isChecked()
                for name, checkbox in checkboxes.items()
            }
            for section, checkboxes in self.output_checkboxes.items()
        }
