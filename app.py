
from flask import Flask, render_template

app = Flask(__name__)

files = [
    {"name": "فایل PDF نمونه", "url": "https://drive.google.com/uc?export=download&id=FILE_ID1"},
    {"name": "ویدیو نمونه", "url": "https://drive.google.com/uc?export=download&id=FILE_ID2"},
    {"name": "عکس نمونه", "url": "https://drive.google.com/uc?export=download&id=FILE_ID3"}
]

@app.route("/")
def index():
    return render_template("index.html", files=files)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)

