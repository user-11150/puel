try:
    import flask
    del flask
except ImportError:
    import pip
    import os.path
    import sys
    import io

    print("loading")
    
    pip.main(["install", "-r", os.path.abspath(os.path.join(os.path.dirname(__file__), "requirements.txt"))])

from flask import Flask, redirect

app: Flask = Flask(__package__,
                   static_url_path="/",)
                   
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1

@app.route("/")
def index():
    return redirect("/index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0",
            port=2500,
            debug=True)
