from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Receipt(Base):
    """Receipt model for purchase records."""
    __tablename__ = "receipts"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    shopping_list_id = Column(Integer, ForeignKey("shopping_lists.id"), nullable=True)
    store_name = Column(String(255), nullable=False)
    total_amount = Column(Float, nullable=False)
    items_count = Column(Integer, default=0)
    receipt_image_url = Column(String(500), nullable=True)
    ocr_text = Column(String(2000), nullable=True)
    is_processed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Receipt(id={self.id}, user_id={self.user_id}, store_name={self.store_name})>"
