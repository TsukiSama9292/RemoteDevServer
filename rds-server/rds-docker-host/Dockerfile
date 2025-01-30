FROM ubuntu:jammy-20240911.1

############################################################

RUN apt-get update && \
    apt-get install -y \
    wget \
    bzip2 \
    ca-certificates \
    curl \
    git \
    build-essential \
    python3-dev \
    docker.io

RUN apt-get clean && rm -rf /var/lib/apt/lists/*

RUN wget -qO /tmp/miniconda.sh https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh && \
    bash /tmp/miniconda.sh -b -p /opt/conda && \
    rm /tmp/miniconda.sh

ENV PATH /opt/conda/bin:$PATH
RUN conda init
RUN conda create -n workspace python=3.10 -y
ENV PATH /opt/conda/envs/workspace/bin:$PATH
RUN echo "conda activate workspace" >> ~/.bashrc
ENV PYTHONDONTWRITEBYTECODE=1
RUN mkdir /app

############################################################

# 安裝 FastAPI 依賴
RUN pip install --quiet 'fastapi==0.115.6'
RUN pip install --quiet 'pydantic==2.10.4'
RUN pip install --quiet 'uvicorn==0.34.0'
RUN pip install --quiet 'gunicorn==23.0.0'
RUN pip install --quiet 'python-multipart==0.0.20'
RUN pip install --quiet 'pytest==8.3.4'
RUN pip install --quiet 'pytest-asyncio==0.25.1'
RUN pip install --quiet 'docker==7.1.0'
RUN pip install --quiet 'python-dotenv==1.0.1'