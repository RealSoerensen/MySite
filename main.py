from flask import Flask, render_template
from pathlib import Path
from api_refresh import Stats
from threading import Thread
from time import sleep

path = Path(__file__).parent.resolve()
app = Flask(__name__, 
  static_folder=str(path) + "/assets", 
  template_folder=path)

@app.route("/")
def main():
  return render_template('index.html')

# Refresh stats every 24 hours
def refresh():
  stat = Stats()
  stat.update()
  print("Stats updated")
  sleep(60*60*24)

if __name__ == "__main__":
  Thread(target=refresh).start()
  app.run(host="0.0.0.0")
