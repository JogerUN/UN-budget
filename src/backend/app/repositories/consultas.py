from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.prueba import Item


class ItemRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_all(self) -> list[Item]:
        stmt = select(Item)
        return list(self.db.scalars(stmt).all())

    def get_first(self) -> Item | None:
        stmt = select(Item).limit(1)
        return self.db.scalar(stmt)

    def get_by_id(self, item_id: int) -> Item | None:
        stmt = select(Item).where(Item.id == item_id)
        return self.db.scalar(stmt)

    def create(self, texto_item: str) -> Item:
        nuevo_item = Item(item=texto_item)
        self.db.add(nuevo_item)
        self.db.commit()
        self.db.refresh(nuevo_item)
        return nuevo_item