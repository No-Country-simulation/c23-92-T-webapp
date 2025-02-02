import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy import CheckConstraint
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
    mood_intensity = db.Column(db.Integer, nullable=True, info={"check_constraint": "mood_intensity >= 0 AND mood_intensity <= 10"})

    __table_args__ = (
        CheckConstraint("mood_intensity >= 0 AND mood_intensity <= 10", name="mood_intensity_range"),
    )

    def __init__(self, title, state, content, response, journal_id, mood_intensity=None):
        self.title = title
        self.state_interaction = state
        self.journal_id = journal_id
        self.content = content
        self.response = response
        self.mood_intensity = mood_intensity
    
    def to_dict(self):
        return {
            "title": self.title,
            "content": self.content,
            "response": self.response,
            "date_interaction": self.date_interaction.isoformat() if self.date_interaction else None,
            "state_interaction": self.state_interaction,
            "mood_intensity": self.mood_intensity,
            "journal": {
                "date_journal": self.journal.date_journal.isoformat() if self.journal.date_journal else None,
                "interactions_count": self.journal.interactions_count
            }
        }
    
    def to_dict_without_journal(self):
        return {
            "title": self.title,
            "content": self.content,
            "response": self.response,
            "date_interaction": self.date_interaction.isoformat() if self.date_interaction else None,
            "state_interaction": self.state_interaction,
            "mood_intensity": self.mood_intensity
        }

    def __repr__(self):
        return f"<Interaction {self.content}>"