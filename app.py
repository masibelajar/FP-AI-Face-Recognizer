from flask import Flask, render_template, request
from deepface import DeepFace
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        file1 = request.files.get('img1')
        file2 = request.files.get('img2')

        if not file1 or not file2 or file1.filename == '' or file2.filename == '':
            result = {"error": "❗ Harap upload dua file gambar terlebih dahulu."}
            return render_template("index.html", result=result)

        path1 = os.path.join(app.config['UPLOAD_FOLDER'], file1.filename)
        path2 = os.path.join(app.config['UPLOAD_FOLDER'], file2.filename)

        file1.save(path1)
        file2.save(path2)

        try:
            verification = DeepFace.verify(img1_path=path1, img2_path=path2, model_name='Facenet')
            verified = verification["verified"]
            distance = verification["distance"]
            threshold = verification["threshold"]
            confidence = round((1 - distance / threshold) * 100, 2) if verified else 0.0

            result = {
                "verified": verified,
                "distance": distance,
                "confidence": confidence,
                "img1": file1.filename,
                "img2": file2.filename
            }
        except Exception as e:
            result = {"error": str(e)}

    return render_template("index.html", result=result)

if __name__ == '__main__':
    app.run(debug=True)
