import os
import tempfile


class File:

    new_file_count = 0

    def __init__(self, path):
        self.current_position = 0
        self.path = path
        if not os.path.exists(path):
            open(path, 'w').close()

    def read(self):
        with open(self.path, 'r') as f:
            return f.read()

    def write(self, new_text):
        with open(self.path, 'w') as f:
            f.write(new_text)

    def __str__(self):
        return os.path.abspath(self.path)

    def __add__(self, other):
        File.new_file_count += 1
        new_path = os.path.join(tempfile.gettempdir(),
                                'new_file_{}.txt'.format(File.new_file_count))
        new_obj = File(new_path)
        new_obj.write(self.read() + other.read())
        return new_obj

    def __iter__(self):
        return self

    def __next__(self):
        with open(self.path, 'r') as f:
            f.seek(self.current_position)
            next_line = f.readline()
            if not next_line:
                self.current_position = 0
                raise StopIteration
            self.current_position = f.tell()
        return next_line
