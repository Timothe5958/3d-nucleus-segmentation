import time

from PySide6.QtWidgets import (
    QMessageBox,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from ..processing.pipeline import ProcessingOptions
from ..utils import format_elapsed_time
from .pages import ObservationSelectionPage, OutputSelectionPage, ProgressPage
from .worker import ProcessingWorker


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('3D Nucleus Segmentation')
        self.resize(700, 400)

        self.observation_page = ObservationSelectionPage()
        self.output_page = OutputSelectionPage()
        self.progress_page = ProgressPage()

        # Stack the pages in the main window.
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.addWidget(self.observation_page)
        self.stacked_widget.addWidget(self.output_page)
        self.stacked_widget.addWidget(self.progress_page)

        layout = QVBoxLayout()
        layout.addWidget(self.stacked_widget)
        self.setLayout(layout)

        # Navigation between pages (signals)
        self.observation_page.next_requested.connect(
            self.go_to_output_page
        )
        self.output_page.back_requested.connect(
            self.go_to_observation_page
        )
        self.output_page.run_requested.connect(
            self.run_processing
        )

        # information on the pipeline progress
        self.worker = None
        self.completed_observations = 0
        self.completed_steps = 0
        self.current_observation_name = None

        # timer for observation
        self.start_observation = None


    def go_to_output_page(self):
        if not self.observation_page.get_selected_observations():
            return

        self.stacked_widget.setCurrentWidget(
            self.output_page
        )


    def go_to_observation_page(self):
        self.stacked_widget.setCurrentWidget(
            self.observation_page
        )


    def go_to_progress_page(self):
        self.stacked_widget.setCurrentWidget(
            self.progress_page
        )


    def run_processing(self):
        selected_observations = self.observation_page.get_selected_observations()
        output_options = self.output_page.get_output_options()

        processing_options = ProcessingOptions()

        output_folder = (
            self.observation_page.selected_folder.parent / 'nucleus_segmentation_output'
        )

        # number of steps for each observation
        # (number of steps in the pipeline + number of output figures)
        nb_steps = sum(
            sum(section.values())
            for section in output_options.values()
        ) + len(output_options['Pipeline (Expert only)'])

        self.progress_page.initial_update(len(selected_observations), nb_steps)
        self.go_to_progress_page()

        self.worker = ProcessingWorker(
            selected_observations,
            processing_options,
            output_options,
            output_folder,
            log=True,
        )

        self.worker.progress_event.connect(
            self.handle_progress_event
        )
        self.worker.processing_finished.connect(
            self.handle_processing_finished
        )
        self.worker.processing_failed.connect(
            self.handle_processing_failed
        )
        self.worker.finished.connect(
            self.worker.deleteLater
        )
        self.worker.save_requested.connect(
            self.execute_gui_request
        )

        self.worker.start()

    def handle_progress_event(
        self,
        event_type,
        observation_name,
        step_name,
    ):
        if event_type == 'step':
            # Réinitialiser le compteur au début de chaque observation.
            if observation_name != self.current_observation_name:
                self.start_observation = time.time()

                self.current_observation_name = observation_name
                self.curr_step_id = 0

            self.curr_step_id += 1

            self.progress_page.update_observation_progress(
                self.curr_step_id,
                observation_name,
                step_name,
            )

        elif event_type == 'observation_done':
            # La barre globale avance uniquement à la fin
            # de chaque observation.
            self.completed_observations += 1

            self.progress_page.update_global_progress(
                self.completed_observations
            )

            duration = format_elapsed_time(self.start_observation)
            self.progress_page.last_observation_duration.setText(
                f'Computation time for {self.current_observation_name} : {duration}'
            )

            self.current_observation_name = None

    def handle_processing_finished(self):
        self.progress_page.finish()

    def handle_processing_failed(self, error_message):
        self.progress_page.step_label.setText(
            f'Error during the processing : {error_message}'
        )

        QMessageBox.critical(
            self,
            'Error of processing',
            error_message,
        )

    def execute_gui_request(self, request):
        try:
            request['function'](
                *request['args'],
                **request['kwargs'],
            )
        except Exception as error:
            request['error'] = error
        finally:
            request['event'].set()
