from typing import List

from pydantic import BaseModel, Field


class Ingredient(BaseModel):
    name: str = Field(..., description="Name of the ingredient")
    weight: float = Field(..., ge=0.1, description="Weight of the ingredient in gram")


class Recipes(BaseModel):
    title: str = Field(
        ..., min_length=1, max_length=100, description="Title of the recipe"
    )
    time_cooking: int = Field(..., gt=0, description="Time cooking in min")
    ingredients: List[Ingredient] = Field(..., description="List of ingredients")
    description: str = Field(
        ..., min_length=1, max_length=1000, description="Description of recipe"
    )


class RecipesIn(Recipes): ...


class RecipesOut(Recipes):
    id: int

    class Config:
        from_attributes = True
