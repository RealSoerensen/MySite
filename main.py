from os import path
import requests
from bs4 import BeautifulSoup as bs
from flask import Flask, render_template
import html

path = path.dirname(__file__)
app = Flask(__name__, static_folder=path + "/assets", template_folder=path)

@app.route("/")
def main():
    csgo_stat, krunker_stat, valo_stats, aimlab_stats, rl_stats, sg_stats = api_stats()
    # Open index.html
    with open("index.html") as f:
        soup = bs(f, 'html.parser')
        soup.find("span", {"class": "csgo_level"}).string.replaceWith(str(csgo_stat[0]))
        soup.find("span", {"class": "csgo_elo"}).string.replaceWith(str(csgo_stat[1]))
        soup.find("span", {"class": "csgo_kd"}).string.replaceWith(str(csgo_stat[2]))
        soup.find("span", {"class": "csgo_hs"}).string.replaceWith(str(csgo_stat[3]))
        soup.find("span", {"class": "csgo_winrate"}).string.replaceWith(str(csgo_stat[4]))

        soup.find("span", {"class": "krunker_level"}).string.replaceWith(str(krunker_stat[0]))
        soup.find("span", {"class": "krunker_elo"}).string.replaceWith(str(krunker_stat[1]))
        soup.find("span", {"class": "krunker_kd"}).string.replaceWith(str(krunker_stat[2]))
        soup.find("span", {"class": "krunker_hs"}).string.replaceWith(str(krunker_stat[3]))
        soup.find("span", {"class": "krunker_winrate"}).string.replaceWith(str(krunker_stat[4]))

        soup.find("span", {"class": "valo_rank"}).string.replaceWith(str(valo_stats[0]))
        soup.find("span", {"class": "valo_rr"}).string.replaceWith(str(valo_stats[1]))

        soup.find("span", {"class": "aimlab_rank"}).string.replaceWith(str(aimlab_stats))

        soup.find("span", {"class": "rl_rank"}).string.replaceWith(str(rl_stats))

        soup.find("span", {"class": "sg_rank"}).string.replaceWith(str(sg_stats))

    with open("index.html", "w") as file: 
        
        file.write(str(soup.prettify()))
    return render_template('index.html')


def faceit_id(name, header):
    try:
        r = requests.get(f"https://open.faceit.com/data/v4/players?nickname={name}", headers=header)
        acc_data = r.json()
        player_id = acc_data.get("player_id")
    except Exception:
        return "Error"
    return player_id


def krunker_stats(player_id, header):
    try:
        r = requests.get(f"https://open.faceit.com/data/v4/players/{player_id}/stats/krunker", headers=header)
        acc_data = r.json()
        data = acc_data.get("lifetime")
        kd = data.get("Average K/D ratios")
        hs = data.get("Average headshot %")
        winrate = data.get("Win rate %")
    except Exception:
        return "Error", "Error", "Error"
    return kd, hs, winrate


def csgo_stats(player_id, header):
    try:
        r = requests.get(f"https://open.faceit.com/data/v4/players/{player_id}/stats/csgo", headers=header)
        acc_data = r.json()
        data = acc_data.get("lifetime")
        kd = data.get("Average K/D Ratio")
        hs = data.get("Average Headshots %")
        winrate = data.get("Win Rate %")
    except Exception:
        return "Error", "Error", "Error"
    return kd, hs, winrate


def faceit_level(player_id, game, header):
    try:
        r = requests.get(f"https://open.faceit.com/data/v4/players/{player_id}", headers=header)
        accData = r.json()
        data = accData.get("games").get(game)
        level = data.get("skill_level")
        elo = data.get("faceit_elo")
    except Exception:
        return "Error", "Error"
    return level, elo


def valorant_stats():
    try:
        r = requests.get(f"https://api.henrikdev.xyz/valorant/v1/mmr/eu/LFT Soerensen/420")
        acc_data = r.json()
        data = acc_data.get("data")
        rank = data.get("currenttierpatched")
        rr = data.get("currenttier")
        return rank, rr
    except Exception:
        return "Error", "Error"


def api_stats():
    # Krunker and CSGO rank
    name = "-Soerensen"
    faceit_key = "4705bf80-6714-44c7-96e0-0525c7239f1b"
    header = {"Authorization": "Bearer " + faceit_key}
    player_id = faceit_id(name, header)

    krunker_stat = faceit_level(player_id, "krunker", header) + krunker_stats(player_id, header)
    csgo_stat = faceit_level(player_id, "csgo", header) + csgo_stats(player_id, header)

    # Valorant rank
    valo_stats = valorant_stats()

    # Aimlab
    aimlab_stats = "Master 3"

    # Rocket League
    rl_stats = "Champion 2"

    # Splitgate
    sg_stats = "Diamond"

    return csgo_stat, krunker_stat, valo_stats, aimlab_stats, rl_stats, sg_stats

if __name__ == "__main__":
    app.run(host="0.0.0.0")
