from flask import Flask, render_template, request, redirect, url_for, send_file
from werkzeug.utils import secure_filename
import os
import ml_logic
from flask_mail import Mail, Message

app = Flask(__name__)
mail = Mail(app)

# configuration of mail
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'finalyrproject001@gmail.com'
app.config['MAIL_PASSWORD'] = '9424772300'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_DEFAULT_SENDER'] = 'finalyrproject001@gmail.com'
app.config['MAIL_ASCII_ATTACHMENTS'] = True
mail = Mail(app)

app.config["TEMPLATES_AUTO_RELOAD"] = True
app.static_folder = 'static'
app.config['UPLOAD_PATH'] = "static/dataset/"
app.config['UPLOAD_EXTENSIONS'] = [".csv"]

users = [['anshulhedau2001@gmail.com', 'Anshul Hedau'], ['hatwarprajwal@gmail.com', 'Prajwal Hatwar'], ['shreyasrajurkar13@gmail.com', 'Shreyas Rajurkar']]#, ['julikhobragade923@gmail.com', 'Juli Khobragade'], ['ganeshyenurkar@gmail.com', 'Ganesh Yenurkar']]
result_filename = "result.csv"
csv_file_format_filename = "csv_file_format.csv"
input_data_filename = "input_data.csv"
to_send_email_list = [] #format: [['email', 'name'], ... ]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/", methods=["POST"])
def upload_file():
    global to_send_email_list
    uploaded_file = request.files["file"]
    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in app.config["UPLOAD_EXTENSIONS"]:
            return "File type not supported. Please upload csv file."
        uploaded_file.save(os.path.join(app.config["UPLOAD_PATH"], filename))
        print("Saved file successfully")
        to_send_email_list = ml_logic.machinelearning() #returning list of emails of patients with high_risk=="YES"
        return redirect("/downloadfile/"+ result_filename) 
    else:
        return redirect(url_for('index'))
    
@app.route("/downloadfile/<result_filename>", methods=["GET"])
def download_file(result_filename):
    return render_template("download.html",value=result_filename)

@app.route("/return-files/<result_filename>")
def return_files_tut(result_filename):
    result_filepath = os.path.join(app.config["UPLOAD_PATH"], result_filename)
    input_data_filepath = os.path.join(app.config["UPLOAD_PATH"], input_data_filename)

    try:
        return send_file(result_filepath, as_attachment=True, download_name="ResultFile.csv")
    except:
        return "Either the file is already downloaded or the file is not available! Please visit homepage."
    

@app.route("/downloadcsv/", methods=["GET"])
def downloadcsv():
    csvfile = os.path.join(app.config["UPLOAD_PATH"], csv_file_format_filename) 
    try:
        return send_file(csvfile, as_attachment=True)
    except FileNotFoundError:
        return "csv file format not available!"

@app.route("/sendemail/")
def sendemail():
    global to_send_email_list, users
    if len(to_send_email_list)==0 or len(users)==0:
        return "Email already sent!"

    with mail.connect() as conn:
        for user in users:
            message = "Hello " + str(user[1])
            subject = "Fightcovid COVID-19 status."
            msg = Message(body=message, subject=subject, recipients=[user[0]])
            #msg.html = f"<h2>Hello { user[1] },</h2><h3><b>You have a high risk of COVID-19 based on your health condition.</b></h3><br><br><p>The result file is attached below.</p><br>--Thanks."
            msg.html = render_template('email.html', name = user[1])
            with app.open_resource(os.path.join(app.config["UPLOAD_PATH"], result_filename)) as fp:
                msg.attach("ResultFile.csv", "text/csv", fp.read())
            
            conn.send(msg)
    
    to_send_email_list.clear()
    users.clear()
    return "Sent"
    
if __name__ == "__main__":
    app.run()