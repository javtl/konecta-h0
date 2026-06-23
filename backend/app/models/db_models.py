from app.db.database import Base
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON, Text, Boolean, Index
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base
import uuid

class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String(100), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Profile
    gym = Column(String(100), index=True, nullable=True)
    sport = Column(String(50), nullable=False)  # BOXING, MMA, MUAY_THAI
    weight = Column(Integer, nullable=False)  # kg
    experience = Column(String(50), nullable=False)  # BEGINNER, INTERMEDIATE, ADVANCED

    # Octagon: 8 atributos de 0-10
    octagon = Column(JSON, default={
        "speed": 5,
        "defense": 5,
        "technique": 5,
        "power": 5,
        "cardio": 5,
        "adaptability": 5,
        "aggression": 5,
        "precision": 5,
    })

    # Stats
    total_sparrings = Column(Integer, default=0)
    wins = Column(Integer, default=0)
    losses = Column(Integer, default=0)
    ranking = Column(Integer, default=1000)  # ELO score
    last_sparring = Column(DateTime, nullable=True)

    # Relationships
    sparrings_challenger = relationship("Sparring", foreign_keys="Sparring.challenger_id", back_populates="challenger")
    sparrings_opponent = relationship("Sparring", foreign_keys="Sparring.opponent_id", back_populates="opponent")

    # Índices compuestos para búsquedas rápidas
    __table_args__ = (
        Index('idx_sport_weight', 'sport', 'weight'),
        Index('idx_users_gym_ranking', 'gym', 'ranking'),
    )

    def __repr__(self):
        return f"<User {self.username}>"


class Sparring(Base):
    __tablename__ = "sparrings"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    challenger_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    opponent_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    scheduled_date = Column(DateTime, nullable=False)
    status = Column(String(50), default="SCHEDULED", nullable=False)  # SCHEDULED, COMPLETED, VOTED

    # Voting
    challenger_vote = Column(String(50), nullable=True)  # "challenger" or "opponent"
    opponent_vote = Column(String(50), nullable=True)
    voted_at = Column(DateTime, nullable=True)
    result = Column(String(50), nullable=True)  # "CHALLENGER_WINS", "OPPONENT_WINS", "DISPUTED"

    # Details
    gym = Column(String(100), nullable=False, index=True)
    sport = Column(String(50), nullable=False)
    notes = Column(Text, nullable=True)

    # Relationships
    challenger = relationship("User", foreign_keys=[challenger_id], back_populates="sparrings_challenger")
    opponent = relationship("User", foreign_keys=[opponent_id], back_populates="sparrings_opponent")
    votes = relationship("Vote", back_populates="sparring")

    __table_args__ = (
        Index('idx_status_scheduled', 'status', 'scheduled_date'),
        Index('idx_gym_sport', 'gym', 'sport'),
    )

    def __repr__(self):
        return f"<Sparring {self.id}>"


class Vote(Base):
    __tablename__ = "votes"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    sparring_id = Column(String(36), ForeignKey("sparrings.id"), nullable=False, index=True)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    vote = Column(String(50), nullable=False)  # "challenger" or "opponent"
    voted_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    sparring = relationship("Sparring", back_populates="votes")

    __table_args__ = (
        Index('idx_sparring_user', 'sparring_id', 'user_id'),
    )

    def __repr__(self):
        return f"<Vote {self.sparring_id}>"


class Ranking(Base):
    __tablename__ = "rankings"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    gym = Column(String(100), nullable=False, index=True)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, unique=False)
    username = Column(String(100), nullable=False)
    ranking = Column(Integer, nullable=False)
    wins = Column(Integer, default=0)
    losses = Column(Integer, default=0)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index('idx_users_gym_ranking', 'gym', 'ranking'),
        Index('idx_gym_user', 'gym', 'user_id'),
    )

    def __repr__(self):
        return f"<Ranking {self.username}: {self.ranking}>"