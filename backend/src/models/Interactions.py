import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from extensions import db
from datetime import datetime

class Interactions(db.Model):
    __tablename__ = 'interactions'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = db.Column(db.String(100), nullable=True)
    content = db.Column(db.String(1000), nullable=False)
    response = db.Column(db.String(1000), nullable=True)
    date_interaction = db.Column(db.DateTime, default=datetime.utcnow)
    state_interaction = db.Column(db.Integer, default=1, nullable=True)
    journal_id = db.Column(UUID(as_uuid=True), db.ForeignKey('journals.id', ondelete="CASCADE"), nullable=False)
    journal = relationship('Journal', back_populates='interactions')

    def __init__(self, title, state, content, response, journal_id):
        self.title = title
        self.state_interaction = state
        self.journal_id = journal_id
        self.content = content
        self.response = response
        
    
    def __repr__(self):
        return f"<Interaction {self.content}>"