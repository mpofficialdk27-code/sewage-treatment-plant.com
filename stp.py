import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# --- सेटअप ---
base_dir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

# --- डेटाबेस कॉन्फ़िगरेशन (Render के लिए अपडेट किया गया) ---

# पुरानी लाइन को हटा दिया गया है:
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(base_dir, 'database.db')

# Render के लिए writeable डिस्क का पाथ
RENDER_DISK_PATH = '/var/data'
DATABASE_PATH = os.path.join(RENDER_DISK_PATH, 'database.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + DATABASE_PATH
# --- अपडेट खत्म ---

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- डेटाबेस मॉडल (सूचना टेबल) ---
class UpdatePost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

# --- वेबसाइट के पेज (Routes) ---

@app.route("/")
@app.route("/home")
def home():
    # 'templates' फ़ोल्डर से index.html को रेंडर करो
    return render_template('index.html')

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/how-it-works")
def how_it_works():
    return render_template('how-it-works.html')

@app.route("/updates")
def updates():
    # बैकएंड का काम: डेटाबेस से सभी पोस्ट को 'तारीख' के हिसाब से (नई पहले) ऑर्डर करो
    posts = UpdatePost.query.order_by(UpdatePost.date_posted.desc()).all()
    
    # 'updates.html' पेज को रेंडर करो और उसे सभी 'posts' भेज दो
    return render_template('updates.html', posts=posts, title="सूचनाएं")


# --- यह कोड सिर्फ एक बार, डेटाबेस बनाने के लिए ---
def create_database_if_not_exists():
    # यह चेक करेगा कि हम Render पर हैं या नहीं
    is_on_render = os.environ.get('RENDER', False)
    db_path_to_check = DATABASE_PATH if is_on_render else os.path.join(base_dir, 'database.db')

    # अगर Render पर हैं, तो डेटाबेस हमेशा 'writeable' पाथ में ही बनेगा
    # अगर लोकल हैं, तो यह .db फ़ाइल को चेक करेगा
    
    # एक 'app context' के अंदर यह काम करना ज़रूरी है
    with app.app_context():
        # हम सीधे db.create_all() को कॉल कर सकते हैं, 
        # यह टेबल तभी बनाएगा जब वे मौजूद नहीं होंगी।
        db.create_all()
        
        # चेक करें कि क्या कोई पोस्ट पहले से है
        if UpdatePost.query.count() == 0:
            print("डेटाबेस खाली है, सैंपल पोस्ट जोड़ रहे हैं...")
            # कुछ सैंपल पोस्ट जोड़ रहे हैं
            post1 = UpdatePost(title='वेबसाइट लॉन्च (सैंपल पोस्ट)', content='जल संरक्षण और सीवर ट्रीटमेंट के महत्व पर जागरूकता फ़ैलाने के लिए यह शैक्षणिक वेबसाइट आज लॉन्च की गई है।')
            post2 = UpdatePost(title='जल ही जीवन है (सैंपल लेख)', content='पानी बचाना क्यों ज़रूरी है? इस लेख में हम जल संरक्षण के आसान तरीकों पर चर्चा करेंगे...')
            
            db.session.add(post1)
            db.session.add(post2)
            db.session.commit()
            print("सैंपल पोस्ट जोड़ दिए गए हैं।")
        else:
            print("डेटाबेस पहले से मौजूद है।")


# --- ऐप को रन करो ---
if __name__ == '__main__':
    create_database_if_not_exists() # ऐप रन होने से पहले डेटाबेस चेक होगा
    # debug=True को Render पर हटा देना चाहिए, लेकिन waitress इसे हैंडल कर लेगा।
    # लोकल चलाने के लिए:
    # app.run(debug=True)
    
    # यह लाइन Render के 'Start Command' (waitress-serve) द्वारा इस्तेमाल की जाती है
    # इसलिए हमें यहाँ app.run() की ज़रूरत नहीं है जब यह सर्वर पर हो।
    # create_database_if_not_exists() अपने आप चल जाएगा।
    pass
