from typing import Dict

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


predict_transform = transforms.Compose([
    transforms.Lambda(
        lambda image: transforms.RandomCrop(
            max(image.height, image.width),
            pad_if_needed=True,
            padding_mode='symmetric'
        )
    ),
    transforms.Resize([192, 192]),
    transforms.ToTensor(),
    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
])


def predict(image_bytes: bytes, lightning_model: LightningFashionStylesModel) -> Dict[str, float]:
    image = Image.open(io.BytesIO(image_bytes))
    x = predict_transform(image)

    with torch.no_grad():
        y_pred = lightning_model(x)

    styles = lightning_model.class_names
    return {style: score for style, score in zip(styles, y_pred.tolist())}


if __name__ == '__main__':
    data_dir = read_env_var('DATA_DIR')
    img_path = os.path.join(
        data_dir, 'img_fashion_styles_extracted', 'gothic', 'women-490-65.jpg')
    with open(img_path, 'rb') as f:
        img_bytes = f.read()

    lm = load_eval_model('best')
    print(predict(img_bytes, lm))
