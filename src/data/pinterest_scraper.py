from typing import List, Tuple
from pinterest_board_parser import parse_pins_from_board
import numpy as np
from concurrent.futures import ThreadPoolExecutor
import threading
import os
import requests


def _split_list(lst: List, n: int) -> List[List]:
    return list(map(lambda arr: arr.tolist(), np.array_split(lst, n)))


def save_image_from_url(url: str, output_dir: str, new_img_name: str = None):
    os.makedirs(output_dir, exist_ok=True)
    file_name = os.path.basename(url)
    img_name, img_ext = os.path.splitext(file_name)
    if new_img_name is not None:
        img_name = new_img_name
    img_path = os.path.join(output_dir, img_name + img_ext)

    response = requests.get(url, stream=True)
    if response.status_code != 200:
        raise ValueError(
            f"Failed to download image from {url}: HTTP code {response.status_code}")

    with open(img_path, 'wb') as file:
        for chunk in response.iter_content(chunk_size=4096):
            file.write(chunk)

    return img_path


def save_images_from_urls(
    urls_with_idx: List[Tuple[str, int]],
    output_dir: str,
    img_name_prefix: str = "",
    logging_enabled: bool = False,
    log_every_nth_step: int = 5
) -> List[str]:
    
    def log_thread_message(msg: str) -> None:
        if logging_enabled:
            print(f'Worker #{threading.get_native_id()}: {msg}')

    imgs_paths = []
    for i, url_id in enumerate(urls_with_idx):
        url, id = url_id
        try:
            img_path = save_image_from_url(
                url, output_dir, new_img_name=f'{img_name_prefix}{id}')
            imgs_paths.append(img_path)
            if (i + 1) % log_every_nth_step == 0:
                log_thread_message(f'in progress | saved {i + 1} / {len(urls_with_idx)} images')
        except Exception as e:
            log_thread_message(f'failed to save image {url} due to {e}')
            
    log_thread_message(f'finished | saved {len(urls_with_idx)} images')

    return imgs_paths


def download_images(
        urls: List[str],
        output_dir: str,
        board_name: str,
        num_of_workers: int,
        logging_enabled: bool = False
) -> List[str]:
    num_of_workers = min(num_of_workers, len(urls))
    urls_chunks = _split_list(
        list(zip(urls, range(len(urls)))),
        num_of_workers
    )

    def worker_job(urls_with_idx: List[Tuple[str, int]]) -> List[str]:
        return save_images_from_urls(
            urls_with_idx,
            output_dir,
            img_name_prefix=board_name,
            logging_enabled=logging_enabled,
            log_every_nth_step=10
        )

    try:
        with ThreadPoolExecutor(max_workers=num_of_workers) as executor:
            imgs_paths = []
            for chunk_img_paths in executor.map(worker_job, urls_chunks):
                imgs_paths += list(chunk_img_paths)
        return imgs_paths

    except KeyboardInterrupt:
        print(f"Interrupted")


def download_images_from_board(
        board_url: str,
        output_dir: str,
        board_name: str = None,
        num_of_workers: int = 10,
        logging_enabled: bool = False
) -> List[str]:
    pins_urls = parse_pins_from_board(
        board_url, logging_enabled=logging_enabled)
    if logging_enabled:
        print()
    imgs_paths = download_images(
        pins_urls,
        output_dir=output_dir,
        board_name=board_name,
        num_of_workers=num_of_workers,
        logging_enabled=logging_enabled
    )
    if logging_enabled:
        print(f"Successfully downloaded {len(imgs_paths)} images")
    return imgs_paths
