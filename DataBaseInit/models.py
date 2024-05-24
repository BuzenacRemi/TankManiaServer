from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import uuid

Base = declarative_base()
class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(16), unique=True, nullable=False)
    hashed_pass = Column(String, nullable=False)
    uuid = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)

    # Relationships
    ranks = relationship("Rank", back_populates="user")
    sessions = relationship("Session", back_populates="user")
    game_histories1 = relationship("GameHistory", foreign_keys="[GameHistory.uuid_player1]")
    game_histories2 = relationship("GameHistory", foreign_keys="[GameHistory.uuid_player2]")
    game_histories_winner = relationship("GameHistory", foreign_keys="[GameHistory.uuid_winner]")
    game_stats = relationship("GameStats", back_populates="user")


class Rank(Base):
    __tablename__ = 'rank'

    id = Column(Integer, primary_key=True, index=True)
    uuid_player = Column(UUID(as_uuid=True), ForeignKey('user.uuid'), unique=True, nullable=False)
    value = Column(Integer, nullable=False)

    # Relationships
    user = relationship("User", back_populates="ranks")

class Session(Base):
    __tablename__ = 'session'

    id = Column(Integer, primary_key=True, index=True)
    uuid_player = Column(UUID(as_uuid=True), ForeignKey('user.uuid'), nullable=False)
    session_key = Column(String(255), unique=True, nullable=False)
    expiration_date = Column(TIMESTAMP(timezone=True), nullable=False)

    # Relationships
    user = relationship("User", back_populates="sessions")

class GameHistory(Base):
    __tablename__ = 'game_history'

    id = Column(Integer, primary_key=True, index=True)
    uuid_player1 = Column(UUID(as_uuid=True), ForeignKey('user.uuid'), nullable=False)
    uuid_player2 = Column(UUID(as_uuid=True), ForeignKey('user.uuid'), nullable=False)
    uuid_winner = Column(UUID(as_uuid=True), ForeignKey('user.uuid'))

    # Relationships
    player1 = relationship("User", foreign_keys=[uuid_player1])
    player2 = relationship("User", foreign_keys=[uuid_player2])
    winner = relationship("User", foreign_keys=[uuid_winner])

class GameStats(Base):
    __tablename__ = 'game_stats'

    id = Column(Integer, primary_key=True, index=True)
    id_game = Column(Integer, ForeignKey('game_history.id'), nullable=False)
    uuid_player = Column(UUID(as_uuid=True), ForeignKey('user.uuid'), nullable=False)
    success_missiles = Column(Integer, nullable=False)
    missiles_launched = Column(Integer, nullable=False)
    damages_received = Column(Integer, nullable=False)
    movement_distance = Column(Integer, nullable=False)

    # Relationships
    game_history = relationship("GameHistory", back_populates="game_stats")
    user = relationship("User", back_populates="game_stats")