from dbconect import dbConnection
import mysql.connector as mysql

conn = dbConnection()
conn.ping(reconnect=True)
cursor = conn.cursor()
cursor.execute("use employees;")



for list_byyear in result_list:
  year = list_byyear[0]
  result = list_byyear[1]
  result_sections = result[1:]
  for index, result_section in enumerate(result_sections):  
    section = index+1
    cursor.execute("INSERT INTO matchresult (year ,rank ,section ,team_id ,result ) VALUES (%s,1,%s,1,%s);", (year, section, result_section))


cursor.execute("select section, result from sample3  where year = 2019 and rank = 1 and team_id = 1 order by section;") 

results = cursor.fetchall()
# print(results)
points = []
for result in results:
  points.append(result[0])

# print(points)

try:
    cursor.execute("create table winrecords (id int auto_increment primary key, year int, rank int, team_id int, section_from int,section_to int, continuou_record int);")
except mysql.errors.ProgrammingError:
  print("already exists")
year = 2019

winrecords_num = 0
winrecords_start = 0
winrecords_stop = 0
for section, point in results:
  if section == 34:
    if winrecords_num >=1 and point ==3:
      winrecords_num += 1
      winrecords_stop = 34
      cursor.execute("INSERT INTO winrecords (year ,rank ,team_id , section_from, section_to, continuou_record) VALUES (%s,1,1,%s,%s,%s);", (year,winrecords_start,winrecords_stop,winrecords_num))
  else: #section !=34
    if point == 3:
      winrecords_num += 1
      if winrecords_num == 1:
        winrecords_start = section
    else: # point == 0,1
      if winrecords_num >= 2:
        winrecords_stop = section-1
        cursor.execute("INSERT INTO winrecords (year ,rank ,team_id , section_from, section_to, continuou_record) VALUES (%s,1,1,%s,%s,%s);", (year,winrecords_start,winrecords_stop,winrecords_num))
      winrecords_num = 0
      winrecords_start = 0
      winrecords_stop = 0

  
# cursor.execute("select * from sample4;") 
# data = cursor.fetchall()
# # print(data)
