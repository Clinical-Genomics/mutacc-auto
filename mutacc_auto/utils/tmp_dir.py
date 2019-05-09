import tempfile
import shutil

class TemporaryDirectory():
    """Context manager for tempfile.mkdtemp() so it's usable with "with" statement."""

    def __init__(self, directory, delete_dir=False):

        self.delete_dir = delete_dir
        self.directory = directory

    def __enter__(self):
        self.name = tempfile.mkdtemp(dir=self.directory)
        return self.name

    def __exit__(self, exc_type, exc_value, traceback):
        if self.delete_dir:
            shutil.rmtree(self.name)
