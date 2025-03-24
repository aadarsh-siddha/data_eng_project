FROM python:3.11

# Set the working directory
WORKDIR /app

# Copy the requirements file and install Python dependencies
COPY requirements.txt .
COPY resource_parser.py .
COPY notebooks/ notebooks/
RUN pip install --no-cache-dir -r requirements.txt

# Update apt-get and install default-jdk and wget (wget is needed for the download)
RUN apt-get update && apt-get install -y default-jdk wget && rm -rf /var/lib/apt/lists/*

# Download the jar file
RUN git clone https://github.com/synthetichealth/synthea.git
# Expose the port for the web server
EXPOSE 8080
# Set default command
CMD ["/bin/bash"]
