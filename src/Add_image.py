from sqlalchemy import create_engine
import pandas as pd
import numpy as np
import cv2

from Candidate_match import candidate_match


def add_image(candidates):
    weights = list(candidates.values())[:8]
    total_weight = sum(weights)
    weights = list(map(lambda x: x / total_weight, weights))
    top_eight = list(candidates.keys())[:8]

    imgdir = "../images-copy/"
    img_pathes = list(map(lambda x: imgdir + x, top_eight))
    imgs = list(map(lambda x: cv2.imread(x, cv2.IMREAD_GRAYSCALE), img_pathes))

    # shadow = sum(list(map(lambda img, weight: img * weight, imgs, weights)))
    shadow = np.zeros_like(imgs[0])
    # 逐張圖片進行加權
    for img, weight in zip(imgs, weights):
        weighted_img = cv2.multiply(img, weight)
        shadow = cv2.add(shadow, weighted_img)
    return shadow


if __name__ == "__main__":
    connection = create_engine(
        "mysql+pymysql://root:password@localhost:3306/SHADOWDRAW", echo=False
    )
    query = "SELECT * FROM SKETCH"
    sketches_in_db = pd.read_sql(query, connection)

    img_path = "../images/" + "cat" + "/" + "n02123045_712.JPEG"
    img = cv2.imread(img_path)
    candidates = candidate_match(img, sketches_in_db)

    shadow_img = add_image(candidates)

    cv2.imshow("addWeighted", shadow_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
