from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


class SignUp(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(10), unique=True, nullable=False)
    mobile = db.Column(db.String(12), unique=True, nullable=False)
    country_code = db.Column(db.String(12),  nullable=False)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f"SignUp('{self.username}')"
