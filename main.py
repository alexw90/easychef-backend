from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import uvicorn

app = FastAPI(title="Recipe API", description="API for managing recipes and ingredients")

# Data Models
class Ingredient(BaseModel):
    name: str
    amount: float
    unit: str

class Recipe(BaseModel):
    id: Optional[int] = None
    title: str
    description: str
    ingredients: List[Ingredient]
    instructions: List[str]
    prep_time: int  # in minutes
    cook_time: int  # in minutes
    servings: int
    difficulty: str
    tags: List[str]
    created_at: Optional[datetime] = None

# In-memory storage (replace with database in production)
recipes_db = {}
recipe_counter = 1

# API Endpoints
@app.post("/recipes/", response_model=Recipe, status_code=201)
async def create_recipe(recipe: Recipe):
    global recipe_counter
    recipe.id = recipe_counter
    recipe.created_at = datetime.now()
    recipes_db[recipe_counter] = recipe
    recipe_counter += 1
    return recipe

@app.get("/recipes/", response_model=List[Recipe])
async def list_recipes(
    skip: int = 0,
    limit: int = 10,
    tag: Optional[str] = None,
    difficulty: Optional[str] = None
):
    filtered_recipes = recipes_db.values()
    
    if tag:
        filtered_recipes = [r for r in filtered_recipes if tag in r.tags]
    if difficulty:
        filtered_recipes = [r for r in filtered_recipes if r.difficulty == difficulty]
    
    return list(filtered_recipes)[skip:skip + limit]

@app.get("/recipes/{recipe_id}", response_model=Recipe)
async def get_recipe(recipe_id: int):
    if recipe_id not in recipes_db:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipes_db[recipe_id]

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)