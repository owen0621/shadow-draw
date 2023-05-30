from Min_hash import minhash
from BiCE_descriptor import compute_BiCE_descriptor
from Edge_extraction import long_edge_extraction
import cv2
import random

img = cv2.imread("/Users/wang/Dev/hw/1112CG/final/out/bike.jpg")
edge = long_edge_extraction(img, (300, 300))
x = 60
y = 120
bias = 60
patch = edge[y : y + bias, x : x + bias]
cv2.imshow("My Image", patch)
# 按下任意鍵則關閉所有視窗
cv2.waitKey(0)
cv2.destroyAllWindows()

des = compute_BiCE_descriptor(patch)
permutation = list(range(len(des)))
random.shuffle(permutation)
hash_value = minhash(des, permutation)
print(hash_value)
