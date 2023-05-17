from flask import Flask, render_template, request, jsonify

from pymongo import MongoClient
client = MongoClient('mongodb+srv://sparta:test@cluster0.ssvirwm.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta
from bson.objectid import ObjectId

import certifi
import base64
import gridfs

app = Flask(__name__)

fs = gridfs.GridFS(db)
ca = certifi.where()

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/view')
def song():
    name=request.args.get('name')       
    mbti=request.args.get('mbti')
    return render_template('view.html',name=name)

@app.route("/", methods=["POST"])
def menu_post():
    photo_receive = request.files['photo_give']
    name_receive = request.form['name_give']
    introduce_receive = request.form['introduce_give']
    mbti_receive = request.form['mbti_give']
    merits_demerits_receive = request.form['merits_demerits_give']
    style_receive = request.form['style_give']
    blog_receive = request.form['blog_give']
    github_receive = request.form['github_give']
    
    file_img_id = fs.put(photo_receive)
    doc = {
        'photo' : file_img_id,
        'name' : name_receive,
        'introduce' : introduce_receive,
        'mbti' : mbti_receive,
        'merits_demerits' : merits_demerits_receive,
        'style' : style_receive,
        'blog' : blog_receive,
        'github' : github_receive
    }
    db.member.insert_one(doc)
    return jsonify({'msg':'저장 완료!'})
    
@app.route("/alldata", methods=["GET"])
def team_get():
    all_myself = list(db.member.find({},{'_id':True, 'name':True, 'mbti':True, 'introduction':True, 
                                         'strengths':True, 'collaboration_style':True ,'blog_url':True
                                         ,'github_url':True, 'photo':True}))
    
    for myself in all_myself:
        photo_id = myself['photo']
        if photo_id:
            try:
                image_data = fs.get(photo_id).read()
                base64_img = base64.b64encode(image_data).decode('utf-8')
                myself['photo'] = 'data:image/jpeg;base64,' + base64_img
            except gridfs.error.NoFile as e:
                print.error("파일이 없습니다.")  
                 
        myself['_id'] = str(myself['_id'])
    
    return jsonify({'result':all_myself})


@app.route("/view/<id>", methods=["GET"])
def find_team(id):    
    find_myself = db.member.find_one({"_id": ObjectId(id)})        
    photo_id = find_myself['photo']    
    print('find_myself = ', find_myself['photo'])
    print(photo_id)      
    if photo_id:
         try:
              image_data = fs.get(photo_id).read()
              base64_img = base64.b64encode(image_data).decode('utf-8')
              find_myself['photo'] = 'data:image/jpeg;base64,' + base64_img
         except gridfs.error.NoFile as e:
              print.error("파일이 없습니다.")    
    find_myself['photo'] = str(find_myself['photo'])

    
    return render_template('view.html', myself=find_myself)



    




@app.route('/write.html')
def menuInput():
    return render_template('write.html')
    
if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)