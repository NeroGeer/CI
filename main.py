import logging
from contextlib import asynccontextmanager
from typing import Optional

import uvicorn
from fastapi import FastAPI, HTTPException
from sqlalchemy.future import select

import models as models
import schemas as schemas
from database import SessionDep, engine
a
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Код при старте приложения (startup)
    logger.info("Starting up application...")
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)
    logger.info("Database tables created.")
    yield
    logger.info("Shutting down application...")
    # Код при завершении работы приложения (shutdown)
    await engine.dispose()
    logger.info("Database engine disposed.")


logger = logging.getLogger(__name__)
app = FastAPI(lifespan=lifespan)


@app.post("/recipes", response_model=schemas.RecipesOut)
async def create_recipes(data: schemas.RecipesIn, session: SessionDep):
    logger.info("Creating recipes...")
    recipe_dict = data.model_dump()  # или recipe.model_dump() для Pydantic v2
    new_recipes = models.Recipes(**recipe_dict)
    session.add(new_recipes)
    await session.commit()
    return new_recipes


@app.get("/recipes/")
async def get_recipes(session: SessionDep, idx: Optional[int] = None):

    if idx is not None:
        query = select(models.Recipes).where(models.Recipes.id == idx)
        result = await session.execute(query)
        recipe = result.scalars().first()
        if not recipe:
            raise HTTPException(status_code=404, detail="Recipe not found")

        recipe.popularity += 1
        await session.commit()
        return recipe

    else:
        query = select(models.Recipes)
        result = await session.execute(query)
        return result.scalars().all()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    uvicorn.run("main:app", host="127.0.0.1", port=8000)
