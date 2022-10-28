from fastapi import FastAPI
from demo_app import models
from demo_app.database import engine
from demo_app.routers import authentication
from fastapi.staticfiles import StaticFiles

from domain import db

"""
Creates an Object of FastAPI Instance as app with some Title and Description while viewing in
Swagger or ReadDoc mode.
"""

tags_metadata = [
    {
        "name": "Authentication",
        "description": "Operations with Authentication. It Consists of Registration | Login |"
                       " Forgot Password"
    },
]

app = FastAPI(
    title='Demo App',
    description='FastAPI Demo App System',
    version='1.0.0',
    terms_of_service='',
    contact={
        'name': 'DEEP SHAH',
        'email': 'deep.inexture@gmail.com'
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
    openapi_tags=tags_metadata
)

"""Allow Static Files to use in app via mounting"""
# app.mount("/templates", StaticFiles(directory="grocerystore/templates", html=True), name="templates")

"""Following command will create new tables if not exists in Database."""
"""Now We are using alembic migrations."""


# models.Base.metadata.create_all(engine)
db.init_db()


"""Following command will call the routers and stored in different files for clean flow of project ."""
app.include_router(authentication.router)

"""
Using following we can directly run python file instead of whole uvicorn command.
Don't use while of production server.
"""
# if __name__ == "__main__":
#     uvicorn.run(app, host="127.0.0.1", port=8000)