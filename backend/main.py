from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from utils.outline import generate_outline
from classes.cache import SemanticCache

app = FastAPI()
cache = SemanticCache(redisHost="localhost", redisPort=6379)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Hello FastAPI!"}

@app.get("/generate-outline")
def get_generated_outline(topic: str):
    generated_outline = cache.getOrGenerate(topic, lambda: generate_outline(topic))
    return {"outline": generated_outline}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)



#docker run -d --name redis-stack -p 6379:6379 redis/redis-stack
