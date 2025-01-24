import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    timezone = db.Column(db.String(50), default="UTC", nullable=False)
    journals = relationship('Journal', back_populates='user', cascade='all, delete-orphan')

    def __init__(self, username, email, password, timezone='UTC'):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)
        self.timezone = timezone

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def encrypt_password(self, password):
        return generate_password_hash(password)

    def __repr__(self):
        return f"<User {self.username}>"