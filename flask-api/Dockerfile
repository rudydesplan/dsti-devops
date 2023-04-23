# Use the official Python base image
FROM python:3.12.0a7

# Set the working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt

# Copy the rest of the application code
COPY setup.py
COPY modules ./modules
COPY service ./service

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Install the application
RUN python setup.py install
    
# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run the application
CMD ["python", "service/service.py"]
