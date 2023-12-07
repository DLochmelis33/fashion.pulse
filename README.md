<img src="readme-atrifacts/fashion_pulse_logo.png" align="right" />

# fashion.pulse
<!-- Badges -->
[![releases](https://img.shields.io/github/v/release/DLochmelis33/fashion.pulse.svg)](https://github.com/DLochmelis33/fashion.pulse/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![contributions](https://img.shields.io/github/contributors/DLochmelis33/fashion.pulse)](https://github.com/DLochmelis33/fashion.pulse/graphs/contributors)

## Stylish Introduction ✨✨✨

The project provides a service that **_evaluates how fashionable an outfit on the image is_**. The fashion score is given for 20 different styles.

![Alt Text](readme-atrifacts/fashion_pulse_demo_mini.gif)

To try the app by yourself check the [Releases](https://github.com/DLochmelis33/fashion.pulse/releases) section!

### This repo includes
* *FastAPI* server and *Android* app implementation;
* *PyTorch Lightning* model to evaluate images' score;
* `img_fashion_styles` dataset gathered from *Pinterest*;
  
...and, of course, a developed infrastructure to reproduce our results and conduct further experiments.

### Table of contents
- [fashion.pulse](#fashionpulse)
  - [Stylish Introduction ✨✨✨](#stylish-introduction-)
    - [This repo includes](#this-repo-includes)
    - [Table of contents](#table-of-contents)
  - [Detailed repo structure 🔍](#detailed-repo-structure-)
  - [Train model \& deploy server 🚂](#train-model--deploy-server-)
    - [Train the fanciest model](#train-the-fanciest-model)
    - [Deploy the most reliable server](#deploy-the-most-reliable-server)
  - [Infrastructure methods overview ⚙️](#infrastructure-methods-overview-️)

## Detailed repo structure 🔍

Repo is organised in the following way:
* [`core`](core) &mdash; the main directory with everything related to experimenting with model and gathering the dataset;
  * [`data`](core/data) &mdash; the directory to keep the dataset there, initially there is only compressed `img_fashion_styles.7z` that will be extracted to the `img_fashion_styles_extracted` by `FashionStylesDataModule`;
  * [`notebooks`](core/notebooks/) &mdash; contains notebooks with several preliminary experiments and an example model's training pipeline;
  * [`src`](core/src) &mdash; contains all the machine learning code;
    * [`data`](core/src/data) &mdash; is dedicated to gathering, preparing and compressing the raw dataset (the ready-to-use compressed version is already located in the `data` directory);
    * [`models`](core/src/models) &mdash; every piece of code related to the training pipeline is located there;
    * [`server`](core/src/server) &mdash; contains code implementation of the _FastAPI_ server, to run it properly you'd probably need to refer to [`README_SERVER.md`](core/src/README_SERVER.md);
    * [`utils`](core/src/utils) &mdash; finally, just a bunch of util models used throughout the project;
* [`androidApp`](androidApp) &mdash; the implementation code of the _Android_ app.

## Train model & deploy server 🚂

### Train the fanciest model

**TL;DR**: you can skip reading and just jump to [the Jupyter notebook](core/notebooks/FashionPulsePipeline.ipynb) to check an example of the complete model training pipeline! But the more detailed guide is presented below.

Training model is pretty straightforward, luckily we made it simple! First, go to the `core/src` directory, all the following commands should be executed from there.
```bash
cd core/src
```

Since _Wanbd_ is used for logging the model, first you should log in to it with your credentials. If you use your own Wandb project, don't forget to update its name.
```bash
wandb login
```

Then set up several environment variables with the corresponding paths, but don't forget to use absolute paths.
```bash
export DATA_DIR=.../core/data # directory to extract dataset
export ARTIFACTS_DIR=.../core/artifacts # directory to store checkpoints and wand logs
```

Train model for the specified number of epochs. In Google Collab with GPU machine provided one epoch takes aproximately 1.5 minute.
```bash
python -m models.train --num_epochs=100
```
_Wandb_ will output the genereated run id (for example, `sg3yeobh`) &mdash; don't forget to save it and pass to the testing module further, so the test execution will also be logged in the same _Wandb_ run.

Once the training is finished, the time has come to test the model!
```bash
python -m models.test --run_id sg3yeobh
```

Finally, to use the trained model you can run `predict` module or call its functions directly from the Python code.
```bash
python -m models.predict --image_path img_fashion_styles_extracted/gothic/women-490-65.jpg --ckpt_path checkpoints/model.ckpt
``` 

### Deploy the most reliable server

See details in [`README_SERVER.md`](core/src/README_SERVER.md).

## Infrastructure methods overview ⚙️

Section is in progress. We tried to create the most readable code as possible, so we hope that a passionated reader would be able to go through it happily ;-) 