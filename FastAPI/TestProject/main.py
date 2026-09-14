from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI(
    title="Mini Game API",
    description="First Project on FastAPI",
    version="1.0.0",
)

class GameCreate(BaseModel):
    title: str = Field(min_length=2, max_length=100)
    genre: str = Field(min_length=2, max_length=50)
    price: float = Field(ge=0)

games = [
    {
        "id": 1,
        "title": "Cyberpunk 2077",
        "genre": "RPG",
        "price": 29.99,
    },
    {
        "id": 2,
        "title": "DOOM Eternal",
        "genre": "FPS",
        "price": 19.99,
    },
    {
        "id": 3,
        "title": "The Witcher 3",
        "genre": "RPG",
        "price": 19.99,
    },
]

@app.get("/")
def root():
    return {"message": "Mini Game API is running"}

@app.get("/games")
def get_games():
    return games

@app.get("/games/{game_id}")
def get_game(game_id: int):
    for game in games:
        if game["id"] == game_id:
            return game

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Game not found",
    )

@app.post("/games", status_code=status.HTTP_201_CREATED)
def create_game(game:GameCreate):
    next_id = max((item["id"] for item in games), default=0) + 1

    new_game ={
        "id": next_id,
        "title":game.title,
        "genre": game.genre,
        "price":game.price
    }

    games.append(new_game)
    return new_game
