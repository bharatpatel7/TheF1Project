# Step 1: Use the official Python image from Docker Hub
FROM python:3.9-slim

# Step 2: Set the working directory inside the container
WORKDIR /app

# Step 3: Copy the current directory contents into the container
COPY . /app

# Step 4: Install required Python libraries from requirements.txt
COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Set environment variable to prevent Python from writing .pyc files to disc
ENV PYTHONUNBUFFERED 1

# Step 6: Set the environment variable to ensure that Python output is sent straight to the terminal without buffering
ENV PYTHONUNBUFFERED 1

# Step 7: Run your application (optional)
CMD ["python", "visual.py"]
