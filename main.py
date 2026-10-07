import uvicorn
from blog.models import Base
from fastapi import FastAPI
from blog.database import engine
from blog.routers import blog, user, auth

app = FastAPI()
Base.metadata.create_all(engine)
app.include_router(auth.router)
app.include_router(blog.router)
app.include_router(user.router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
