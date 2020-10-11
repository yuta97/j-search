from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import mysql.connector as mysql
from dbconect import dbConnection

app = Flask(__name__)
CORS(app)
app.config['JSON_AS_ASCII'] = False 
app.config["JSON_SORT_KEYS"] = False 



@app.route('/continuous-records/match/win/', methods=['GET'])
def hello2():
    yearFrom = int(request.args.get('yearFrom',2017))
    yearTo = int(request.args.get('yearTo',2019))
    continuou_recordFrom = int(request.args.get('continuou_recordFrom',2))
    continuou_recordTo = int(request.args.get('continuou_recordTo',34))
    conn = dbConnection()
    conn.ping(reconnect=True)
    cursor = conn.cursor()
    # cursor.execute("use employees;")
    cursor.execute("select * from winrecords where year <= %s and  year >= %s and continuou_record <= %s and continuou_record >= %s;",(yearTo,yearFrom,continuou_recordTo,continuou_recordFrom)) 
    data = cursor.fetchall()
    return jsonify({
        'status':'OK',
        'data':data
    })



if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True)