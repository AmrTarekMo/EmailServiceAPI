import sendgrid
import time
import requests
from flask import Flask , request , render_template , redirect , url_for
from email import utils

app = Flask(__name__)

#Update Your API Keys
SendGridKEY = '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'
MailGunDomain = 'amr.domain.com'
MailGunKey = 'fcaae0c2179e4a72737ea9743ecd170d-9525e19d-e687ff51'

def sendGrid(fromEmail , toEmail , subject , message , _time):
    sg = sendgrid.SendGridAPIClient(apikey=SendGridKEY)
    data = {
        "personalizations": [
            {
                "to": [
                    {
                        "email": toEmail
                    }
                ],
                "subject": subject,
                "send_at": int(time.time()) + _time
            }
        ],
        "from": {
            "email": fromEmail
        },
        "content": [
            {
                "type": "text/plain",
                "value": message
            }
        ]
    }
    response = sg.client.mail.send.post(request_body = data)
    return response.status_code

def mailGun(fromEmail , toEmail , subject , message , _time):
    _time = utils.formatdate(time.time() + _time)
    return requests.post("https://api.mailgun.net/v3/%s/messages" % MailGunDomain,
                         auth=("api", MailGunKey),
                         data={"from": "<%s>" % fromEmail,
                               "to": toEmail,
                               "subject": subject,
                               "text": message,
                               "o:deliverytime": _time})

@app.route('/' , methods=['GET' , 'POST'])
def send():
    if request.method == 'POST':

        # Takes schedule date ( Not Required ) then it sends the Email after the given time from local time
        time = 0
        if request.form['day'] :
            time += int(request.form['day']) * 86400
        if request.form['hrs'] :
            time += int(request.form['hrs']) * 3600
        if request.form['min'] :
            time += int(request.form['min']) * 60

        # Try SendGrid if it failed , it will try mailGun
        try:
            sendGrid(request.form['fromEmail'],request.form['toEmail'],request.form['subject'],request.form['message'],time)
        except:
            mailGun(request.form['fromEmail'],request.form['toEmail'],request.form['subject'],request.form['message'],time)

        return redirect(url_for('send'))
    else :
        return render_template("index.html")

if __name__ == '__main__':
    app.run()
