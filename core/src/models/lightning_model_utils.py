from pytorch_lightning.loggers import WandbLogger
from pytorch_lightning.callbacks import LambdaCallback, ModelCheckpoint

import os
import wandb

from utils.env_utils import read_env_var
from models.fashion_style_model import FashionStylesModel
from models.lightning_model import LightningFashionStylesModel

BATCH_SIZE = 64
LEARNING_RATE = 1e-3
NUM_CLASSES = 20


# IMPORTANT NOTE: login to wandb before training the model
# > !wandb login


def get_checkpoints_dir() -> str:
    return os.path.join(read_env_var('ARTIFACTS_DIR'), 'checkpoints')

    
def get_wandb_dir() -> str:
    return os.path.join(read_env_var('ARTIFACTS_DIR'), 'wandb')


def setup_wandb_logger(lightning_model: LightningFashionStylesModel, resume_run_id: str = None) -> WandbLogger:
    wandb_dir = get_wandb_dir()
    os.makedirs(wandb_dir, exist_ok=True)
    if resume_run_id is None:
        wandb.init(dir=wandb_dir)
    else:
        wandb.init(dir=wandb_dir, id=resume_run_id, project='fashion.pulse-core_src', resume='must')

    wandb_logger = WandbLogger(project='fashion-pulse', log_model='all')
    wandb_logger.experiment.config['batch_size'] = BATCH_SIZE
    wandb_logger.experiment.config['learning_rate'] = LEARNING_RATE
    wandb_logger.watch(lightning_model, log='all')
    return wandb_logger


def get_model_checkpoint_callback() -> ModelCheckpoint:
    return ModelCheckpoint(
        monitor='val_f1',
        mode='max',
        dirpath=get_checkpoints_dir()
    )


def load_from_checkpoint(checkpoint_path: str) -> LightningFashionStylesModel:
    return LightningFashionStylesModel.load_from_checkpoint(
        checkpoint_path, model=FashionStylesModel(num_classes=NUM_CLASSES)
    )
