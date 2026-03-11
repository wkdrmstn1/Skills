from flask import Flask, jsonify
from flask_cors import CORS  # <-- 이거 필수!

app = Flask(__name__)
CORS(app)  # 모든 곳에서 오는 요청을 허용한다 (보안 해제)

@app.route('/api/hello')
def hello():
    return jsonify({"message": "안녕? 나는 Flask야!"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)