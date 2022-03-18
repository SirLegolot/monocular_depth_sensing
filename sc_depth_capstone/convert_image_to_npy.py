import numpy as np
import cv2

from imageio import imread, imwrite
from path import Path
import os


import datasets.custom_transforms as custom_transforms

from visualization import *


inference_transform = custom_transforms.Compose([
    custom_transforms.RescaleTo([256, 320]),
    custom_transforms.ArrayToTensor(),
    custom_transforms.Normalize()]
)

def rescale(im, resize_shape=[256, 320]):
    in_h, in_w, _ = im.shape
    out_h, out_w = resize_shape[0], resize_shape[1]

    if in_h != out_h or in_w != out_w:
        if im.ndim < 3:  # depth
            scaled_im = cv2.resize(im, dsize=(
                out_w, out_h), fx=1.0, fy=1.0, interpolation=cv2.INTER_NEAREST)
        else:
            scaled_im = cv2.resize(im, dsize=(
                out_w, out_h), interpolation=cv2.INTER_LINEAR)
    else:
        scaled_im = im

    return scaled_im

def to_tensor(im):
    tensorized = np.transpose(im, (2, 0, 1))/255
    return tensorized

def normalize(im, mean=[0.45, 0.45, 0.45], std=[0.225, 0.225, 0.225]):
    # for i in range(len(mean)):
    im -= mean[0]
    im /= std[0]
    return im

def img_file_to_tensor(img_file):
    img = imread(img_file).astype(np.float32)
    tensor_img = inference_transform([img])[0][0].unsqueeze(0)
    tensor_img = tensor_img.cpu().detach().numpy()
    return tensor_img

def custom_transform(img_file):
    im = imread(img_file).astype(np.float32)
    im = rescale(im)
    im = to_tensor(im)
    im = normalize(im)
    return np.expand_dims(im, axis=0)

tensor_img = img_file_to_tensor("demo/input/00.jpg")
my_img = custom_transform("demo/input/00.jpg")
print(np.allclose(tensor_img, my_img))

np.save("demo_00.npy", my_img)


