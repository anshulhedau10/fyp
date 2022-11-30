from flask import Flask, render_template, request, redirect, url_for, send_file
from matplotlib.style import use
# from numpy import cov  
# import pandas as pd 
from werkzeug.utils import secure_filename
import os
import ml_logic_rf, ml_logic_xgb
from flask_mail import Mail, Message
import pickle
from pathlib import Path
import threading
import requests
import bs4

base_path = Path(__file__)

app = Flask(__name__)

# configuration
app.config['DEBUG'] = False
app.config['MAIL_SERVER']='smtp.office365.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'anshul.demo@outlook.com'
app.config['MAIL_PASSWORD'] = 'Anshul@12345'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_DEFAULT_SENDER'] = ('FIGHT COVID', 'anshul.demo@outlook.com')
app.config['MAIL_ASCII_ATTACHMENTS'] = True
app.config['MAIL_MAX_EMAILS'] = 2
app.config['MAIL_SUPPRESS_SEND '] = False
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.static_folder = 'static'
app.config['UPLOAD_PATH'] = 'static/dataset/'
app.config['UPLOAD_EXTENSIONS'] = ['.csv']

mail = Mail(app)

users = [['18010032@ycce.in', 'Anshul Hedau']]#, ['hatwarprajwal@gmail.com', 'Prajwal Hatwar'], ['shreyasrajurkar13@gmail.com', 'Shreyas Rajurkar'], ['julikhobragade923@gmail.com', 'Juli Khobragade'], ['ganeshyenurkar@gmail.com', 'Ganesh Yenurkar']]
result_filename = 'result.csv'
csv_file_format_filename = 'csv_file_format.csv'
input_data_filename = 'input_data.csv'
to_send_email_list = [] #format: [['email', 'name'], ... ]

ROCAUC = pickle.load(open((base_path/'../pickle_global/xgb_roc_auc.pkl').resolve(),'rb'))
confusionMatrix = pickle.load(open((base_path/'../pickle_global/xgb_cnf_matrix.pkl').resolve(),'rb'))
report = pickle.load(open((base_path/'../pickle_global/xgb_report.pkl').resolve(),'rb'))
accuracy = pickle.load(open((base_path/'../pickle_global/xgb_accuracy.pkl').resolve(),'rb'))

@app.route('/') #render home page
def index():
    return render_template('index.html')

@app.route('/about') #render about page
def about():
    return render_template('about.html')

@app.route('/<int:formNo>', methods=['POST']) #upload file
def upload_file(formNo):
    global to_send_email_list

    if formNo == 1:
        uploaded_file = request.files['file']
        filename = secure_filename(uploaded_file.filename)

        if filename != '':
            file_ext = os.path.splitext(filename)[1]
            
            if file_ext not in app.config['UPLOAD_EXTENSIONS']:
                return 'File type not supported. Please upload csv file.'

            uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], input_data_filename))
            print('Saved file successfully')
            to_send_email_list = ml_logic_xgb.machinelearning1() #returning list of emails of patients with high_risk=='YES'
            
            return redirect('/downloadfile') 
        else:
            return redirect(url_for('index'))
        
    elif formNo == 2:

        to_send_email_list = ml_logic_xgb.machinelearning2()
        print("Printing to send email list: ")
        print(to_send_email_list)
        return redirect('/downloadfile') 
    

@app.route('/downloadfile', methods=['GET']) #render download page
def download_file():
    global ROCAUC, confusionMatrix, accuracy
    # Calling maintenance function to clear graphs after 5 mins
    timer = threading.Timer(5*60.0, maintenance)
    timer.start()

    return render_template('download.html', ROCAUC = ROCAUC, confusionMatrix = confusionMatrix, accuracy=accuracy)


@app.route('/return-file') #download result file
def return_files_tut():
    result_filepath = os.path.join(app.config['UPLOAD_PATH'], result_filename)
    try:
        return send_file(result_filepath, as_attachment=True, download_name='ResultFile.csv')
    except:
        return 'Timeout! Please try again :(.'
    

@app.route('/downloadcsv/', methods=['GET']) #download csv file format
def downloadcsv():
    csvfile = os.path.join(app.config['UPLOAD_PATH'], csv_file_format_filename) 
    try:
        return send_file(csvfile, as_attachment=True)
    except:
        return 'csv file format is not available!'

@app.route('/covid_stats') #display covid stats
def covid_stats():
    active, discharged, deaths, vaccinated, updatedOn = '', '', '', '', ''

    URL = 'https://www.mohfw.gov.in/'
    response = requests.get(URL).content
    soup = bs4.BeautifulSoup(response, 'html.parser')

    stats_section = soup.findAll('section', {'id':'site-dashboard'})
    strong_list = stats_section[0].find_all('strong')
    for ele in strong_list[2]:
        if type(ele) == bs4.element.NavigableString:
            active  = str(ele)
            print(active)
            break

    for ele in strong_list[5]:
        if type(ele) == bs4.element.NavigableString:
            discharged = str(ele)
            print(discharged)
            break

    for ele in strong_list[8]:
        if type(ele) == bs4.element.NavigableString:
            deaths = str(ele)
            print(deaths)
            break

    vacc_stats = soup.findAll('span', {'class':'coviddata'})
    for ele in vacc_stats[0]:
        if type(ele) == bs4.element.NavigableString:
            vaccinated = str(ele)
            print(vaccinated)
            break
    
    updatedOn_stats = stats_section[0].find_all('div', {'class':'col-xs-12'})
    updatedOn_stats1 = updatedOn_stats[0].find_all('h5')
    t = str((list(updatedOn_stats1))[0])
    t = t.replace('<h5>', '')
    t = t.replace('</h5>', '')
    t = t.replace('<br/>', '')
    t = t.replace('<span>', '')
    t = t.replace('</span>', '')
    t = t.replace('(↑↓ Status change since yesterday)', '')
    updatedOn = t

    return render_template('covid_stats.html', active = active, discharged = discharged, deaths = deaths, vaccinated = vaccinated, updatedOn = updatedOn)


@app.route('/sendemail/') #send email
def sendemail():
    global to_send_email_list, users
    if len(to_send_email_list)==0:
        return 'There are no high-risk patients. Go back to homepage.!'

    with mail.connect() as conn:
        for user in to_send_email_list:
            message = 'Hello ' + str(user[1])
            subject = 'Fightcovid COVID-19 status.'
            msg = Message(body=message, subject=subject, recipients=[user[0]])
            msg.html = render_template('email.html', name = user[1], email = user[0])

            try:
                with app.open_resource(os.path.join(app.config['UPLOAD_PATH'], result_filename)) as fp:
                    msg.attach('ResultFile.csv', 'text/csv', fp.read())

                with app.open_resource(os.path.join('static/images/graphs', user[0]+'.png')) as fp:
                    msg.attach('HealthReport.png', 'image/png', fp.read())
            
            except:
                return 'Please try again!'
            
            # change message ID
            msg.msgId = msg.msgId.split('@')[0] + '@short_string'  # for instance your domain name
            
            #send
            conn.send(msg)
    

    
    #to_send_email_list = []
    #users = []
    
    # Clearing out graph images
    # for file in os.scandir('static/images/graphs'):
    #     try:
    #         os.remove(file.path)
    #     except:
    #         print('Folder encountered')
    
    return 'Sent'

    
    
#@app.after_response

def maintenance():
    # Clearing out graph images
    for file in os.scandir('static/images/graphs'):
        try:
            os.remove(file.path)
        except:
            pass

    

    
    
if __name__ == '__main__':
    app.run(debug=False)