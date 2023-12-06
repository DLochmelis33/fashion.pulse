from typing import Dict

import json
import os
import torch
import io
from PIL import Image
from torchvision import transforms

from models.lightning_model import LightningFashionStylesModel
from utils.env_utils import read_env_var

from .lightning_model_utils import load_from_checkpoint


def load_eval_model(checkpoint_path: str) -> LightningFashionStylesModel:
    lightning_model = load_from_checkpoint(checkpoint_path)
    lightning_model.cpu()
    lightning_model.eval()
    return lightning_model


def load_classes_labels() -> Dict[int, str]:
    data_dir = read_env_var('DATA_DIR')
    file_path = os.path.join(data_dir, 'classes_labels.json')
    with open(file_path, 'r') as file:
        return json.loads(file.read())


predict_transform = transforms.Compose([
    transforms.Lambda(
        lambda image: transforms.RandomCrop(
            max(image.height, image.width),
            pad_if_needed=True,
            padding_mode='symmetric'
        )(image)
    ),
    transforms.Resize([192, 192]),
    transforms.ToTensor(),
    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
])


def predict(image_bytes: bytes, lightning_model: LightningFashionStylesModel) -> Dict[str, float]:
    image = Image.open(io.BytesIO(image_bytes))
    x = torch.unsqueeze(predict_transform(image), dim=0)

    with torch.no_grad():
        y_pred = lightning_model(x)

    styles = load_classes_labels()
    scores = y_pred.tolist()
    return {styles[i]: scores[i] for i in range(len(scores))}


if __name__ == '__main__':
    data_dir = read_env_var('DATA_DIR')
    img_path = os.path.join(
        data_dir, 'img_fashion_styles_extracted', 'gothic', 'women-490-65.jpg')
    with open(img_path, 'rb') as f:
        img_bytes = f.read()

    lm = load_eval_model('/content/fashion.pulse/core/artifacts/checkpoints/epoch=0-step=285.ckpt')
    print(predict(img_bytes, lm))
