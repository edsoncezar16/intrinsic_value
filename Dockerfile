FROM python:3.12-slim

WORKDIR /app

COPY /app/requirements.txt .

RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY /app .

EXPOSE 8501

ENTRYPOINT [ "streamlit", "run", "Intrinsic.py", "--server.address=0.0.0.0"]
