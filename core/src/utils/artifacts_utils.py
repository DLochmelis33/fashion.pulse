from typing import Dict
import os
import json

from .env_utils import read_env_var

def load_classes_labels() -> Dict[int, str]:
    data_dir = read_env_var('DATA_DIR')
    file_path = os.path.join(data_dir, 'classes_labels.json')
    with open(file_path, 'r') as file:
        classes_labels = json.loads(file.read())
    return {int(idx): label for idx, label in classes_labels.items()}
