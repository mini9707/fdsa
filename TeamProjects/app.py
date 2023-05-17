from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
import certifi
import base64
import gridfs
app = Flask(__name__)
client = MongoClient('mongodb+srv://sparta:test@atlascluster.anrkcap.mongodb.net/')
db = client.dbsparta
fs = gridfs.GridFS(db)
ca = certifi.where()
@app.route('/')
def home():
    return render_template('index.html')
@app.route("/menu", methods=["POST"])
def menu_post():
    photo_receive = request.files['photo_give']
    cate_receive = request.form['cate_give']
    comment_receive = request.form['comment_give']
    star_receive = request.form['star_give']
    name_receive = request.form['name_give']
    address_receive = request.form['address_give']
    menu_receive = request.form['menu_give']
    cost_receive = request.form['cost_give']
    
    file_img_id = fs.put(photo_receive)
    doc = {
        'photo' : file_img_id,
        'cate' : cate_receive,
        'name' : name_receive,
        'address' : address_receive,
        'comment' : comment_receive,
        'star' : star_receive,
        'menu' : menu_receive,
        'cost' : cost_receive
    }
    db.delicious.insert_one(doc)
    return jsonify({'msg':'저장 완료!'})
    
@app.route("/menu", methods=["GET"])
def menu_get():
    all_menus = list(db.delicious.find({},{'_id':False}))
    for menus in all_menus :
            photo_id = menus['photo']
            if photo_id:
                    try:
                        image_data = fs.get(photo_id).read()
                        base64_img = base64.b64encode(image_data).decode('utf-8')
                        menus['photo'] = 'data:image/jpeg;base64,' + base64_img
                    except gridfs.error.NoFile as e:
                        print("파일이 없습니다.")
    return jsonify({'result': all_menus})
@app.route('/menu/input')
def menuInput():
    return render_template('popup.html')
    
if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)