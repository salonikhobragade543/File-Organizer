from flask import Flask, render_template, request, redirect, url_for, flash
from organizer import organize_files
import os, datetime, werkzeug

app = Flask(__name__)
app.secret_key = "change-me"

# Max file upload size = 16MB
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        folder = request.form.get("folder")
        folder = os.path.abspath(folder)

        if not folder or not os.path.isdir(folder):
            flash("❌ Invalid folder path. Please enter a valid directory.", "danger")
            return redirect(url_for("home"))

        uploaded_files = request.files.getlist("files[]")
        saved_files = 0
        uploaded_file_names = []

        for file in uploaded_files:
            if file and file.filename:
                filename = werkzeug.utils.secure_filename(file.filename)
                try:
                    save_path = os.path.join(folder, filename)
                    file.save(save_path)
                    uploaded_file_names.append(filename)
                    saved_files += 1
                except Exception as e:
                    flash(f"Error saving {filename}: {e}", "danger")

        start = datetime.datetime.now()
        moved, total = organize_files(folder)
        elapsed = (datetime.datetime.now() - start).total_seconds()

        if uploaded_file_names:
            flash(f"📦 Uploaded: {', '.join(uploaded_file_names)}", "info")

        flash(f"✅ Uploaded {saved_files} file(s). Organized {moved}/{total} files in {elapsed:.2f}s", "success")
        return redirect(url_for("home"))

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
