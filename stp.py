import os
import platform  # यह OS (Windows/Linux) चेक करने के लिए है
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
base_dir = os.path.abspath(os.path.dirname(__file__))

# --- डायनेमिक डेटाबेस कॉन्फ़िगरेशन (Windows और Render दोनों के लिए) ---
IS_ON_RENDER = os.environ.get('RENDER', False)

if IS_ON_RENDER:
    # Render (Linux) पर: /var/data/ (Persistent Disk) में सेव करें
    RENDER_DISK_PATH = '/var/data'
    DATABASE_PATH = os.path.join(RENDER_DISK_PATH, 'database.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + DATABASE_PATH
    print(f"Render एनवायरनमेंट डिटेक्ट हुआ। DB पाथ: {DATABASE_PATH}")
else:
    # लोकल (Laptop) पर:
    DATABASE_PATH = os.path.join(base_dir, 'database.db')
    
    # --- Windows पाथ फिक्स ---
    # Windows पाथ (C:\...) को फॉरवर्ड स्लैश (C:/...) में बदलें
    # और 3 स्लैश (sqlite:///) का इस्तेमाल करें
    DATABASE_PATH_FOR_URI = DATABASE_PATH.replace(os.sep, '/')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + DATABASE_PATH_FOR_URI
    # --- फिक्स खत्म ---
    
    print(f"लोकल एनवायरनमेंट डिटेक्ट हुआ। DB URI: {app.config['SQLALCHEMY_DATABASE_URI']}")


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

# --- DB Creation Logic ---
# यह ब्लॉक ऐप इनिशियलाइज़ होते ही रन होगा (Render और लोकल दोनों पर)
with app.app_context():
    print("डेटाबेस टेबल्स के लिए db.create_all() रन किया जा रहा है...")
    db.create_all()
    
    # चेक करें कि क्या कोई पोस्ट पहले से है
    if UpdatePost.query.count() == 0:
        print("डेटाबेस खाली है, सैंपल पोस्ट जोड़ रहे हैं...")
        post1 = UpdatePost(title='वेबसाइट लॉन्च (सैंपल पोस्ट)', content='जल संरक्षण और सीवर ट्रीटमेंट के महत्व पर जागरूकता फ़ैलाने के लिए यह शैक्षणिक वेबसाइट आज लॉन्च की गई है।')
        post2 = UpdatePost(title='जल ही जीवन है (सैंपल लेख)', content='पानी बचाना क्यों ज़रूरी है? इस लेख में हम जल संरक्षण के आसान तरीकों पर चर्चा करेंगे...')
        
        db.session.add(post1)
        db.session.add(post2)
        db.session.commit()
        print("सैंपल पोस्ट जोड़ दिए गए हैं।")
    else:
        print("डेटाबेस पहले से मौजूद है।")
# --- End of DB Creation Logic ---


# --- वेबसाइट के पेज (Routes) ---

@app.route("/")
@app.route("/home")
def home():
    return render_template('index.html')

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/how-it-works")
def how_it_works():
    return render_template('how-it-works.html')

@app.route("/updates")
def updates():
    posts = UpdatePost.query.order_by(UpdatePost.date_posted.desc()).all()
    return render_template('updates.html', posts=posts, title="सूचनाएं")

# --- ऐप को रन करो ---
if __name__ == '__main__':
    # यह सिर्फ लोकल (आपके लैपटॉप) पर चलाने के लिए है
    print("लोकल सर्वर (debug mode) स्टार्ट हो रहा है...")
    app.run(debug=True)
