import subprocess
from os import listdir
from os.path import isfile, join

designer_folder = '../ui/designer/'
compiled_folder = '../ui/compiled/'
uic_path = '../venv/Scripts/pyside6-uic.exe'


def is_ui(filename):
    return filename.endswith('ui')


if __name__ == '__main__':
    files = [file for file in listdir(designer_folder) if isfile(join(designer_folder, file)) and is_ui(file)]
    for file in files:
        subprocess.run(args=[uic_path, join(designer_folder, file), '-o',join(compiled_folder, file[:-3] + '.py')],
                       stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE)
