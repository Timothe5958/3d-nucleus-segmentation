from pathlib import Path

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QCheckBox,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from ...observation import ObservationsList


class ObservationSelectionPage(QWidget):
    next_requested = Signal()

    def __init__(self):
        super().__init__()

        # Folder selection
        self.folder_label = QLabel('No folder selected')

        self.select_folder_button = QPushButton('Select a folder')
        self.select_folder_button.clicked.connect(self.select_folder)

        # List of the observations
        self.observations = []
        self.observation_checkboxes = []

        self.observations_label = QLabel('Observation(s) found :')
        self.observations_list = QListWidget()

        self.select_all_button = QPushButton('Select all')
        self.select_all_button.clicked.connect(self.select_all_observations)

        self.deselect_all_button = QPushButton('Deselect all')
        self.deselect_all_button.clicked.connect(self.deselect_all_observations)

        # next page button
        self.next_button = QPushButton('Next')
        self.next_button.clicked.connect(
            self.next_requested.emit
        )

        selection_buttons_layout = QHBoxLayout()
        selection_buttons_layout.addWidget(self.select_all_button)
        selection_buttons_layout.addWidget(self.deselect_all_button)

        # create the layout that will be displayed
        layout = QVBoxLayout()

        layout.addWidget(self.folder_label)
        layout.addWidget(self.select_folder_button)
        layout.addWidget(self.observations_label)
        layout.addWidget(self.observations_list)
        layout.addLayout(selection_buttons_layout)
        layout.addWidget(self.next_button)

        self.setLayout(layout)


    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(
            self,
            'Select the folder containing the data',
        )

        if not folder:
            return

        self.folder_label.setText(folder)
        self.load_observations(folder)
        self.selected_folder = Path(folder)


    def load_observations(self, folder):
        self.observations_list.clear()
        self.observation_checkboxes.clear()

        self.observations = ObservationsList(folder)

        for observation in self.observations:
            checkbox = QCheckBox(observation.path.name)

            self.observation_checkboxes.append(checkbox)
            self.observations_list.addItem('')

            item = self.observations_list.item(
                self.observations_list.count() - 1
            )

            self.observations_list.setItemWidget(
                item,
                checkbox,
            )


    def select_all_observations(self):
        for checkbox in self.observation_checkboxes:
            checkbox.setChecked(True)


    def deselect_all_observations(self):
        for checkbox in self.observation_checkboxes:
            checkbox.setChecked(False)


    def get_selected_observations(self):
        return [
            observation
            for observation, checkbox in zip(
                self.observations,
                self.observation_checkboxes,
                strict=True,
            )
            if checkbox.isChecked()
        ]
