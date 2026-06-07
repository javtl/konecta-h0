from sqlalchemy import text
import asyncio
from datetime import datetime, timedelta
from uuid import uuid4
from app.db.database import AsyncSessionLocal, Base, engine
from app.models.db_models import User, Sparring, Vote, Ranking
import hashlib
import random

def hash_password(password: str) -> str:
    """Simple hash for seed data (not for production)."""
    return hashlib.sha256(password.encode()).hexdigest()

async def seed_database():
    """Populate database with test data."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as session:
        result = await session.execute(text("SELECT count(*) FROM users"))
        count = result.scalar()
        if count > 0:
            print("✅ Database already seeded, skipping...")
            return

        print("🌱 Seeding database...")
        users = []
        sports = ["BOXING", "MMA", "MUAY_THAI"]
        experiences = ["BEGINNER", "INTERMEDIATE", "ADVANCED"]
        gyms = ["Mi Gym Boxeo", "CrossFit Madrid", "MMA Elite"]

        for i in range(10):
            user = User(
                id=str(uuid4()),
                username=f"boxer_{i+1}",
                email=f"boxer{i+1}@konecta.local",
                hashed_password=hash_password("password123"),
                gym=random.choice(gyms),
                sport=random.choice(sports),
                weight=75 + random.randint(-10, 10),
                experience=random.choice(experiences),
                octagon={
                    "speed": random.randint(4, 9),
                    "defense": random.randint(4, 9),
                    "technique": random.randint(4, 9),
                    "power": random.randint(4, 9),
                    "cardio": random.randint(4, 9),
                    "adaptability": random.randint(4, 9),
                    "aggression": random.randint(4, 9),
                    "precision": random.randint(4, 9),
                },
                total_sparrings=random.randint(0, 20),
                wins=random.randint(0, 15),
                losses=random.randint(0, 10),
                ranking=1000 + random.randint(-200, 400),
            )
            users.append(user)
            session.add(user)

        await session.flush()  # Get IDs
        print(f"✅ Created {len(users)} users")
        sparrings = []
        for i in range(5):
            sparring = Sparring(
                id=str(uuid4()),
                challenger_id=users[i].id,
                opponent_id=users[i+1].id,
                scheduled_date=datetime.utcnow() + timedelta(days=random.randint(1, 10)),
                status=random.choice(["SCHEDULED", "COMPLETED", "VOTED"]),
                gym=users[i].gym,
                sport=users[i].sport,
                notes=f"Sparring test {i+1}",
            )
            if i > 2:
                sparring.status = "VOTED"
                sparring.challenger_vote = random.choice(["challenger", "opponent"])
                sparring.opponent_vote = sparring.challenger_vote  # Match for demo
                sparring.result = f"{sparring.challenger_vote.upper()}_WINS"
                sparring.voted_at = datetime.utcnow()

            sparrings.append(sparring)
            session.add(sparring)

        await session.flush()
        print(f"✅ Created {len(sparrings)} sparrings")
        for sparring in sparrings:
            if sparring.status == "VOTED":
                vote = Vote(
                    id=str(uuid4()),
                    sparring_id=sparring.id,
                    user_id=sparring.challenger_id,
                    vote=sparring.challenger_vote,
                )
                session.add(vote)

        await session.flush()
        print(f"✅ Created votes")
        for user in users:
            ranking = Ranking(
                id=str(uuid4()),
                gym=user.gym,
                user_id=user.id,
                username=user.username,
                ranking=user.ranking,
                wins=user.wins,
                losses=user.losses,
            )
            session.add(ranking)

        await session.flush()
        print(f"✅ Created {len(users)} rankings")
        await session.commit()
        print("\n✅ Database seeded successfully!")
        print(f"   - {len(users)} users")
        print(f"   - {len(sparrings)} sparrings")
        print(f"   - {len(users)} rankings")

async def main():
    await seed_database()

if __name__ == "__main__":
    asyncio.run(main())


