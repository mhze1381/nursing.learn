import os
from flask import Flask, render_template


app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/<page>")
def show_page(page):
    page = page.lower()  # همه حروف کوچیک بشه
    file_path = os.path.join(app.template_folder, f"{page}.html")
    if os.path.exists(file_path):
        return render_template(f"{page}.html")
    else:
        return "صفحه مورد نظر یافت نشد."

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)

