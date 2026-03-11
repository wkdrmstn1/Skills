import numpy as np
import cv2
import os
import glob

base_dir = 'train'
categories = ['apples', 'tomatoes']

X = []
y = []

for class_index, category in enumerate(categories):
    path_pattern = os.path.join(base_dir, category, '*.jpeg')
    files = glob.glob(path_pattern)
    
    for file_path in files:
        img = cv2.imread(file_path)
        if img is not None:
            img = cv2.resize(img, (100, 100))
            X.append(img)
            y.append(class_index)

X = np.array(X)
y = np.array(y)

#np.save('AT.npy', X)
#np.save('label.npy', y)

print(len(X))
print(len(y))