from flask import Flask, render_template, request, current_app
from flask_mysqldb import MySQL
import smtplib
import ssl
import dotenv
import os
import newsapi
from apscheduler.schedulers.background import BackgroundScheduler
import time


'''-----------------------initialising the app----------------------------------'''
app= Flask(__name__)


dotenv.load_dotenv()
db= os.getenv('db')
#database config
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = db

mysql = MySQL(app)

'''-------------------------fetching the email list and sending email-------------------'''
def getemlist():
    with app.app_context():
        cur= mysql.connection.cursor()
        query= ('select Email from email_list')
        cur.execute(query)
        data= cur.fetchall()
        cur.close()

    emlist= []
    for ele in data:
        emlist.append(ele[0])

    return emlist

port= 465
pwd= os.getenv('pwd')
context = ssl.create_default_context()
smtp_server= 'smtp.gmail.com'
sender_email= 'newsnest99@gmail.com'

def senddailynews():

    em_list= getemlist()
    SUBJECT= 'Your daily news dose'
    title_list= newsapi.get_news_title()
    source_list= newsapi.get_news_source()
    TEXT=''
    for i in range(5):
        TEXT= TEXT+ title_list[i]+'\n'+' Source: '+source_list[i]+'\n'

    message = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)
    msg= message.encode('utf-8')
    for ele in em_list:
        with smtplib.SMTP_SSL(smtp_server,port,context=context) as server:
            server.login(sender_email,pwd)
            server.sendmail(sender_email,ele,msg)

'''-------------------------------------------------------------------------------'''

'''---------------Scheduling email at daily 6 in the morning----------------------'''
sched= BackgroundScheduler(daemon=True)
sched.add_job(senddailynews, 'cron', day_of_week='mon-sun', hour='06', minute='00', timezone='Asia/Kolkata')
sched.start()


'''----------------------------app routes-----------------------------------------'''
@app.route("/")
def main():
    return render_template('home.html')

@app.route("/thankyou", methods=['GET','POST'])
def thankyou():
    if request.method =='GET':
        return render_template('home.html')

    if request.method == 'POST':
        email= request.form['email']
        cur= mysql.connection.cursor()
        cur.execute('''INSERT into email_list(Email) VALUES(%s)''',(email,))
        mysql.connection.commit()
        cur.close()
        return render_template('thankyou.html')



'''-----------------------------Running the app--------------------------------------'''
if __name__ == "__main__":
    app.run(debug=True)
    #schedule_mail('20:20')



