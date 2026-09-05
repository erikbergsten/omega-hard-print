FROM alpine:3.23

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN apk add glib
RUN apk add pango
RUN apk add font-dejavu

WORKDIR /app

COPY pyproject.toml .
RUN uv sync
COPY omega_hard_print omega_hard_print

WORKDIR /work

ENTRYPOINT ["/app/.venv/bin/python3", "-m", "omega_hard_print"]
