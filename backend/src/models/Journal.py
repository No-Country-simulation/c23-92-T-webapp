import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from extensions import db
from datetime import datetime

class Journal(db.Model):
    __tablename__ = 'journals'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)
    date_journal = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    interactions_count = db.Column(db.Integer, default=0)

    user = relationship('User', back_populates='journals')

    interactions = relationship('Interactions', back_populates='journal', cascade='all, delete-orphan')

    def __init__(self, user_id):
        self.user_id = user_id
    
    def __repr__(self):
        return f"<Journal {self.id}>"