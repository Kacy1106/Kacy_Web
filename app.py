import os
from flask import Flask, request, render_template, send_from_directory, redirect, url_for, flash
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "yoursecret"   # 用于 flash 提示

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# -------------------------
# 允许的文件格式
# -------------------------
ALLOWED_EXTENSIONS = {
    "png", "jpg", "jpeg", "gif", "pdf", "doc", "docx", "ppt", "pptx",
    "xls", "xlsx", "txt", "mp3", "mp4", "cdr", "zip", "7z", "rar"
}

# -------------------------
# 最大单文件 50MB
# -------------------------
app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 * 1024  # 50MB
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def allowed_file(filename):
    return "." in filename and \
           filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.errorhandler(413)
def too_large(e):
    flash("❌ 上传失败：文件超过 50MB 限制！")
    return redirect(url_for("index"))


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "file" not in request.files:
            flash("❌ 未选择文件")
            return redirect(url_for("index"))

        file = request.files["file"]

        if file.filename == "":
            flash("❌ 文件名为空")
            return redirect(url_for("index"))

        if allowed_file(file.filename):
            filename = secure_filename(file.filename)
            save_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)

            file.save(save_path)
            flash("✅ 上传成功！")
            return redirect(url_for("index"))
        else:
            flash("❌ 不支持的文件格式！")
            return redirect(url_for("index"))

    file_list = os.listdir(UPLOAD_FOLDER)
    return render_template("index.html", files=file_list)


@app.route("/uploads/<path:filename>")
def download_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=False)


@app.route("/delete/<path:filename>")
def delete_file(filename):
    try:
        os.remove(os.path.join(UPLOAD_FOLDER, filename))
        flash("🗑 文件已删除")
    except:
        flash("❌ 删除失败")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
