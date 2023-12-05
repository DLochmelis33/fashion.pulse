import os
from utils.env_utils import read_env_var
from utils.archive_utils import compress_to_archive

if __name__ == '__main__':
    data_dir = read_env_var('DATA_DIR')
    dataset_dir = os.path.join(data_dir, 'img_fashion_styles')
    volume_name = 'img_fashion_styles.7z'

    compress_to_archive(
        dataset_dir,
        output_volume_dir=os.path.join(data_dir, volume_name),
        volume_size_MB=65
    )
