from flask import Flask, request, send_file
from PIL import Image
from sqlalchemy import create_engine
import pandas as pd
import numpy as np
from io import BytesIO

from Candidate_match import candidate_match
from Add_image import add_image


app = Flask(
    __name__,
    static_url_path="/python",
    static_folder="static",
    template_folder="templates",
)

connection = create_engine(
    "mysql+pymysql://root:password@localhost:3306/SHADOWDRAW", echo=False
)
query = "SELECT * FROM SKETCH"
sketches_in_db = pd.read_sql(query, connection)


@app.route("/")
def root():
    return "draw"


@app.route("/get_background", methods=["POST"])
def get_background():
    image_file = request.files["canvasImage"]
    image = Image.open(image_file)
    # Process the image as needed
    candidates = candidate_match(np.array(image), sketches_in_db)
    shadow_img = add_image(candidates)
    mod_img = Image.fromarray(shadow_img)

    # Save the modified image to a BytesIO object
    image_io = BytesIO()
    mod_img.save(image_io, "JPEG")
    image_io.seek(0)

    # Return the modified image as a response
    return send_file(image_io, mimetype="image/jpeg")


if __name__ == "__main__":
    # app.run(debug=True)
    app.run()
