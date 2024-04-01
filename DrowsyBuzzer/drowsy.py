# https://www.kaggle.com/datasets/ismailnasri20/driver-drowsiness-dataset-ddd

import pandas as pd

from tensorflow import keras
from keras.preprocessing.image import ImageDataGenerator as data_augment
from keras.models import Model,Sequential
from keras.layers import Input,Conv2D,MaxPooling2D,Dropout,Flatten,Dense,GlobalAveragePooling2D,BatchNormalization
from keras.callbacks import EarlyStopping,ModelCheckpoint
from tensorflow.keras import layers as layers

#data augmetation 
data_generate_training = data_augment (rescale=1./255, 
                              shear_range = 0.2,
                              zoom_range = 0.2,
                              fill_mode = "nearest",
                              horizontal_flip = True,
                              width_shift_range = 0.2,
                              height_shift_range = 0.2,
                              validation_split = 0.15)

data_generate_test = data_augment(rescale = 1./255)

traind = data_generate_training.flow_from_directory("./Driver Drowsiness Dataset (DDD)",
                                          target_size = (227, 227),
                                          seed = 123,
                                          batch_size = 32,
                                          subset = "training")

testd = data_generate_training.flow_from_directory("./Driver Drowsiness Dataset (DDD)",
                                          target_size = (227, 227),
                                          seed = 123,
                                          batch_size = 32,
                                          subset = "validation")

CNNmodel = keras.Sequential([
    layers.Conv2D(32, (3, 3), input_shape=(227, 227, 3), activation='relu'),
    layers.BatchNormalization(),
    layers.MaxPooling2D((2,2)),
    layers.Dropout(0.5),
    
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.BatchNormalization(),
    layers.MaxPooling2D((2,2)),
    layers.Dropout(0.5),
    
    layers.Conv2D(128, (3, 3), activation='relu'),
    layers.BatchNormalization(),
    layers.MaxPooling2D((2,2)),
    layers.Dropout(0.5),

    layers.Flatten(),
    layers.Dense(256, activation='relu'),
    layers.Dropout(0.5),  
    layers.Dense(128, activation = 'relu', kernel_regularizer='l1'),
    layers.Dense(2, activation = 'sigmoid')
])

CNNmodel.compile(optimizer='adam',
              loss="binary_crossentropy",
              metrics=['accuracy'])

history = CNNmodel.fit(traind, epochs = 20, validation_data = testd) 
