import cv2
import os
from tqdm import tqdm

from Img2sketches import img2sketches
from Candidate_match import candidate_match
from Edge_extraction import canny

imgdir = "../images-copy/"
savedir = "../images-copy2/"
img_names = os.listdir(imgdir)
for img_name in tqdm(img_names):
    img_path = imgdir + img_name
    save_path = savedir + img_name
    img = cv2.imread(img_path)
    edge_img = canny(img, (300, 300))
    cv2.imwrite(save_path, edge_img)
