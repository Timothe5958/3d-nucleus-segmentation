import logging

from .output.saver import OutputSaver
from .processing import processing_pipeline

logger = logging.getLogger(__name__)


def process_observations(
    observations,
    processing_options,
    output_config,
    progress_callback,
    save_dispatcher,
):

    for observation in observations:
        logger.info('Processing %s...', observation.path.name)

        # Compute the results in the second thread (current one)
        pipeline_results = processing_pipeline.process_observation(
            observation,
            processing_options,
            progress_callback,
        )

        output_manager = OutputSaver(
            observation,
            pipeline_results,
            output_config,
        )

        # Save pipeline 3d view screenshots in the main thread (Napari viewer requirement)
        save_dispatcher(
            output_manager.save_outputs,
            progress_callback=progress_callback,
        )

        progress_callback(
            'observation_done',
            observation.path.name,
            '',
        )
