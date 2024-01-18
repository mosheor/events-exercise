# Inspiered by https://medium.com/@albertazzir/blazing-fast-python-docker-builds-with-poetry-a78a66f5aed0
FROM python:3.12.0-slim AS builder

# Install poetry and needed dependencies for instalion
RUN apt-get update && apt-get install -y curl && apt-get clean && \
    curl -sSL https://install.python-poetry.org | python3 -

# Set environment variables for poetry that will make poetry install dependencies in the project directory
ENV PATH="/root/.local/bin:$PATH" \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

# we don't need the real md file, but poetry needs it to install dependencies
RUN touch readme.MD

# copy only requirements to cache them in docker layer
COPY pyproject.toml poetry.lock ./
# Install dependencies adn copy auth secrets for our private repo
RUN --mount=type=secret,id=auth_toml,target=/root/.config/pypoetry/auth.toml \
    poetry install --no-root --only main  && \
    rm -rf $POETRY_CACHE_DIR

FROM python:3.12.0-slim AS runtime

ENV VIRTUAL_ENV="/app/.venv" \
    PATH="/app/.venv/bin:$PATH"

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

COPY ./evidence_handler ./evidence_handler

EXPOSE 8000

CMD ["uvicorn", "evidence_handler.app:app", "--port" ,"8000", "--host", "0.0.0.0"]
