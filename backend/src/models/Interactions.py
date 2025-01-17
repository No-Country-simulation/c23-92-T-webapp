import uuid
from sqlalchemy.dialects.postgresql import UUID
from extensions import db
from datetime import datetime

class Interactions(db.Model):
    __tablename__ = 'interactions'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    content = db.Column(db.String(1000), nullable=False)
    response = db.Column(db.String(1000), nullable=True)
    date_interaction = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, content, response):
        self.content = content
        self.response = response
        
    
    # crear relacion con journal
    # journal_id = db.Column(UUID(as_uuid=True), db.ForeignKey('journals.id'), nullable=False)

    # journal = relationship('Journal', back_populates='interactions')

    def __repr__(self):
        return f"<Interaction {self.content}>"