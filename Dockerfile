# Use the official Python image from the Docker Hub
FROM python:3.12-slim

ARG APP_HOME=/app
ARG APP_PORT=8000

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR $APP_HOME

# Install dependencies required for building psycopg2
RUN apt-get update && apt-get install -y \
    libpq-dev \
    build-essential \
    gcc \
    && apt-get clean

# Copy the requirements file into the container
COPY ./requirements.txt .

# Install the dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port the app runs on
EXPOSE $APP_PORT

# Run the Django development server
CMD ["python", "app/manage.py", "runserver", "0.0.0.0:8000"]