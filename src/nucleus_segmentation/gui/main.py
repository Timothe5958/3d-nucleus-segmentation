import sys
from pathlib import Path

from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from ..observation import ObservationsList
from ..output import OutputOptions
from ..pipeline import ProcessingOptions, process_observations


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('3D Nucleus Segmentation')
        self.resize(700, 400)

        self.stacked_widget = QStackedWidget()

        self.create_observation_page()
        self.create_output_page()

        self.stacked_widget.addWidget(self.observation_page)
        self.stacked_widget.addWidget(self.output_page)

        layout = QVBoxLayout()
        layout.addWidget(self.stacked_widget)
        self.setLayout(layout)


    def create_observation_page(self):
        self.observation_page = QWidget()

        # Folder selection
        self.folder_label = QLabel('Aucun dossier sélectionné')

        self.select_folder_button = QPushButton('Choisir un dossier')
        self.select_folder_button.clicked.connect(self.select_folder)

        # List of the observations
        self.observations = []
        self.observation_checkboxes = []

        self.observations_label = QLabel('Observations trouvées :')
        self.observations_list = QListWidget()

        self.select_all_button = QPushButton('Tout sélectionner')
        self.select_all_button.clicked.connect(self.select_all_observations)

        self.deselect_all_button = QPushButton('Tout désélectionner')
        self.deselect_all_button.clicked.connect(self.deselect_all_observations)

        # next page button
        self.next_button = QPushButton('Suivant')
        self.next_button.clicked.connect(self.go_to_output_page)

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

        self.observation_page.setLayout(layout)


    def create_output_page(self):
        self.output_page = QWidget()

        title = QLabel('Sélection des plots')

        self.output_checkboxes = {
            'raw': QCheckBox('Raw'),
            'resampled': QCheckBox('Resampled'),
            'denoised': QCheckBox('Denoised'),
            'cropped': QCheckBox('Cropped'),
            'normalized': QCheckBox('Normalized'),
            'segmented': QCheckBox('Segmented'),
            'segmented_clean': QCheckBox('Cleaned segmentation'),
            'labelled': QCheckBox('Labelled'),
        }

        self.back_button = QPushButton('Retour')
        self.back_button.clicked.connect(
            self.go_to_observation_page
        )

        self.run_button = QPushButton('Lancer')
        self.run_button.clicked.connect(
            self.run_processing
        )

        navigation_layout = QHBoxLayout()
        navigation_layout.addWidget(self.back_button)
        navigation_layout.addWidget(self.run_button)

        layout = QVBoxLayout()

        layout.addWidget(title)

        for checkbox in self.output_checkboxes.values():
            layout.addWidget(checkbox)

        layout.addStretch()
        layout.addLayout(navigation_layout)

        self.output_page.setLayout(layout)


    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(
            self,
            'Sélectionner le dossier contenant les données',
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


    def go_to_output_page(self):
        selected_observations = self.get_selected_observations()

        if not selected_observations:
            return

        self.stacked_widget.setCurrentWidget(
            self.output_page
        )


    def go_to_observation_page(self):
        self.stacked_widget.setCurrentWidget(
            self.observation_page
        )


    def get_output_options(self):
        return OutputOptions(
            save_raw=self.output_checkboxes['raw'].isChecked(),
            save_resampled=self.output_checkboxes['resampled'].isChecked(),
            save_denoised=self.output_checkboxes['denoised'].isChecked(),
            save_cropped=self.output_checkboxes['cropped'].isChecked(),
            save_normalized=self.output_checkboxes['normalized'].isChecked(),
            save_segmented=self.output_checkboxes['segmented'].isChecked(),
            save_segmented_clean=self.output_checkboxes['segmented_clean'].isChecked(),
            save_labelled=self.output_checkboxes['labelled'].isChecked(),
        )


    def run_processing(self):
        selected_observations = self.get_selected_observations()
        output_options = self.get_output_options()

        processing_options = ProcessingOptions()

        output_folder = (
            self.selected_folder.parent / 'nucleus_segmentation_output'
        )

        process_observations(
            selected_observations,
            processing_options,
            output_options,
            output_folder,
            log=True,
            reduction=6,
        )


def main():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
