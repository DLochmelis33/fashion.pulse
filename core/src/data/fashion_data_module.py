
# class DataModule(pl.LightningDataModule):
#     def __init__(self, data_path='./'):
#         super().__init__()
#         self.data_path = data_path

#     def prepare_data(self):
#         CelebA(root=self.data_path, download=True)
#         # input: (3, 218, 178)
#         self.transform = transforms.Compose([
#             transforms.RandomCrop((160, 160)), # 178 > 160 = 128 + 32
#             transforms.Resize([128, 128]),
#             transforms.ToTensor(),
#             transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)) # why?
#         ])

#     def setup(self, stage=None):
#         self.train = CelebA(root=self.data_path,
#                                      split='train',
#                                      target_type='attr',
#                                      transform=self.transform)

#         self.valid = CelebA(root=self.data_path,
#                                      split='valid',
#                                      target_type='attr',
#                                      transform=self.transform)

#         self.test = CelebA(root=self.data_path,
#                                     split='test',
#                                     target_type='attr',
#                                     transform=self.transform)

#     def train_dataloader(self):
#         train_loader = DataLoader(dataset=self.train,
#                                   batch_size=BATCH_SIZE,
#                                   drop_last=True,
#                                   shuffle=True,
#                                   num_workers=NUM_WORKERS)
#         return train_loader

#     def val_dataloader(self):
#         valid_loader = DataLoader(dataset=self.valid,
#                                   batch_size=BATCH_SIZE,
#                                   drop_last=False, # why not True, the same question about test
#                                   shuffle=False,
#                                   num_workers=NUM_WORKERS)
#         return valid_loader

#     def test_dataloader(self):
#         test_loader = DataLoader(dataset=self.test,
#                                  batch_size=BATCH_SIZE,
#                                  drop_last=False,
#                                  shuffle=False,
#                                  num_workers=NUM_WORKERS)
#         return test_loader

# # set up path
# # torch.manual_seed(1)
# # data_module = DataModule(data_path='./data')