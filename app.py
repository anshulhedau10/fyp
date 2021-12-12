from flask import Flask, render_template, request, redirect, url_for, send_file
from werkzeug.utils import secure_filename
import os
import ml_logic
from flask_mail import Mail, Message
import pickle
from pathlib import Path

base_path = Path(__file__)

app = Flask(__name__)

# configuration
app.config['DEBUG'] = False
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'finalyrproject001@gmail.com'
app.config['MAIL_PASSWORD'] = '9424772300'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_DEFAULT_SENDER'] = ('FIGHT COVID', 'finalyrproject001@gmail.com')
app.config['MAIL_ASCII_ATTACHMENTS'] = True
app.config['MAIL_MAX_EMAILS'] = 2
app.config['MAIL_SUPPRESS_SEND '] = False
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.static_folder = 'static'
app.config['UPLOAD_PATH'] = "static/dataset/"
app.config['UPLOAD_EXTENSIONS'] = [".csv"]

mail = Mail(app)

users = [['18010032@ycce.in', 'Anshul Hedau'], ['hatwarprajwal@gmail.com', 'Prajwal Hatwar'], ['shreyasrajurkar13@gmail.com', 'Shreyas Rajurkar'], ['julikhobragade923@gmail.com', 'Juli Khobragade']]#, ['ganeshyenurkar@gmail.com', 'Ganesh Yenurkar']]
result_filename = "result.csv"
csv_file_format_filename = "csv_file_format.csv"
input_data_filename = "input_data.csv"
to_send_email_list = [] #format: [['email', 'name'], ... ]

ROCAUC = pickle.load(open((base_path/"../pickle_global/roc_auc.pkl").resolve(),'rb'))
confusionMatrix = pickle.load(open((base_path/"../pickle_global/cnf_matrix.pkl").resolve(),'rb'))
report = pickle.load(open((base_path/"../pickle_global/report.pkl").resolve(),'rb'))
accuracy = pickle.load(open((base_path/"../pickle_global/accuracy.pkl").resolve(),'rb'))

@app.route("/") #render home page
def index():
    return render_template("index.html")

@app.route("/about") #render about page
def about():
    return render_template("about.html")

@app.route("/", methods=["POST"]) #upload file
def upload_file():
    global ROCAUC, confusionMatrix, accuracy, to_send_email_list
    uploaded_file = request.files["file"]
    filename = secure_filename(uploaded_file.filename)

    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in app.config["UPLOAD_EXTENSIONS"]:
            return "File type not supported. Please upload csv file."
        uploaded_file.save(os.path.join(app.config["UPLOAD_PATH"], input_data_filename))
        print("Saved file successfully")
        to_send_email_list = ml_logic.machinelearning() #returning list of emails of patients with high_risk=="YES"
        #print(to_send_email_list[:5])
        return redirect("/downloadfile/") 
    else:
        return redirect(url_for('index'))
    
@app.route("/downloadfile/", methods=["GET"]) #render download page
def download_file():
    return render_template("download.html", ROCAUC = ROCAUC, confusionMatrix = confusionMatrix, accuracy=accuracy)

@app.route("/return-file/") #download result file
def return_files_tut():
    result_filepath = os.path.join(app.config["UPLOAD_PATH"], result_filename)
    try:
        return send_file(result_filepath, as_attachment=True, download_name="ResultFile.csv")
    except:
        return "Either the file is already downloaded or the file is not available! Please try again :(."
    

@app.route("/downloadcsv/", methods=["GET"]) #download csv file format
def downloadcsv():
    csvfile = os.path.join(app.config["UPLOAD_PATH"], csv_file_format_filename) 
    try:
        return send_file(csvfile, as_attachment=True)
    except FileNotFoundError:
        return "csv file format not available!"

@app.route("/sendemail/") #send email
def sendemail():
    global to_send_email_list, users
    if len(to_send_email_list)==0:
        return "Email already sent!"

    with mail.connect() as conn:
        for user in to_send_email_list:
            message = "Hello " + str(user[1])
            subject = "Fightcovid COVID-19 status."
            msg = Message(body=message, subject=subject, recipients=[user[0]])
            msg.html = render_template('email.html', name = user[1], email = user[0])
            with app.open_resource(os.path.join(app.config["UPLOAD_PATH"], result_filename)) as fp:
                msg.attach("ResultFile.csv", "text/csv", fp.read())

            with app.open_resource(os.path.join("static/images/graphs", user[0]+".png")) as fp:
                msg.attach("HealthReport.png", "image/png", fp.read())
            
            conn.send(msg)
    
    #to_send_email_list = []
    #users = []
    
    for file in os.scandir("static/images/graphs"):
        try:
            os.remove(file.path)
        except:
            print("Folder encountered")
    return "Sent"
    
#@app.after_response
#def maintenance():
    

    
    
if __name__ == "__main__":
    app.run()