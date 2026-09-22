from datetime import datetime, timezone
from app.extensions import db
from app.models.user import User

class Customer(db.Model):
    __tablename__ = "clientes"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    updated_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    user = db.relationship("User", back_populates="customers", lazy=True)

    def __repr__(self):
        return f"<Cliente {self.name}>"