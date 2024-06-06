from app.extensions import db

class JobBoardScraperEmails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return f'<User: {self.email}>'
