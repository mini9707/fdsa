from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://sparta:test@cluster0.h5jsrip.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta


@app.route('/')
def home():
    return render_template('index.html')

@app.route("/bucket", methods=["POST"])
def bucket_post():
    bucket_receive = request.form['bucket_give']

    doc = {
        'bucket' : bucket_receive
    }
    db.bucket.insert_one(doc)

    return jsonify({'msg': '저장 완료!'})
    
@app.route("/bucket", methods=["GET"])
def bucket_get():
    all_bucket = list(db.bucket.find({},{'_id':False}))
    return jsonify({'result': all_bucket})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)