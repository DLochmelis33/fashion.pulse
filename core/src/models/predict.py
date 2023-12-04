
# path = trainer.checkpoint_callback.best_model_path
# lightning_model = DlhfLightningModel.load_from_checkpoint(
#     path, model=DlhfModel(num_classes=NUM_CLASSES)
# )
# lightning_model.cpu()
# lightning_model.eval()

# test_dataloader = data_module.test_dataloader()
# acc = torchmetrics.Accuracy(task='multilabel', num_labels=NUM_CLASSES)

# for batch in test_dataloader:
#     x, y = batch

#     with torch.no_grad():
#         y_pred = lightning_model(x)

#     print(f'acc: {acc(y_pred, y)}')
#     break

# y_pred[:5]