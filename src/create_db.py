import mysql.connector
import os
import cv2
import random
from tqdm import tqdm
from multiprocessing import set_start_method, Pool

from Min_hash import minhash
from BiCE_descriptor import compute_BiCE_descriptor
from Edge_extraction import long_edge_extraction, canny
from Img2sketches import img2sketches

# create db connection
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="SHADOWDRAW",
)
# create cursor and read seeds
cursor = connection.cursor()
query = "SELECT `SEED1`, `SEED2`, `SEED3` FROM `HASH_FUNC`"
cursor.execute(query)
seeds = cursor.fetchall()
cursor.close()

if __name__ == "__main__":
    set_start_method("fork", True)
    pool = Pool()
    cursor = connection.cursor()

    img_size = 300
    patch_size = 60
    over_lap = 0.5
    coor = [
        (x, y)
        for y in range(0, img_size - patch_size + 1, int(patch_size * over_lap))
        for x in range(0, img_size - patch_size + 1, int(patch_size * over_lap))
    ]

    categories = os.listdir("../images")
    for cate in tqdm(categories):
        curdir = "../images/" + cate + "/"
        img_names = os.listdir(curdir)
        for img_name in tqdm(img_names):
            img_path = curdir + img_name
            img = cv2.imread(img_path)
            sketchs = img2sketches(img)
            # 插入 IMG 数据
            img_data = [(img_name, cate)]
            img_insert_query = "INSERT INTO IMG (FNAME, CATE) VALUES (%s, %s)"
            cursor.executemany(img_insert_query, img_data)
            # 插入 PATCH 数据
            patch_data = [
                (img_name, i, coor[i][0], coor[i][1]) for i in range(len(sketchs))
            ]
            patch_insert_query = (
                "INSERT INTO PATCH (FNAME, `ID`, DX, DY) VALUES (%s, %s, %s, %s)"
            )
            cursor.executemany(patch_insert_query, patch_data)
            # 插入 SKETCH 数据
            sketch_data = []
            for i in range(len(sketchs)):
                for j in range(len(sketchs[0])):
                    sketch_data.append(
                        (
                            img_name,
                            i,
                            j,
                            sketchs[i][j][0],
                            sketchs[i][j][1],
                            sketchs[i][j][2],
                        )
                    )
            sketch_insert_query = "INSERT INTO SKETCH (FNAME, `ID`, `INDEX`, `VALUE1`, `VALUE2`, `VALUE3`) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.executemany(sketch_insert_query, sketch_data)
            # 提交事务
            connection.commit()
    cursor.close()
    connection.close()
