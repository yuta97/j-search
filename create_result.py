import requests
from bs4 import BeautifulSoup
import time
import mysql.connector as mysql
from dbconect import dbConnection

def match_result(url,result_team_list,team_num):
  # urlをスクレイピングしlistに試合結果を挿入する関数。
  # Ex. result_team_list = ['チーム名',0,1,3,3,0,・・・]
  html = requests.get(url)
  soup = BeautifulSoup(html.text, "html.parser")
  base = soup.find("tbody")
  tr = base.find_all("tr", recursive=False)
  if result_team_list == []:
    result_team_list.append(tr[team_num].find("th").text)

  matches = tr[team_num].find_all("td", recursive=False)
  
  for match in matches:
    match = match.find("table").find_all("tr")[1]
    match_result = match.find("th").text
    if '●' in match_result: #lose
      result_team_list.append(0)
    elif '△' in match_result: #draw
      result_team_list.append(1)
    elif '○' in match_result: #win
      result_team_list.append(3)

number = [0,9,18,27,'' ] #pageを変えるオプション。1ページに8節しかない
result_list = [] #result_team_listをいれる配列
options = [
  [2019,460],[2018,444],[2017,428]
]
# 2020年はシーズン途中なので別途対応が必要（定期的にクローリングするのも含めて2020年用の関数を用意する。節指定。）
# options = [
#   [2020,477],
# ]
for yearId, competitionId in options:
  # time.sleep(5) # 一度の大量アクセスを防ぐ
  result_list＿year= [yearId]
  for team_num in range(1,19):
    # チーム数（18）分ループを回す
    result_team_list = []
    for n in number:
      url = f"https://data.j-league.or.jp/SFRT05/?search=search&yearId={yearId}&competitionId={competitionId}&currIdx={n}"
      match_result(url,result_team_list,team_num)
    result_list_year.append(result_team_list)
    # print(len(result_team_list))
  result_list.append(result_list＿year)

#mysql

conn = dbConnection()
conn.ping(reconnect=True)
cursor = conn.cursor()
cursor.execute("use employees;")

try:
    cursor.execute("create table matchresult (id int auto_increment primary key, year int, rank int, section int, team_name varchar(100), result int);")
except mysql.errors.ProgrammingError:
  print("already exists")

for list_byyear in result_list:
  year = list_byyear[0]
  for result in list_byyear[1:]:
    team_name = result[0]
    result_sections = result[1:]
    index = 1
    for result_section in result_sections:
      section = index 
      index += 1
      cursor.execute("INSERT INTO matchresult (year ,rank ,section ,team_name ,result ) VALUES (%s,1,%s,%s,%s);", (year,section ,team_name ,result_section))


#create_winrecords
try:
    cursor.execute("create table winrecords (id int auto_increment primary key, year int, rank int, team_name varchar(100), section_from int,section_to int, continuou_record int);")
except mysql.errors.ProgrammingError:
  print("already exists")


for list_byyear in result_list:
  year = list_byyear[0]
  for result in list_byyear[1:]:
    team_name = result[0]
    winrecords_num = 0
    winrecords_start = 0
    winrecords_stop = 0
    index = 1
    for point in result:
      section = index 
      index += 1
      if section == 34:
        if winrecords_num >=1 and point ==3:
          winrecords_num += 1
          winrecords_stop = 34
          cursor.execute("INSERT INTO winrecords (year ,rank ,team_name , section_from, section_to, continuou_record) VALUES (%s,1,%s,%s,%s,%s);", (year,team_name,winrecords_start,winrecords_stop,winrecords_num))
      else: #section !=34
        if point == 3:
          winrecords_num += 1
          if winrecords_num == 1:
            winrecords_start = section
        else: # point == 0,1
          if winrecords_num >= 2:
            winrecords_stop = section-1
            cursor.execute("INSERT INTO winrecords (year ,rank ,team_name , section_from, section_to, continuou_record) VALUES (%s,1,%s,%s,%s,%s);", (year,team_name,winrecords_start,winrecords_stop,winrecords_num))
          winrecords_num = 0
          winrecords_start = 0
          winrecords_stop = 0
cursor.close()
conn.commit()
conn.close()
