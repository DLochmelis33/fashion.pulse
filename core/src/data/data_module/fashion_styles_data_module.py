import json
import os
import pytorch_lightning as pl
import torch
import torch.nn.functional as F
from torch.utils.data import DataLoader, Dataset, random_split
from torchvision import transforms, datasets

import matplotlib.pyplot as plt

from utils.archive_utils import extract_archive
from utils.env_utils import read_env_var


class FashionStylesDataModule(pl.LightningDataModule):
    def __init__(
            self,
            data_dir: str,
            batch_size: int,
            num_workers: int = 0,
            seed: int = 65,
    ):
        super().__init__()
        self.data_dir = data_dir
        self.batch_size = batch_size

        self.num_workers = num_workers
        self.generator = torch.Generator().manual_seed(seed)

        self.dataset_dir_name = 'img_fashion_styles_extracted'
        self.dataset_path = os.path.join(data_dir, self.dataset_dir_name)
        self.dataset_archive_path = os.path.join(
            data_dir, 'img_fashion_styles.7z')

        self.num_classes = None
        self.dataset: datasets.ImageFolder = None

    def _extract_dataset(self):
        if not os.path.exists(self.dataset_archive_path):
            raise ValueError(
                f'Unable to find {self.dataset_archive_path}')
        return extract_archive(volume_dir=self.dataset_archive_path,
                               output_dir=self.data_dir, output_name=self.dataset_dir_name)

    def prepare_data(self):
        if not os.path.exists(self.dataset_path):
            self._extract_dataset()
        self.num_classes = len(os.listdir(self.dataset_path))

        # input: (3, <=236, ~100-700)
        # crop + resize: 236 > 224 = 192 + 32
        self.transform = transforms.Compose([
            transforms.RandomCrop(
                (224, 224),
                pad_if_needed=True,
                padding_mode='symmetric'
            ),
            transforms.Resize([192, 192]),
            transforms.ToTensor(),
            transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
        ])

    def _save_classes_labels(self):
        classes_to_labels = {idx: label for label, idx in self.dataset.class_to_idx.items()}
        file_path = os.path.join(self.data_dir, 'classes_labels.json')
        with open(file_path, 'w') as file:
            file.write(json.dumps(classes_to_labels))
            
    def setup(self, stage=None):
        self.dataset = datasets.ImageFolder(
            root=self.dataset_path,
            transform=self.transform,
            target_transform=transforms.Lambda(
                lambda label: F.one_hot(torch.tensor(label), self.num_classes)
            )
        )
        self._save_classes_labels()
        self.train, self.valid, self.test = random_split(
            self.dataset, [0.8, 0.1, 0.1], generator=self.generator
        )

    def _dataloader(self, dataset: Dataset, is_train: bool = False) -> DataLoader:
        return DataLoader(
            dataset=dataset,
            batch_size=self.batch_size,
            drop_last=is_train,
            shuffle=is_train,
            num_workers=self.num_workers,
            generator=self.generator
        )

    def train_dataloader(self):
        return self._dataloader(self.train, is_train=True)

    def val_dataloader(self):
        return self._dataloader(self.valid)

    def test_dataloader(self):
        return self._dataloader(self.test)


if __name__ == '__main__':
    data_dir = read_env_var('DATA_DIR')

    def init_dm() -> DataLoader:
        dm = FashionStylesDataModule(data_dir=data_dir, batch_size=256)
        dm.prepare_data()
        dm.setup()
        return dm

    data_module = init_dm()
    data_module = init_dm()

    # note: don't forget to comment transform.Normalize :)
    images = next(iter(data_module.train_dataloader()))[0]
    images = images.numpy().transpose((0, 2, 3, 1))
    os.makedirs('pics-test', exist_ok=True)
    for i in range(100):
        plt.imshow(images[i])
        plt.savefig(f'pics-test/{i}.png')
