from flask import Flask, redirect

app: Flask = Flask(__package__,
                   static_url_path="/",)
                   
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1

@app.route("/")
def index():
    return redirect("/index.html")

if __name__ == "__main__":
    app.run(host="127.0.0.1",
            port=2500,
            debug=True)
