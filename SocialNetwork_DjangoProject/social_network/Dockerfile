# Stage 1: Build backend
FROM python:3.10-slim

# Assign the container's working directory.
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1



# CMD to run the Django app
CMD ["python", "manage.py", "runserver", "0.0.0.0:4200", "--settings=winnow.settings.develop"]