from database.models import async_session
from database.models import User, Group
from sqlalchemy import select, update, delete


async def set_user(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id))
            await session.commit()


async def get_all_user_ids():
    async with async_session() as session:
        result = await session.execute(select(User.tg_id))
        user_ids = result.scalars().all()  # Returns a list of tg_id values
        return user_ids
    
async def set_group(group_id):
    async with async_session() as session:
        user = await session.scalar(select(Group).where(Group.tg_id == group_id))

        if not user:
            session.add(Group(tg_id=group_id))
            await session.commit()


            
async def get_all_groups_ids():
    async with async_session() as session:
        result = await session.execute(select(Group.tg_id))
        user_ids = result.scalars().all()  # Returns a list of tg_id values
        return user_ids