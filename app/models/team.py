from app import db

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    players = db.relationship('Player', backref='team', lazy=True)

    def __repr__(self):
        return f"<Team {self.name}>"
