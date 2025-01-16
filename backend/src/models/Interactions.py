import uuid
from sqlalchemy.dialects.postgresql import UUID
from extensions import db
from datetime import datetime

class Interactions(db.Model):
    __tablename__ = 'interactions'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    content = db.Column(db.Text, nullable=False)
    response = db.Column(db.Text, nullable=True)
    date_interaction = db.Column(db.DateTime, default=datetime.utcnow)

    # crear relacion con journal
    # journal_id = db.Column(UUID(as_uuid=True), db.ForeignKey('journals.id'), nullable=False)

    # journal = relationship('Journal', back_populates='interactions')

    def __repr__(self):
        return f"<Interaction {self.content}>"