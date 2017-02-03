"""jobarchitect package."""

__version__ = "0.1.0"


class JobSpec(object):
    """Job specification class."""

    def __init__(self, program_template, dataset_path,
                 output_root, hash_ids, docker_image_name=None):
        self.program_template = program_template
        self.dataset_path = dataset_path
        self.output_root = output_root
        self.hash_ids = hash_ids
        if docker_image_name is not None:
            self.docker_image_name = docker_image_name
