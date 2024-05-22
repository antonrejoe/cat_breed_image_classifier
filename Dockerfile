# # start by pulling the python image
# FROM python:3.11

# # switch working directory
# RUN mkdir /app

# WORKDIR /app


# # copy every content from the local file to the image
# COPY . .

# RUN python -m pip install --upgrade pip

# RUN pip install -r requirements.txt
# # configure the container to run in an executed manner

# CMD ["python","upload.py" ]


# Use slim Python base image
FROM python:3.11-slim AS builder

# Create working directory
WORKDIR /app

# Copy only requirements file first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
    && pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get remove -y build-essential \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

# Copy the rest of the application
COPY . .

# Runtime image
FROM python:3.11-slim

WORKDIR /app

# Copy only necessary files from the builder stage
COPY --from=builder /usr/local/lib/python3.11/site-packages/ /usr/local/lib/python3.11/site-packages/
COPY --from=builder /app .

# Command to run the application
CMD ["python", "upload.py"]
