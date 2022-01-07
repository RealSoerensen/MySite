from flask import Flask, render_template
from pathlib import Path
from api_refresh import Stats
import threading

path = Path(__file__).parent.resolve()
app = Flask(__name__, 
    static_folder=str(path) + "/assets", 
    template_folder=path)

@app.route("/")
def main():
    return render_template('index.html')

# Refresh stats every 24 hours
def refresh():
    threading.Timer(60*60*24, refresh).start()
    stat = Stats()
    stat.update()

if __name__ == "__main__":
    app.run(host="0.0.0.0")
    refresh()
