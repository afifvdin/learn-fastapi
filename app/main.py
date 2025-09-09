from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference  # type: ignore

from app.core.settings import settings
from app.routes.user_routes import users_router

app = FastAPI(
    title=settings.APP_NAME, docs_url=settings.DOCS_URL, redoc_url=settings.REDOC_URL, openapi_url=settings.OPENAPI_URL
)

app.include_router(users_router)


@app.get("/scalar", include_in_schema=False)
async def scalar_html():
    if not app.openapi_url:
        raise ValueError("openapi_url is None")

    return get_scalar_api_reference(openapi_url=app.openapi_url, title=app.title)
