import uuid
from sqlalchemy.dialects.postgresql import UUID
from extensions import db
from sqlalchemy import Column, Text, Date
from datetime import datetime

class Token(db.Model):
    __tablename__ = 'tokens'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)
    refresh_token = Column(Text, nullable=False)
    created_at = Column(Date, default=datetime.utcnow, nullable=False)
    updated_at = Column(Date, onupdate=datetime.utcnow, nullable=False)
    expires_at = Column(Date, nullable=False)

    def __init__(self, user_id, refresh_token, expires_at):
        self.user_id = user_id
        self.refresh_token = refresh_token
        self.expires_at = expires_at