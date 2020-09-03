import os
import shutil
from pathlib import Path

def copy_all_files(root_dir: str, output_dir: str, file_type: str='png') -> None:
    path_generator = Path(root_dir).rglob(f'*.{file_type}')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    for file in path_generator:
        output_file_path = output_dir+'/'+file.name
        print(f'Copying {file} to {output_file_path}')
        shutil.copy(file, output_file_path)

