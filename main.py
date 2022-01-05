from flask import Flask, render_template
from os import path

path = path.dirname(__file__)
print(path)
app = Flask(__name__, static_folder=path + "/assets", template_folder=path)

@app.route("/")
def main():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0")
