from fastapi import FastAPI, Request
from scalar_fastapi import get_scalar_api_reference  # type: ignore
from starlette.middleware.sessions import SessionMiddleware
from starlette.templating import Jinja2Templates

from app.core.settings import settings
from app.routes.auth_routes import auth_router
from app.routes.post_routes import posts_router
from app.routes.user_routes import users_router
from app.tasks.email_tasks import send_email

templates = Jinja2Templates(directory="app/templates")

app = FastAPI(
    title=settings.APP_NAME, docs_url=settings.DOCS_URL, redoc_url=settings.REDOC_URL, openapi_url=settings.OPENAPI_URL
)

app.add_middleware(SessionMiddleware, secret_key=settings.JWT_SECRET)


app.include_router(users_router)
app.include_router(posts_router)
app.include_router(auth_router)


@app.get("/email")
def email():
    send_email.delay("afifudin.fdn@gmail.com", "Subject", "Body")
    return {"message": "Done sent email"}


@app.get("/")
def get_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "app_name": settings.APP_NAME})


@app.get("/scalar", include_in_schema=False)
async def scalar_html():
    if not app.openapi_url:
        raise ValueError("openapi_url is None")

    return get_scalar_api_reference(openapi_url=app.openapi_url, title=app.title)
