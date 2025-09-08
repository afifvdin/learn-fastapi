FROM ghcr.io/astral-sh/uv:debian

WORKDIR /app

COPY . . 

RUN uv sync

EXPOSE 8000

CMD ["sh", "-c", "make db-up && make dev"]