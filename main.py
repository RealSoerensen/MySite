from flask import Flask, render_template

app = Flask(__name__,
    static_folder="templates/assets",
    template_folder="templates")


@app.route("/")
def main():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0")
