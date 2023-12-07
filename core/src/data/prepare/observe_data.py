import os
from utils.env_utils import read_env_var


def print_downloaded_data_size(data_dir: str):
    total = 0
    styles = {style: None for style in os.listdir(data_dir)}
    for style in styles.keys():
        style_dir = os.path.join(data_dir, style)
        style_size = len(os.listdir(style_dir))
        total += style_size
        styles[style] = style_size

    styles = dict(
        sorted(styles.items(), key=lambda item: item[1], reverse=True)
    )
    for style, style_size in styles.items():
        print(f'{style}: {style_size} images')
    print('-------')
    print(f'Total: {len(styles)} styles, {total} images')


if __name__ == '__main__':
    root_data = read_env_var('DATA_DIR')
    data_dir = os.path.join(root_data, 'img_fashion_styles_extracted')
    print_downloaded_data_size(data_dir)
