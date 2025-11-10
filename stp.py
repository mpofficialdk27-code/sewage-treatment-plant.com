import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# --- सेटअप ---
base_dir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
# डेटाबेस फ़ाइल का कॉन्फ़िगरेशन
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(base_dir, 'database.db')
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
def create_sample_data():
    if not os.path.exists(os.path.join(base_dir, 'database.db')):
        print("डेटाबेस बनाया जा रहा है...")
        with app.app_context():
            db.create_all()
            
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
    create_sample_data() # ऐप रन होने से पहले डेटाबेस चेक होगा
    app.run(debug=True) # debug=True का मतलब है कि बदलाव करते ही ऐप रीस्टार्ट हो जाएगा
