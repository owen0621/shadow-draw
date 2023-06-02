from sqlalchemy import create_engine
from multiprocessing import set_start_method, Pool
import pandas as pd
import cv2

from Img2sketches import img2sketches


def patch_match(argv):
    patch = argv[0]
    Id = argv[1]
    df = argv[2]
    df = df.loc[df["ID"] == Id]
    total_match = []
    for index in range(20):
        patch_match1 = df.loc[
            (df["INDEX"] == index) & (df["VALUE1"] == patch[index][0]),
            ["FNAME", "ID", "INDEX"],
        ]
        patch_match2 = df.loc[
            (df["INDEX"] == index) & (df["VALUE2"] == patch[index][1]),
            ["FNAME", "ID", "INDEX"],
        ]
        patch_match3 = df.loc[
            (df["INDEX"] == index) & (df["VALUE3"] == patch[index][2]),
            ["FNAME", "ID", "INDEX"],
        ]
        total_match.append(patch_match1)
        total_match.append(patch_match2)
        total_match.append(patch_match3)
    total_match = pd.concat(total_match)
    # print(total_match)
    return total_match


def candidate_match(img, df):
    cv2.imwrite("debug.jpg", img)
    sketches = img2sketches(img, 480, 96, 25)
    # patch_match((sketches[100], 100//4, df))
    set_start_method("fork", True)
    pool = Pool()
    id_arr = [i // 4 for i in range(len(sketches))]
    df_arr = [df for _ in range(len(sketches))]
    total_matches = pool.map(patch_match, zip(sketches, id_arr, df_arr))
    pool.close()
    total_matches = pd.concat(total_matches).groupby("FNAME")
    return total_matches.size().sort_values(ascending=False).to_dict()


if __name__ == "__main__":
    connection = create_engine(
        "mysql+pymysql://root:password@localhost:3306/SHADOWDRAW", echo=False
    )
    query = "SELECT * FROM SKETCH"
    sketches_in_db = pd.read_sql(query, connection)

    img_path = "../images/" + "cat" + "/" + "n02123045_712.JPEG"
    img = cv2.imread(img_path)
    candidates = candidate_match(img, sketches_in_db)
    print(candidates)
