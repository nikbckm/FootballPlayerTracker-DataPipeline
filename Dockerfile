# Use a Python base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the data generator script
COPY data_generator.py /app/

# Install required Python packages
RUN pip install kafka-python

# Run the data generator script
CMD ["python", "data_generator.py"]
