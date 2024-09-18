# Developed by Dhanush R S

import os
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.optimizers import Adam

# Define image size and directories for FER2013 dataset
img_size = 48

# Paths for FER2013 train and test datasets
fer_train_dir = 'dataset/fer2013/train'
fer_test_dir = 'dataset/fer2013/test'

# Data augmentation for FER2013 dataset
fer_train_datagen = ImageDataGenerator(
    rescale=1./255,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True
)

fer_test_datagen = ImageDataGenerator(rescale=1./255)

# FER2013 Data Generators
fer_train_generator = fer_train_datagen.flow_from_directory(
    fer_train_dir,
    target_size=(img_size, img_size),
    color_mode='grayscale',
    batch_size=64,
    class_mode='categorical'
)

fer_test_generator = fer_test_datagen.flow_from_directory(
    fer_test_dir,
    target_size=(img_size, img_size),
    color_mode='grayscale',
    batch_size=64,
    class_mode='categorical'
)

# Define the CNN model
def create_model():
    model = Sequential()

    model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(img_size, img_size, 1)))  # Grayscale images
    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Conv2D(64, (3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Conv2D(128, (3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Flatten())
    model.add(Dense(128, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(7, activation='softmax'))  # Assuming 7 emotion classes

    return model

# Compile and train the model
def train_model():
    model = create_model()

    model.compile(optimizer=Adam(learning_rate=0.001), loss='categorical_crossentropy', metrics=['accuracy'])

    # Train the model on FER2013 dataset
    model.fit(
        fer_train_generator,
        epochs=25,
        validation_data=fer_test_generator
    )

    # Save the trained model
    model.save('backend/emotion_model.h5')

if __name__ == "__main__":
    train_model()
