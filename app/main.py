from fastapi import FastAPI
from .routers import posts, users, auth, votes
from fastapi.middleware.cors import CORSMiddleware

# This line is no longer needed, since we're using alembic
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"] # configure this once you build out the client-side web app; make it an env variable

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(votes.router)


@app.get('/')
def root():
    return {'message': 'Welcome to my api!!!'}
