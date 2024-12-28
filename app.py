from flask import Flask, render_template, request, send_file
from PIL import Image
import os

app = Flask(__name__)
UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/compress", methods=["POST"])
def compress_image():
    if "image" not in request.files:
        return "No file uploaded", 400

    uploaded_file = request.files["image"]
    if uploaded_file.filename == "":
        return "No file selected", 400

    # Get compression quality from the form
    try:
        quality = int(request.form.get("quality", 30))  # Default to 30 if not provided
        if not (1 <= quality <= 100):
            raise ValueError("Quality out of range")
    except ValueError:
        return "Invalid compression quality. Please enter a number between 1 and 100.", 400

    # Save uploaded image
    input_path = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
    uploaded_file.save(input_path)

    # Compress the image
    output_path = os.path.join(UPLOAD_FOLDER, f"compressed_{uploaded_file.filename}")
    with Image.open(input_path) as img:
        img.save(output_path, "JPEG", quality=quality)  # Use user-provided quality

    return send_file(output_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
