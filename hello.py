from flask import Flask , render_template , request
import flask
from PIL import Image
import base64
import urllib
import numpy as np
import face_recognition
import sqlfn

app = Flask(__name__)


classes = ['madhavan' , 'madhaesh' , 'kavin' , 'swami']

@app.route('/' , methods=['GET', 'POST'])
def index():

    if flask.request.method == 'POST':

        f = request.form.get("text")

        with urllib.request.urlopen(f) as response:
            data = response.read()

        with open('hi.jpg', "wb") as f:
            f.write(data)
 
        madhavan_image = face_recognition.load_image_file("madhavan1.jpg")
        madhaesh_image = face_recognition.load_image_file("madhaesh1.jpg")
        kavin_image = face_recognition.load_image_file("kavin1.jpg")
        swaminath_image = face_recognition.load_image_file("swaminath1.jpg")
        
        madhavan_encoding = face_recognition.face_encodings(madhavan_image)[0]
        madhaesh_encoding = face_recognition.face_encodings(madhaesh_image)[0]
        kavin_encoding = face_recognition.face_encodings(kavin_image)[0]
        swaminath_encoding = face_recognition.face_encodings(swaminath_image)[0]
        
        known_encodings = [madhavan_encoding , madhaesh_encoding , kavin_encoding , swaminath_encoding]
        
        unknown_filename = "hi.jpg"
        unknown_image = face_recognition.load_image_file(unknown_filename)
        unknown_encoding = face_recognition.face_encodings(unknown_image)[0]
        
        results = face_recognition.face_distance(known_encodings , unknown_encoding)

        
        out = '<h2>IMAGE DISTANCES</h2>'

        for i in range(len(results)):
            x = float(results[i])
            out += classes[i] + ' : ' + str("%.8f" % (x)) + '<br>'

        out += '<br><br><br><h2 STYLE="text-transform:uppercase">' + classes[np.argmin(results)] + " has been marked as present for today</h2>"

        sqlfn.add_date()
        sqlfn.mark_present(classes[np.argmin(results)])
        
        out += '<br><button type="button" onclick="window.location.href=\'/\';">Back</button>'
        out += '<br><button type="button" onclick="window.location.href=\'attnhistory\';">Display Attendance History</button>'

        return out

    else:

        return render_template('index.html')

@app.route('/attnhistory' , methods=['GET', 'POST'])
def attnhistory():

    h1 = sqlfn.columns()
    h2 = sqlfn.history()

    out = '<table border="1|0">'

    out += '<tr>'
    for i in h1:
        out += '<th>'+ str(i[0]) +'</th>'
    out += '</tr>'

    for i in h2:
        out += '<tr>'
        for j in i:
            out += '<td>'+ str(j) +'</td>'
        out += '</tr>'
    out += '</table>'

    out += '<br><button type="button" onclick="window.location.href=\'/\';">Back</button>'

    return out


if __name__ == '__main__':
    app.run()

