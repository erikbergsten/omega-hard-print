FROM alpine:3.23

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN apk add glib
RUN apk add pango
RUN apk add font-dejavu

WORKDIR /app

COPY pyproject.toml .
COPY omega_hard_print omega_hard_print

ENV PATH=$PATH:/root/.local/bin

RUN uv tool install .

WORKDIR /work

ENTRYPOINT ["omega-hard-print"]
