import uuid
from sqlalchemy.dialects.postgresql import UUID
from extensions import db
from sqlalchemy import Column, Text, Date
from datetime import datetime
import hashlib

class Token(db.Model):
    __tablename__ = 'tokens'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)
    refresh_token = Column(Text, nullable=False)
    token_signature = Column(Text, nullable=False)
    is_revoked = Column(db.Boolean, nullable=False, default=False)
    created_at = Column(Date, default=datetime.utcnow, nullable=False)
    updated_at = Column(Date, onupdate=datetime.utcnow, nullable=False)
    expires_at = Column(Date, nullable=False)
    device_id = Column(Text, nullable=True)

    def __init__(self, user_id, token_signature, refresh_token, expires_at, device_id):
        self.user_id = user_id
        self.refresh_token = refresh_token
        self.token_signature = token_signature
        self.expires_at = expires_at
        self.device_id = device_id

    def to_dict(self):
        return {
            "id": str(self.id),
            "user_id": str(self.user_id),
            "refresh_token": self.refresh_token,
            "token_signature": self.token_signature,
            "is_revoked": self.is_revoked,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "expires_at": self.expires_at,
            "device_id": str(self.device_id)
        }