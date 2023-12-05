from pytorch_lightning.loggers import WandbLogger

from models.fashion_style_model import FashionStylesModel
from models.lightning_model import LightningFashionStylesModel

NUM_EPOCHS = 1
BATCH_SIZE = 64
LEARNING_RATE = 1e-3
NUM_CLASSES = 20

# IMPORTANT NOTE: login to wandb before training the model
# > !wandb login


def setup_wandb_logger(lightning_model: LightningFashionStylesModel) -> WandbLogger:
    wandb_logger = WandbLogger(project='fashion-pulse', log_model='all')
    wandb_logger.experiment.config['batch_size'] = BATCH_SIZE
    wandb_logger.experiment.config['learning_rate'] = LEARNING_RATE
    wandb_logger.watch(lightning_model, log='all')
    return wandb_logger


def load_from_checkpoint(checkpoint_path: str) -> LightningFashionStylesModel:
    return LightningFashionStylesModel.load_from_checkpoint(
        checkpoint_path, model=FashionStylesModel(num_classes=NUM_CLASSES)
    )
