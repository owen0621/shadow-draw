import mysql.connector
import random
import cv2
from multiprocessing import set_start_method, Pool

from Min_hash import minhash
from BiCE_descriptor import compute_BiCE_descriptor
from Edge_extraction import long_edge_extraction, canny

# create db connection
# connection = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     password="password",
#     database="SHADOWDRAW",
# )
# # create cursor and read seeds
# cursor = connection.cursor()
# query = "SELECT `SEED1`, `SEED2`, `SEED3` FROM `HASH_FUNC`"
# cursor.execute(query)
# seeds = cursor.fetchall()
# cursor.close()
# connection.close()

seeds = [
    (10, 20, 30),
    (11, 21, 31),
    (12, 22, 32),
    (13, 23, 33),
    (14, 24, 34),
    (15, 25, 35),
    (16, 26, 36),
    (17, 27, 37),
    (18, 28, 38),
    (19, 29, 39),
    (40, 50, 60),
    (41, 51, 61),
    (42, 52, 62),
    (43, 53, 63),
    (44, 54, 64),
    (45, 55, 65),
    (46, 56, 66),
    (47, 57, 67),
    (48, 58, 68),
    (49, 59, 69),
]


# convert a patch to sketches
def patch2sketches(patch):
    descriptor = compute_BiCE_descriptor(patch)
    sketches = []
    for seed in seeds:
        seed1, seed2, seed3 = seed
        permutation = list(range(len(descriptor)))
        random.seed(seed1)
        random.shuffle(permutation)
        hash1 = minhash(descriptor, permutation)
        permutation = list(range(len(descriptor)))
        random.seed(seed2)
        random.shuffle(permutation)
        hash2 = minhash(descriptor, permutation)
        permutation = list(range(len(descriptor)))
        random.seed(seed3)
        random.shuffle(permutation)
        hash3 = minhash(descriptor, permutation)

        sketches.append([hash1, hash2, hash3])
    return sketches


# convert a image to sketches
def img2sketches(img, img_size=300, patch_size=60, step=31):
    edge = canny(img, (img_size, img_size))
    # edge = long_edge_extraction(img, (img_size, img_size))

    patchs = [
        edge[x : x + patch_size, y : y + patch_size]
        for x in range(0, img_size - step + 1, step + 1)
        for y in range(0, img_size - step + 1, step + 1)
    ]
    set_start_method("fork", True)
    pool = Pool()
    result = pool.map(patch2sketches, patchs)
    pool.close()
    # print(seeds)
    return result


if __name__ == "__main__":
    img_path = "../images/" + "cat" + "/" + "n02123045_712.JPEG"
    img = cv2.imread(img_path)
    # img2sketches(img)
    print(img2sketches(img))
