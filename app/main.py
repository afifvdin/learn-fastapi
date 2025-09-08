from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference
from app.settings import settings
from app.schema import User

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    docs_url=settings.DOC_URL,
    redoc_url=settings.REDOC_URL,
)


@app.get("/")
def hello():
    return {"message": "Hei mom!"}


@app.post("/user")
def create_user(user: User):
    return user


@app.get("/scalar", include_in_schema=False)
async def scalar_html():
    if not app.openapi_url:
        raise ValueError("openapi_url is None")

    return get_scalar_api_reference(openapi_url=app.openapi_url, title=app.title)
