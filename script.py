from flask import Flask, url_for, render_template, redirect, send_file, request, session
from pytube import YouTube
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = "!2345@abc"


@app.route('/',methods=['GET','POST'])





def index():
    if request.method == 'POST':
        session['link'] = request.form.get('url')
        x = session['link']
        if len(session['link']) == 0:
            return render_template("index.html")
        else:
            r = requests.get(x)
            if "Video unavailable" in r.text:
                return render_template('index.html')
            url = YouTube(session['link'])
            return render_template('see_video.html', url=url)
    return render_template('index.html')


@app.route('/see-video',methods=['GET','POST'])
def see_video():
    if request.method =='POST':
        url = YouTube(session['link'])
        itag = request.form.get('itag')
        video = url.streams.get_by_itag(itag)
        filename = video.download()
        return send_file(filename,as_attachment=True)
    return redirect(url_for('index'))

if __name__ =="__main__":
    app.run(debug=True)