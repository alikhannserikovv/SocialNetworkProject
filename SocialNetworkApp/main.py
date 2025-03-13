from fastapi import FastAPI
from routers import user, profile, post, comment, lenta
import models
from database import engine

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(user.router)
app.include_router(profile.router)
app.include_router(post.router)
app.include_router(comment.router)
app.include_router(lenta.router)
