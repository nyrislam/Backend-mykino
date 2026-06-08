from sqlalchemy import Column, Integer, String, TIMESTAMP, text, ForeignKey
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=False),
        nullable=False,
        server_default=text("now()")
    )

class Wishlist(Base):
    __tablename__ = "wishlists"

    id = Column(Integer, primary_key=True)
    kinopoiskId = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    posterUrl = Column(String, nullable=False)

    owner_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )
    # __table_args__ = (
    #     UniqueConstraint(
    #         "owner_id",
    #         "kinopoiskId",
    #         name="uq_owner_movie"
    #     ),
    # )