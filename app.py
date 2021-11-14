from flask import Flask, render_template, request, redirect, url_for, abort, send_file
from werkzeug.utils import secure_filename
import os
import ml_logic

app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True
app.static_folder = 'static'
app.config['UPLOAD_PATH'] = "static/dataset/"
app.config['UPLOAD_EXTENSIONS'] = ['.csv']

result_filename = "result.csv"

@app.route("/")
def index():

    # Render HTML
    return render_template("index.html")

@app.route("/", methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in app.config['UPLOAD_EXTENSIONS']:
            abort(400)
        uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
        print("Saved file successfully")
        ml_logic.machinelearning()
        return redirect('/downloadfile/'+ result_filename)
        
    else:
        return render_template("warning.html")
    return redirect(url_for('index'))


@app.route("/downloadfile/<result_filename>", methods=["GET"])
def download_file(result_filename):
    return render_template('download.html',value=result_filename)

@app.route("/return-files/<result_filename>")
def return_files_tut(result_filename):
    file_path = os.path.join(app.config['UPLOAD_PATH'], result_filename)
    return send_file(file_path, as_attachment=True, attachment_filename="ResultFile.csv")

if __name__ == "__main__":
    app.run()