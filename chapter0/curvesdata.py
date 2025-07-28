import cv2
import numpy as np
import skia
import torch

from PIL import Image
from depth_anything.dpt import DepthAnythingV2
from glob import glob
from multiprocessing import Pool
from tqdm import tqdm


def init_depth():
	DEVICE = 'cuda' if torch.cuda.is_available() else 'mps' if torch.backends.mps.is_available() else 'cpu'
	model_configs = {
		'vits': {'encoder': 'vits', 'features': 64, 'out_channels': [48, 96, 192, 384]},
		'vitb': {'encoder': 'vitb', 'features': 128, 'out_channels': [96, 192, 384, 768]},
		'vitl': {'encoder': 'vitl', 'features': 256, 'out_channels': [256, 512, 1024, 1024]},
		'vitg': {'encoder': 'vitg', 'features': 384, 'out_channels': [1536, 1536, 1536, 1536]}
	}

	encoder = 'vitb' # or 'vits', 'vitb', 'vitg'
	model = DepthAnythingV2(**model_configs[encoder])
	model.load_state_dict(torch.load(f'depth_anything/checkpoints/depth_anything_v2_{encoder}.pth', map_location='cpu'))
	model = model.to(DEVICE).eval()
	return model


def object_to_curves(image_path: str, depth_model: DepthAnythingV2):
	image = np.array(Image.open(image_path))
	h, w = image.shape[:2]
	depth = depth_model.infer_image(np.array(image))
	depth = (depth - depth.min()) / (depth.max() - depth.min() + 1e-8)
	edges = cv2.Canny((depth * 255).astype(np.uint8), 1, 80)
	contours, hierarchy = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	paths = []
	for contour in contours:
		points = contour.squeeze().tolist()
		points = [[p[0]/w, p[1]/h] for p in points]
		paths.append(points)
	return paths


def point2letters(p):
	letters = "ABCDEFGHIJ" + "KLMNOPQRST" + "UVWXY"
	x, y = p
	x = letters[int(25*x)]
	y = letters[int(25*y)]
	return x+y

def curve2string(path):
	string = [point2letters(pt) for pt in path] + ["Ze"]
	sarray = ["Zs"]
	for s in string:
		if s != sarray[-1]:
			sarray.append(s)
	string = " ".join(sarray)
	return string


def paths2string(paths):
	return " ".join([curve2string(path) for path in paths])


depth_model = init_depth()
files = glob("data/**/*.jpeg", recursive=True)
np.random.shuffle(files)

count = 0
with open("curves.txt", "w") as fd:
	for f in tqdm(files, total=len(files)):
		try:
			paths = object_to_curves(f, depth_model)
			s = paths2string(paths)
			fd.write(s + "\n")
			count += 1
		except:
			pass

		if count >= 10000:
			break

