from flask import Flask,render_template,request,redirect,url_for,session,send_file
from io import BytesIO
from pytube import YouTube
app = Flask(__name__,template_folder='template', static_folder='assets')
app.config['SECRET_KEY'] = "abcdefghijklmnopqrstuvwxyz"
@app.route('/',methods=["GET","POST"])
def home():
    return render_template('index.html')
    
@app.errorhandler(404) 
def invalid_route(e): 
    return "Cari apa kak?"
    
@app.route('/result',methods=["GET","POST"])
def download():
    if request.method == "POST":
        session["link"] = request.form.get("url")
        try:
            vid = YouTube(session["link"])
            session["title"] = vid.title
            return render_template("result.html",title=vid.title)
        except:
            return render_template("error.html")
    return redirect(url_for('home'))

@app.route('/result/',methods=["GET","POST"])
def startDownload():
    if request.method == "POST":
        buffer = BytesIO()
        #audio = YouTube(session["link"]).streams.filter(only_audio=True)[4]       #for webm
        audio = YouTube(session["link"]).streams.filter(only_audio=True).first()   #for mp3
        #audio = YouTube(session["link"]).streams.get_by_itag(251)                 #for webm
        audio.stream_to_buffer(buffer)
        buffer.seek(0)
        #return send_file(buffer,as_attachment=True,download_name=session["title"]+"mp3",mimetype="audio/mpeg")
        #return send_file(buffer,as_attachment=True,download_name=session["title"],mimetype="audio/mp3")
        return send_file(buffer,as_attachment=True,download_name=session["title"]+".mp3",mimetype="audio/mp3")

    return redirect(url_for('home'))
if __name__ == "__main__":
    app.run(debug=True)
