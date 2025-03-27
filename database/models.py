from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Document(Base):
    __tablename__ = 'documents'
    id = Column(Integer, primary_key=True)
    filename = Column(String, nullable=False)
    slides = relationship("Slide", back_populates="document")

class Slide(Base):
    __tablename__ = 'slides'
    id = Column(Integer, primary_key=True)
    document_id = Column(Integer, ForeignKey('documents.id'))
    slide_number = Column(Integer)
    title = Column(String(255))
    content = Column(Text)
    document = relationship("Document", back_populates="slides")
