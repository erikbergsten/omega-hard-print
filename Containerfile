FROM alpine:latest
COPY --from=docker.io/astral/uv:latest /uv /uvx /bin/

run apk add glib pango fontconfig ttf-dejavu

workdir /app
copy pyproject.toml .
run uv sync

#copy omega_hard_print omega_hard_print
