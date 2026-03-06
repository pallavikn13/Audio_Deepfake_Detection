import os
import numpy as np
from feature_extraction import extract_mfcc
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from sklearn.model_selection import train_test_split

X = []
y = []

for label, folder in enumerate(["dataset/real", "dataset/fake"]):
    for file in os.listdir(folder):
        path = os.path.join(folder, file)
        mfcc = extract_mfcc(path)
        X.append(mfcc)
        y.append(label)

X = np.array(X)
y = np.array(y)

X = X.reshape(X.shape[0], X.shape[1], 1)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

model = Sequential([
    LSTM(128, return_sequences=True, input_shape=(40,1)),
    LSTM(64),
    Dense(1, activation='sigmoid')
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

model.fit(X_train, y_train, epochs=30, batch_size=32, validation_data=(X_test, y_test))

model.save("model/deepfake_model.h5")

print("Model trained & saved successfully!")