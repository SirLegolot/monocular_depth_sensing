import onnxruntime as nxrun
import numpy as np

from tqdm import tqdm
import torch
from imageio import imread, imwrite
from path import Path
import os

from config import get_opts

from SC_Depth import SC_Depth
from SC_DepthV2 import SC_DepthV2

import datasets.custom_transforms as custom_transforms

from visualization import *

# normaliazation
inference_transform = custom_transforms.Compose([
    custom_transforms.RescaleTo([256, 320]),
    custom_transforms.ArrayToTensor(),
    custom_transforms.Normalize()]
)

# Set up onnx runtime
sess = nxrun.InferenceSession("sc_depth_pl.onnx")
input_name = sess.get_inputs()[0].name


def img_file_to_npy(img_file):
    img = imread(img_file).astype(np.float32)
    tensor_img = inference_transform([img])[0][0].unsqueeze(0).cuda()
    tensor_img = tensor_img.cpu().detach().numpy()
    return tensor_img

tensor_img = img_file_to_npy("demo/input/00.jpg")

# Run onnx
result = sess.run(None, {input_name: tensor_img})

def npy_result_to_tensor(result):
    result = torch.FloatTensor(result)[0]
    result = torch.clamp(result, min=0.0, max=1.0)
    return result

result = npy_result_to_tensor(result)

print("TYPPPPE", type(result), result.size(), result.dtype)

print(result[0].argmax())
print(result[0])

vis = visualize_depth(result[0, 0]).permute(1, 2, 0).numpy() * 255
        
imwrite('onnx_test_depth.jpg', vis.astype(np.uint8))

depth = result[0, 0].cpu().numpy()
np.save('onnx_test_depth.npy', depth)

from PIL import Image
#Image.fromarray(np.load('test.npy').reshape(28, 28) * 255).show()