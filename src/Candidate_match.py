import mysql.connector
from sqlalchemy import create_engine
from multiprocessing import set_start_method, Pool
import pandas as pd
from pandasql import sqldf
import cv2

from Img2sketches import img2sketches

histogram = [[0 for i in range(81)] for i in range(12060)]


def sketch_cmp(sketch1, sketch2):
    count = 0
    for i in range(len(sketch1)):
        for j in range(3):
            if sketch1[i][j] == sketch2[i][j]:
                count += 1
    return count


def patch_match(patch, id, df):
    sketch_match = df.loc[df["ID"] == id]
    print(sketch_match.head())


def candidate_match(img, df):
    sketches = img2sketches(img, 480, 96, 25)

    patch_match(sketches[0], 0, df)
    return 0


if __name__ == "__main__":
    connection = create_engine(
        "mysql+pymysql://root:password@localhost:3306/SHADOWDRAW", echo=False
    )
    query = "SELECT * FROM SKETCH"
    sketches_in_db = pd.read_sql(query, connection)
    # sketches_in_db = False

    img_path = "../images/" + "cat" + "/" + "n02123045_127.JPEG"
    img = cv2.imread(img_path)
    candidates = candidate_match(img, sketches_in_db)
    # print(candidates)
