# -*- coding: utf-8 -*-
"""training.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1oSC1GXmJ18MyULXqTPqBhDEv4AwqcmSy
"""

# Commented out IPython magic to ensure Python compatibility.
import os
import sys
import pickle
import copy
from datetime import datetime
from tqdm import tqdm
import numpy as np
import pandas as pd
import seaborn as sns
import torch
import torch.nn.functional as F
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
import matplotlib.pyplot as plt
# %matplotlib inline

from google.colab import drive
drive.mount('/content/drive')
dataset_path = "/content/drive/My Drive/UrbanSound8K/UrbanSound8K"
print(os.listdir(dataset_path))
print("success")

import os
import pickle
file_path = os.path.join("/content/drive/My Drive/UrbanSound8K/UrbanSound8K", "extracted_features.pkl")
try:
    with open(file_path, "rb") as f:
       e = pickle.load(f)
    print(e)
except FileNotFoundError:
    print(f"Error: File not found at path: {file_path}")

### Split the dataset into independent and dependent dataset

e_df = pd.DataFrame(e, columns=["feature", "class"])
# as e was a list so we convert into a dataframe
X=np.array(e_df['feature'].tolist())
y=np.array(e_df['class'].tolist())

X.shape

y,"and",y.shape

print("y shape:", y.shape)
print("y data type:", type(y))
print(y[:2])  # Print first 10 values

### Train Test Split
from sklearn.model_selection import train_test_split
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2,random_state=0)

# here 20% of the dataset will be used for testing

print("Training set size:", X_train.shape, y_train.shape)
print("Testing set size:", X_test.shape, y_test.shape)

"success"

"""# ANN Model"""

import tensorflow as tf
print(tf.__version__)

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense,Dropout,Activation,Flatten
from tensorflow.keras.optimizers import Adam
from sklearn import metrics

### No of classes
num_labels=y.shape[1]
" total classes ::: ",num_labels

# Instead of just calling Dense() without arguments, specify the number of units:
Dense(units=64)  # Replace 64 with the desired number of units for this layer

# ANN

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Dropout, BatchNormalization

model = Sequential()

### First Layer
model.add(Dense(512, input_shape=(40,)))
model.add(Activation('relu'))
model.add(BatchNormalization())
model.add(Dropout(0.5))

### Second Layer
model.add(Dense(1024))
model.add(Activation('relu'))
model.add(BatchNormalization())
model.add(Dropout(0.5))

### Third Layer
model.add(Dense(512))
model.add(Activation('relu'))
model.add(BatchNormalization())
model.add(Dropout(0.5))

### Fourth Layer
model.add(Dense(256))
model.add(Activation('relu'))
model.add(BatchNormalization())
model.add(Dropout(0.5))

### Final Layer
model.add(Dense(num_labels))
model.add(Activation('softmax'))

model.summary()

from tensorflow.keras.optimizers import Adam

model.compile(
    optimizer=Adam(learning_rate=0.0001),  # Lower learning rate for better convergence
    loss='categorical_crossentropy',  # Suitable for multi-class classification
    metrics=['accuracy']
)

from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau, TensorBoard
from datetime import datetime
import os
num_epochs = 200
num_batch_size = 20
checkpointer = ModelCheckpoint(filepath='saved_models/audio_classification_best.keras',
                               verbose=1, save_best_only=True)

early_stopping = EarlyStopping(monitor='val_loss',
                               patience=5,
                               restore_best_weights=True,
                               verbose=1)

lr_scheduler = ReduceLROnPlateau(monitor='val_loss',
                                  factor=0.5,
                                  patience=3,
                                  min_lr=1e-6,
                                  verbose=1)
log_dir = "logs/fit/" + datetime.now().strftime("%Y%m%d-%H%M%S")
tensorboard_callback = TensorBoard(log_dir=log_dir, histogram_freq=1)

start = datetime.now()
# Train the model
model.fit(X_train, y_train,
          batch_size=num_batch_size,
          epochs=num_epochs,
          validation_data=(X_test, y_test),
          callbacks=[checkpointer, early_stopping, lr_scheduler, tensorboard_callback],
          verbose=1)

duration = datetime.now() - start
print("Training completed in time: ", duration)

test_accuracy=model.evaluate(X_test,y_test,verbose=0)
print(test_accuracy[1]*100,'%')