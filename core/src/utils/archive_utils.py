import os
import py7zr
import multivolumefile
from utils.env_utils import read_env_var


def compress_to_archive(data_dir: str, output_volume_dir: str, volume_size_MB: int = 5) -> str:
    os.makedirs(output_volume_dir)
    volume_base_name = os.path.basename(output_volume_dir)
    output_archive_path = os.path.join(output_volume_dir, volume_base_name)
    with multivolumefile.open(
        output_archive_path,
        mode='wb',
        volume=(volume_size_MB * 1024 * 1024)
    ) as target_archive:
        with py7zr.SevenZipFile(target_archive, 'w') as archive:
            archive.writeall(data_dir, 'dataset')
    return output_volume_dir


def extract_archive(volume_dir: str, output_dir: str, output_name: str = 'extracted') -> str:
    output_path = os.path.join(output_dir, output_name)
    if os.path.exists(output_path):
        raise ValueError(
            f'Cannot extract archive, output file already exists: {output_path}')
    archive_path = os.path.join(volume_dir, os.path.basename(volume_dir))
    with multivolumefile.open(archive_path, mode='rb') as target_archive:
        with py7zr.SevenZipFile(target_archive, 'r') as archive:
            archive.extractall(output_dir)
    os.rename(os.path.join(output_dir, 'dataset'), output_path)
    return output_path


if __name__ == '__main__':
    data_dir = read_env_var('RAW_DATA_DIR')
    root_dir = read_env_var('ROOT_DIR')
    volume_dir = os.path.join(root_dir, 'core/data/test.7z')
    compress_to_archive(os.path.join(data_dir, 'gothic'), volume_dir)
    extract_archive(volume_dir, os.path.join(
        root_dir, 'core/data/extracted-test'))
