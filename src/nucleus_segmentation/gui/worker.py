import threading
import traceback

from PySide6.QtCore import QThread, Signal

from ..processing.pipeline import process_observations


class ProcessingWorker(QThread):
    progress_event = Signal(str, str, str)
    processing_finished = Signal()
    processing_failed = Signal(str, str)
    save_requested = Signal(object)

    def __init__(
        self,
        observations,
        processing_options,
        output_options,
        output_folder,
        log=True,
    ):
        super().__init__()

        self.observations = observations
        self.processing_options = processing_options
        self.output_options = output_options
        self.output_folder = output_folder
        self.log = log

    def run(self):
        try:
            process_observations(
                self.observations,
                self.processing_options,
                self.output_options,
                self.output_folder,
                log=self.log,
                progress_callback=self.progress_event.emit,
                save_dispatcher=self.run_on_gui_thread,
            )
        except Exception as error:
            traceback_text = traceback.format_exc()
            print(traceback_text, flush=True)

            self.processing_failed.emit(
                str(error),
                traceback_text,
            )
        else:
            self.processing_finished.emit()

    def run_on_gui_thread(self, function, *args, **kwargs):
        request = {
            'function': function,
            'args': args,
            'kwargs': kwargs,
            'event': threading.Event(),
            'error': None,
        }

        self.save_requested.emit(request)
        request['event'].wait()

        if request['error'] is not None:
            raise request['error']
