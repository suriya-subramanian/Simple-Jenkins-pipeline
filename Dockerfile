FROM python:3.12
WORKDIR /app
RUN pip install --no-cache-dir fastapi uvicorn
COPY main.py ./
RUN useradd app
USER app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3000"]
EXPOSE 3000
