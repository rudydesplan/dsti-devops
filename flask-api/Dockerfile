# Use the official Python base image
FROM python:3.12.0a7 as builder

# Set the working directory
WORKDIR /app

# Copy requirements file
COPY ./requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Copy the rest of the application code
COPY ./setup.py .
COPY ./modules ./modules
COPY ./service ./service

# Install the application
RUN python setup.py install

# Remove unnecessary files to reduce image size
RUN find /app -name '*.pyc' -type f -delete

# --- Stage 2: Runtime image ---
FROM python:3.12.0a7

# Set the working directory
WORKDIR /app

ENV DATASET_LOCATION="app/datasets/avocado.csv"

# Copy installed packages and application from the builder stage
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /app/service /app/service

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run the application
CMD ["python", "service/service.py"]
