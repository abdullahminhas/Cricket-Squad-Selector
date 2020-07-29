from datetime import datetime
from test import db, login_manager, app
from flask_login import UserMixin
from whoosh.analysis import StemmingAnalyzer
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(30), nullable=False)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Player(db.Model):

    player_id = db.Column(db.Integer, primary_key=True, unique=True)
    player_name = db.Column(db.String(25), nullable=False)
    player_image = db.Column(db.String(20), nullable=False, default='default.jpg')
    player_style = db.Column(db.String(10), nullable=True)
    player_mat = db.Column(db.Integer, nullable=True)
    player_inns = db.Column(db.Integer, nullable=True)
    player_runs = db.Column(db.Integer, nullable=True)
    player_hs = db.Column(db.Integer, nullable=True)
    player_sr = db.Column(db.Float, nullable=True)
    player_ave = db.Column(db.Float, nullable=True)
    player_century = db.Column(db.Integer, nullable=True)
    player_country = db.Column(db.String(15), nullable=True)
    player_type = db.Column(db.String(12), nullable=True)
    player_bruns = db.Column(db.Integer, nullable=True)
    player_wkts = db.Column(db.Integer, nullable=True)
    player_bave = db.Column(db.Float, nullable=True)
    player_bsr = db.Column(db.Float, nullable=True)

    def __repr__(self):
        return f"Player('{self.player_id}', '{self.player_name}', '{self.player_image}', '{self.player_style}'," \
               f" '{self.player_mat}', '{self.player_inns}', '{self.player_country}', '{self.player_runs}'," \
               f" '{self.player_hs}', '{self.player_sr}', '{self.player_century}', '{self.player_type}'," \
               f" '{self.player_bruns}', '{self.player_bave}', '{self.player_bsr}')"
