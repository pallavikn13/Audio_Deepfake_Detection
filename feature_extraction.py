<<<<<<< HEAD
import librosa
import numpy as np

def extract_mfcc(file_path):
    audio, sr = librosa.load(file_path, sr=16000)
    mfcc = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=40)
    mfcc = np.mean(mfcc.T, axis=0)
=======
import librosa
import numpy as np

def extract_mfcc(file_path):
    audio, sr = librosa.load(file_path, sr=16000)
    mfcc = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=40)
    mfcc = np.mean(mfcc.T, axis=0)
>>>>>>> ff7d1f8aeb76fd3585a1b833f713ba1743e2d869
    return mfcc