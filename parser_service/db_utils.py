from database.db import SessionLocal
from database.models import Slide

def save_slide(slide_number, title, content, document_id=None):
    session = SessionLocal()
    try:
        slide = Slide(
            slide_number=slide_number,
            title=title,
            content=content,
            document_id=document_id
        )
        session.add(slide)
        session.commit()
        return {
            'document_id': document_id,
            'slide_number': slide_number,
            'title': title,
            'content': content
        }
    finally:
        session.close()
