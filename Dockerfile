FROM python:3.9-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir Flask Faker

RUN python datagen.py

CMD ["python", "Dwarf_In_The_Flask.py"]

EXPOSE 5000
