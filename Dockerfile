# Use an official Python runtime as the base image
FROM python:3.11

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

RUN export $(cat .env)

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project code into the container
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose the port on which the Django app will run
EXPOSE 8002

# Start the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8002"]
