import numpy as np
import pandas as pd
from keras.preprocessing.image import ImageDataGenerator, load_img
from keras.utils import to_categorical
from sklearn.model_selection import train_test_split
import tensorflow as tf
import matplotlib.pyplot as plt
import random
import os
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Dropout, Flatten, Dense, Activation, BatchNormalization
from keras import models

filenames = os.listdir('C:/Users/davis/Datasets/input_data')

categories = []
for filename in filenames:
    category = filename.split('.')[0]
    if category == 'ben':
        categories.append(0)
    elif category == 'dea':
        categories.append(1)
    elif category == 'squ':
        categories.append(2)

df = pd.DataFrame({
    'filename': filenames,
    'category': categories,
})

ImageModel = Sequential()

ImageModel.add(Conv2D(32, (3, 3), activation='relu', input_shape=(150,150, 3)))
ImageModel.add(MaxPooling2D(pool_size=(2, 2)))
ImageModel.add(Dropout(0.25))

ImageModel.add(Conv2D(64, (3, 3), activation='relu'))
ImageModel.add(MaxPooling2D(pool_size=(2, 2)))
ImageModel.add(Dropout(0.25))

ImageModel.add(Flatten())
ImageModel.add(Dense(96, activation='relu'))
ImageModel.add(Dropout(0.5))
ImageModel.add(Dense(3, activation='softmax'))

ImageModel.compile(loss='categorical_crossentropy', optimizer='Adam', metrics=['accuracy'])


df["category"] = df["category"].replace({ 0: 'ben', 1: 'dea', 2: 'squ' })

train_df, validate_df = train_test_split(df, test_size=0.20, random_state=0)
train_df = train_df.reset_index(drop=True)
validate_df = validate_df.reset_index(drop=True)
total_train = train_df.shape[0]
total_validate = validate_df.shape[0]


train_datagen = ImageDataGenerator(
                                    rotation_range=15,
                                    rescale=1./255,
                                    shear_range=0.1,
                                    zoom_range=0.2,
                                    horizontal_flip=True,
                                    width_shift_range=0.1,
                                    height_shift_range=0.1
)

validation_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_dataframe(
    train_df,
    "C:/Users/davis/Datasets/input_data",
    x_col='filename',
    y_col='category',
    target_size=(150,150),
    class_mode='categorical',
    batch_size=16
)

validation_generator = validation_datagen.flow_from_dataframe(
    validate_df,
    "C:/Users/davis/Datasets/input_data",
    x_col='filename',
    y_col='category',
    target_size=(150,150),
    class_mode='categorical',
    batch_size=16
)

epochs=200
batch_size=15

history = ImageModel.fit_generator(
    train_generator,
    epochs=epochs,
    validation_data=validation_generator,
    validation_steps=total_validate/batch_size,
    steps_per_epoch=10,
)

ImageModel.save('imageModel.h5')
