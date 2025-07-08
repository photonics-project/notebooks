FROM debian:11-slim

RUN apt update && apt install -y \
    curl \
    gfortran \
    make

RUN curl -fsSL https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin/:$PATH"

COPY ./ /notebooks/
WORKDIR /notebooks/

RUN uv venv
ENV VIRTUAL_ENV="./.venv"
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN uv sync

RUN uv run make build

EXPOSE 8866

ENTRYPOINT ["voila", "--Voila.ip=0.0.0.0", "--port=8866", "--no-browser", "./build"]
