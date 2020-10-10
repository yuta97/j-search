from dbconect import dbConnection
import mysql.connector as mysql

conn = dbConnection()
conn.ping(reconnect=True)
cursor = conn.cursor()

cursor.execute("use employees;")
try:
    cursor.execute("create table teamId (id int auto_increment primary key,team_id int , team_name varchar(100));")
except mysql.errors.ProgrammingError:
  print("already exists")

j_teamlists = {
  1: "北海道コンサドーレ札幌",
  2: "ベガルタ仙台",
  3: "鹿島アントラーズ",
  4: "浦和レッズ",
  5: "ＦＣ東京",
  6: "川崎フロンターレ",
  7: "横浜Ｆ・マリノス",
  8: "湘南ベルマーレ",
  9: "松本山雅ＦＣ",
  10: "清水エスパルス",
  11: "ジュビロ磐田",
  12: "名古屋グランパス",
  13: "ガンバ大阪",
  14: "セレッソ大阪",
  15: "ヴィッセル神戸",
  16: "サンフレッチェ広島",
  17: "サガン鳥栖",
  18: "大分トリニータ",
  19: "モンテディオ山形",
  20: "水戸ホーリーホック",
  21: "栃木ＳＣ",
  22: "大宮アルディージャ",
  23: "ジェフユナイテッド千葉",
  24: "柏レイソル",
  25: "東京ヴェルディ",
  26: "ＦＣ町田ゼルビア",
  27: "横浜ＦＣ",
  28: "ヴァンフォーレ甲府",
  29: "アルビレックス新潟",
  30: "ツエーゲン金沢",
  31: "ＦＣ岐阜",
  32: "京都サンガF.C.",
  33: "ファジアーノ岡山",
  34: "レノファ山口ＦＣ",
  35: "徳島ヴォルティス",
  36: "愛媛ＦＣ",
  37: "アビスパ福岡",
  38: "Ｖ・ファーレン長崎",
  39: "鹿児島ユナイテッドＦＣ",
  40: "ＦＣ琉球",   
}
	


for team_id ,team_name in j_teamlists.items():   
    cursor.execute("INSERT INTO teamId (team_id ,team_name) VALUES (%s,%s);", (team_id ,team_name))

cursor.close()

conn.commit()

conn.close()