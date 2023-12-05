import os
import pytorch_lightning as pl
import torch
# import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader, Dataset, random_split
from torchvision import transforms, datasets

from utils.archive_utils import extract_archive
from utils.env_utils import read_env_var


class FashionStylesDataModule(pl.LightningDataModule):
    def __init__(
            self,
            batch_size: int,
            dataset_path: str = None,
            dataset_archive_path: str = None,
            num_workers: int = 0,
            seed: int = 65,
    ):
        super().__init__()
        self.batch_size = batch_size

        if dataset_archive_path is None and dataset_path is None:
            raise ValueError(
                'Either `dataset_archive_path` or `dataset_path` should be specified')

        self.dataset_path = dataset_path
        self.dataset_archive_path = dataset_archive_path
        self.num_workers = num_workers
        self.generator = torch.Generator().manual_seed(seed)

        self.num_classes = None

    def _extract_dataset(self) -> str:
        if not os.path.exists(self.dataset_archive_path):
            raise ValueError(
                f'Unable to find {self.dataset_archive_path}')
        data_dir = os.path.dirname(self.dataset_archive_path)
        dataset_dir_name = 'img_fashion_styles_extracted'
        return extract_archive(volume_dir=self.dataset_archive_path,
                               output_dir=data_dir, output_name=dataset_dir_name)

    def prepare_data(self):
        if self.dataset_path is None:
            self.dataset_path = self._extract_dataset()
        self.num_classes = len(os.listdir(self.dataset_path))

        # TODO: transforms
        # input: (???)
        self.transform = transforms.Compose([
            transforms.RandomResizedCrop(224),
            transforms.ToTensor()
        ])

    def setup(self, stage=None):
        dataset = datasets.ImageFolder(
            root=self.dataset_path,
            transform=self.transform,
            target_transform=transforms.Lambda(
                lambda label: F.one_hot(torch.tensor(label), self.num_classes)
            )
        )
        self.train, self.valid, self.test = random_split(
            dataset, [0.8, 0.1, 0.1], generator=self.generator
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

    def init_and_print_len(dm: DataLoader):
        dm.prepare_data()
        dm.setup()
        print(f'{len(dm.train_dataloader())}')

    dataset_archive_path = os.path.join(data_dir, 'img_fashion_styles.7z')
    data_module = FashionStylesDataModule(
        dataset_archive_path=dataset_archive_path, batch_size=256)
    init_and_print_len(data_module)

    dataset_path = os.path.join(data_dir, 'img_fashion_styles_extracted')
    data_module = FashionStylesDataModule(
        dataset_path=dataset_path, batch_size=256)
    init_and_print_len(data_module)
