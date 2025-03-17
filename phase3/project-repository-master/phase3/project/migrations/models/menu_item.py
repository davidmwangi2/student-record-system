from sqlalchemy import Column, Integer, String, ForeignKey
from .base import Base

class MenuItem(Base):
    __tablename__ = 'menu_items'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'), nullable=False)
