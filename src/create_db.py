import mysql.connector
import os
from Min_hash import minhash
from BiCE_descriptor import compute_BiCE_descriptor
from Edge_extraction import long_edge_extraction, canny
import cv2
import random

from multiprocessing import set_start_method, Pool


# 建立数据库连接
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="SHADOWDRAW",
)
# 创建游标对象
cursor = connection.cursor()
query = "SELECT `SEED1`, `SEED2`, `SEED3` FROM `HASH_FUNC`"
cursor.execute(query)
seeds = cursor.fetchall()
cursor.close()
connection.close()

# pool = Pool()


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


def img2sketches(img, img_size=300, patch_size=60, over_lap=0.5):
    edge = canny(img, (img_size, img_size))
    # edge = long_edge_extraction(img, (img_size, img_size))

    patchs = [
        edge[y : y + patch_size, x : x + patch_size]
        for y in range(0, img_size - patch_size + 1, int(patch_size * over_lap))
        for x in range(0, img_size - patch_size + 1, int(patch_size * over_lap))
    ]
    result = pool.map(patch2sketches, patchs)
    return result


if __name__ == "__main__":
    set_start_method("fork", True)
    pool = Pool()
    categories = os.listdir("../images")
    for cate in categories:
        if cate != "cat":
            break
        curdir = "../images/" + cate + "/"
        img_names = list(map(lambda x: curdir + x, os.listdir(curdir)))
        for img_name in img_names:
            img = cv2.imread(img_name)
            sketchs = img2sketches(img)
            break


# # 插入 IMG 数据
# img_data = [("image1.jpg", "cat1"), ("image2.jpg", "cat2"), ("image3.jpg", "cat1")]
# img_insert_query = "INSERT INTO IMG (FNAME, CAT) VALUES (%s, %s)"
# cursor.executemany(img_insert_query, img_data)

# # 插入 SKETCH 数据
# sketch_data = [
#     ("image1.jpg", 1, 10, 20, 30),
#     ("image1.jpg", 2, 15, 25, 35),
#     ("image2.jpg", 1, 12, 22, 32),
# ]
# sketch_insert_query = "INSERT INTO SKETCH (FNAME, `INDEX`, VALUE1, VALUE2, VALUE3) VALUES (%s, %s, %s, %s, %s)"
# cursor.executemany(sketch_insert_query, sketch_data)

# # 插入 HASH_FUNC 数据
# hash_func_data = [(1, 123, 456, 789), (2, 987, 654, 321)]
# hash_func_insert_query = (
#     "INSERT INTO HASH_FUNC (`INDEX`, SEED1, SEED2, SEED3) VALUES (%s, %s, %s, %s)"
# )
# cursor.executemany(hash_func_insert_query, hash_func_data)

# # 提交事务
# connection.commit()

# # 关闭游标和数据库连接
# cursor.close()
# connection.close()
