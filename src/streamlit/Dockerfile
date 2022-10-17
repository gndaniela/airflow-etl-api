FROM python:3.7

EXPOSE 8501

WORKDIR /code

COPY requirements.txt ./

RUN apt-get update && apt-get install -y \
    build-essential \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install -r requirements.txt

COPY . /code

CMD ["streamlit","run", "streamlit.py"]