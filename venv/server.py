from flask import Flask, request, jsonify, render_template
import ocr
from flask_cors import CORS,cross_origin
import pandas as pd
app = Flask(__name__)
CORS(app)
dataframe = pd.read_csv('maple_daily_quest_index.csv')
@app.route('/') #test api
def hello_world():
    return render_template('index_1.html')

@app.route('/post', methods = ['POST']) #get echo api
def get_echo_call():
    global dataframe
    data = request.get_json()
    print(data)
    base64 = ocr.main(data['image'],dataframe)
    print(base64)
    return jsonify({"param": base64})

app.run(host='0.0.0.0', port=5000, debug=True)

