import sendgrid
import time
import requests
from flask import Flask , request , render_template , redirect , url_for

app = Flask(__name__)

def sendGrid(fromEmail , toEmail , subject , message , _time):
    sg = sendgrid.SendGridAPIClient('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')
    data = {
        "personalizations": [
            {
                "to": [
                    {
                        "email": toEmail
                    }
                ],
                "subject": subject,
                "send_at": time.time() + _time
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
    return requests.post("https://api.mailgun.net/v3/%s/messages" % "amr.domain.com",
                         auth=("api", "fcaae0c2179e4a72737ea9743ecd170d-9525e19d-e687ff51"),
                         data={"from": "<%s>" % fromEmail,
                               "to": toEmail,
                               "subject": subject,
                               "text": message,
                               "o:deliverytime": _time})

@app.route('/' , methods=['GET' , 'POST'])
def send():
    if request.method == 'POST':
        time = 0
        if request.form['day'] :
            time += int(request.form['day']) * 86400
        if request.form['hrs'] :
            time += int(request.form['hrs']) * 3600
        if request.form['min'] :
            time += int(request.form['min']) * 60
        try:
            sendGrid(request.form['fromEmail'],request.form['toEmail'],request.form['subject'],request.form['message'],time)
        except:
            mailGun(request.form['fromEmail'],request.form['toEmail'],request.form['subject'],request.form['message'],time)

        return redirect(url_for('send'))
    else :
        return render_template("index.html")



if __name__ == '__main__':
    app.secret_key = "password"
    app.debug = True
    app.run()
