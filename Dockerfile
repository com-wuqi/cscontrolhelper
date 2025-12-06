FROM python:3.13-slim AS builder

WORKDIR /apps

# RUN pip config set global.index-url https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple

COPY requirements.txt .

RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --user --no-cache-dir -r requirements.txt

FROM python:3.13-slim

RUN apt-get update && apt-get install -y wait-for-it curl ca-certificates && rm -rf /var/lib/apt/lists/*

RUN adduser --disabled-password --gecos "" appuser && \
    mkdir -p /home/appuser/.local && \
    chown -R appuser:appuser /home/appuser

USER appuser
WORKDIR /apps

# 从构建阶段复制依赖
COPY --from=builder --chown=appuser:appuser \
     /root/.local /home/appuser/.local

ENV PATH=/home/appuser/.local/bin:$PATH

COPY --chown=appuser:appuser . .

HEALTHCHECK --interval=10s --timeout=5s --retries=3 --start-period=15s \
  CMD curl -f http://localhost:8000/health || exit 1

EXPOSE 8000

CMD ["sh", "-c","wait-for-it.sh", "host.docker.internal:3306", "--","fastapi", "run", "main.py", "--host", "0.0.0.0", "--port", "8000"]
