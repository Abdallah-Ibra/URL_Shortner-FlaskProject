# Import Modules
from flask import Flask,redirect,request,render_template
from flask_sqlalchemy import SQLAlchemy
from hashids import Hashids

#  Config

app = Flask(__name__)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
SALT = 'Hashids SALT'


class Url(db.Model):
   
   # Create table 'urls' id,url
   __tablename__ =  "urls"
   id = db.Column(db.Integer,primary_key=True)
   url = db.Column(db.Text)
   
   def __init__(self,url):
      self.url = url
  
      
@app.route('/')
def index():
    return render_template("index.html")
 
     
# Controllers
@app.route('/shorten')
def shorten():
    # الحصول على الرّابط
    link = request.args.get('link')
    # التّحقق من أنّ الرّابط صالح
    if link and link != "" and not link.count(' ') >= 1 and not link.count('.') == 0:
        # إضافة بادئة http إذا لم تتواجد
        if link[:4].lower() != 'http':
            link = 'http://{}'.format(link)
        # إضافة الرّابط إلى قاعدة البيانات
        db.session.add(Url(url=link)) 
        db.session.commit()
        # استخراج رقم مُعرّف آخر رابط مُضاف (أي الرّابط المُضاف في هذا الموجّه)
        url_id = db.session.query(Url).order_by(Url.id.desc()).first().id
        # تشفير رقم المُعرّف
        id_code = Hashids(salt=SALT, min_length=4).encode(url_id)
        # إضافة علامة / إلى بداية المعرّف الخاص بالرّابط ('/HFdK')
        short_link = '/' + id_code  
        # إرجاع المعرّف
        return short_link 
    # في حالة عدم صلاحيّة الرّابط، عد إلى الصّفحة الرّئيسيّة
    else:
        return render_template("index.html")
      
@app.route('/<id>')
def url(id):
    # تحويل المُعرّف إلى عدد  (فك تشفيره)
    original_id = Hashids(salt=SALT, min_length=4).decode(id)
    # إذا كان المعرف مرتبطا بمجموعة فاحصل على العنصر الأول
    if original_id:
        original_id = original_id[0]
        # الحصول على الرّابط من خلال رقم مُعرّفه
        original_url = Url.query.filter_by(id=original_id).first().url

        # إعادة توجيه المُستخدم إلى الرّابط الأصلي
        return redirect(original_url , code=302)
    else:
        return render_template('index.html')
      
      
if __name__ == "__main__":
    app.run(debug=True,port=7000)