import requests
from bs4 import BeautifulSoup as bs
import os
from datetime import datetime

faceit_key = os.environ['faceit_key']

class Stats:
  def __init__(self):
    self.player_id = ""
    self.header = {"Authorization": "Bearer " + faceit_key}
      
  def faceit_id(self, name):
    try:
      r = requests.get(
          f"https://open.faceit.com/data/v4/players?nickname={name}",
          headers=self.header)
      acc_data = r.json()
      player_id = acc_data.get("player_id")
    except Exception:
        return "Error"
    return player_id

  def krunker_stats(self):
    try:
      r = requests.get(
        f"https://open.faceit.com/data/v4/players/{self.player_id}/stats/krunker",
        headers=self.header)
      acc_data = r.json()
      data = acc_data.get("lifetime")
      kd = data.get("Average K/D ratios")
      hs = data.get("Average headshot %")
      winrate = data.get("Win rate %")
    except Exception:
        return "Error", "Error", "Error"
    return kd, hs, winrate

  def csgo_stats(self):
    try:
      r = requests.get(
        f"https://open.faceit.com/data/v4/players/{self.player_id}/stats/csgo",
        headers=self.header)
      acc_data = r.json()
      data = acc_data.get("lifetime")
      kd = data.get("Average K/D Ratio")
      hs = data.get("Average Headshots %")
      winrate = data.get("Win Rate %")
    except Exception:
        return "Error", "Error", "Error"
    return kd, hs, winrate

  def faceit_level(self, game):
      try:
          r = requests.get(
            f"https://open.faceit.com/data/v4/players/{self.player_id}",
            headers=self.header)
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

  def api_stats(self):
    # Krunker and CSGO rank
    self.player_id = Stats.faceit_id(self, "-Soerensen")

    krunker_stat = Stats.faceit_level(self, "krunker") + Stats.krunker_stats(self)
    csgo_stat = Stats.faceit_level(self, "csgo") + Stats.csgo_stats(self)

    # Valorant rank
    valo_stats = Stats.valorant_stats()

    # Aimlab
    aimlab_stats = "Master 3"

    # Rocket League
    rl_stats = "Champion 2"

    # Splitgate
    sg_stats = "Diamond"

    return csgo_stat, krunker_stat, valo_stats, aimlab_stats, rl_stats, sg_stats

  def update(self):
    csgo_stat, krunker_stat, valo_stats, aimlab_stats, rl_stats, sg_stats = Stats.api_stats(self)
    # Open index.html
    with open("index.html") as f:
      soup = bs(f, 'html.parser')
      soup.find("span", {
          "class": "csgo_level"
      }).string.replaceWith(str(csgo_stat[0]))
      soup.find("span", {
          "class": "csgo_elo"
      }).string.replaceWith(str(csgo_stat[1]))
      soup.find("span", {
          "class": "csgo_kd"
      }).string.replaceWith(str(csgo_stat[2]))
      soup.find("span", {
          "class": "csgo_hs"
      }).string.replaceWith(str(csgo_stat[3]))
      soup.find("span", {
          "class": "csgo_winrate"
      }).string.replaceWith(str(csgo_stat[4]))

      soup.find("span", {
          "class": "krunker_level"
      }).string.replaceWith(str(krunker_stat[0]))
      soup.find("span", {
          "class": "krunker_elo"
      }).string.replaceWith(str(krunker_stat[1]))
      soup.find("span", {
          "class": "krunker_kd"
      }).string.replaceWith(str(krunker_stat[2]))
      soup.find("span", {
          "class": "krunker_hs"
      }).string.replaceWith(str(krunker_stat[3]))
      soup.find("span", {
          "class": "krunker_winrate"
      }).string.replaceWith(str(krunker_stat[4]))

      soup.find("span", {
          "class": "valo_rank"
      }).string.replaceWith(str(valo_stats[0]))
      soup.find("span", {
          "class": "valo_rr"
      }).string.replaceWith(str(valo_stats[1]))

      soup.find("span", {
          "class": "aimlab_rank"
      }).string.replaceWith(str(aimlab_stats))

      soup.find("span", {
          "class": "rl_rank"
      }).string.replaceWith(str(rl_stats))

      soup.find("span", {
          "class": "sg_rank"
      }).string.replaceWith(str(sg_stats))

      now = datetime.now()
      dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
      soup.find("span", {"class": "api_updated"}).string.replaceWith(str(dt_string))

    with open("index.html", "w") as file:
        file.write(str(soup.prettify()))