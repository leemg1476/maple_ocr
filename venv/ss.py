from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route('/') #test api
def hello_world():
    return render_template('index_1.html')

@app.route('/echo_call/<param>') #get echo api
def get_echo_call(param):
    return jsonify({"param": param})

@app.route('/echo_call', methods=['POST']) #post echo api
def post_echo_call():
    param = request.get_json()
    return jsonify(param)

app.run(host='0.0.0.0', port=5000, debug=True)

