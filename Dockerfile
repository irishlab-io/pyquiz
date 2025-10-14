##  Builder Stage  ##
FROM python:latest AS builder

ENV UV_VERSION="0.8.13"

RUN apt-get update && \
    apt-get install --no-install-recommends -y \
    build-essential curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ADD https://astral.sh/uv/${UV_VERSION}/install.sh /install.sh
RUN chmod -R 755 /install.sh && /install.sh && rm /install.sh
  
ENV PATH="/root/.local/bin:${PATH}"

WORKDIR /app
   
COPY ./pyproject.toml .

RUN uv sync

##  Production Stage  ##
  
FROM python:latest AS production

RUN useradd --create-home appuser
USER appuser

WORKDIR /app

COPY --from=builder /app/.venv .venv
COPY . .
  
ENV PATH="/app/.venv/bin:$PATH"

CMD ["python", "apps/main.py"]