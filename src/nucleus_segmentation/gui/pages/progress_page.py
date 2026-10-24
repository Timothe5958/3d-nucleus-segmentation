from PySide6.QtWidgets import (
    QLabel,
    QProgressBar,
    QVBoxLayout,
    QWidget,
)


class ProgressPage(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Processing')
        self.resize(500, 250)

        # Global progress
        self.global_label = QLabel(
            'Observation(s) processed : 0/0'
        )

        self.global_progress_bar = QProgressBar()
        self.global_progress_bar.setRange(0, 1)
        self.global_progress_bar.setValue(0)

        # Current observation
        self.observation_label = QLabel(
           'Current step : 0/0'
        )

        self.observation_progress_bar = QProgressBar()
        self.observation_progress_bar.setRange(0, 1)
        self.observation_progress_bar.setValue(0)

        # Current processing step
        self.step_label = QLabel('')

        # last observation duration
        self.last_observation_duration = QLabel('')

        # Layout
        layout = QVBoxLayout()

        layout.addWidget(self.global_label)
        layout.addWidget(self.global_progress_bar)
        layout.addSpacing(15)
        layout.addWidget(self.observation_label)
        layout.addWidget(self.observation_progress_bar)
        layout.addWidget(self.step_label)
        layout.addWidget(self.last_observation_duration)

        self.setLayout(layout)


    def initial_update(self, total_observations, total_steps):
        self.total_observations = total_observations
        self.total_steps = total_steps

        self.global_progress_bar.setRange(
            0, max(1, total_observations)
        )
        self.observation_progress_bar.setRange(
            0, max(1, total_steps)
        )

        self.update_global_progress(0)
        self.update_observation_progress(0, '...', '...')
        self.step_label.setText('Processing preparation...')


    def update_global_progress(self, completed_observations):
        self.global_progress_bar.setValue(
            completed_observations
        )

        self.global_label.setText(
            f'Observation(s) processed : {completed_observations}/{self.total_observations}'
        )

    def update_observation_progress(self, curr_step_id, current_obs_name, current_step_name):
        self.observation_progress_bar.setValue(curr_step_id)

        self.observation_label.setText(
            f'Observation in process : {current_obs_name}'
        )

        self.step_label.setText(
            f'{current_step_name} - {current_obs_name}'
        )

    def finish(self):
        self.global_progress_bar.setValue(
            self.total_observations
        )
        self.global_label.setText(
            f'Processing done : '
            f'{self.total_observations}/'
            f'{self.total_observations} observations'
        )

        self.observation_progress_bar.setValue(self.total_steps)
        self.observation_progress_bar.setFormat('Done — 100 %')
        self.step_label.setText('Processing done')
