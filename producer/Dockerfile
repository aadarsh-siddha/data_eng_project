FROM python:3.11

# Set the working directory
WORKDIR /app

# Copy the requirements file and install Python dependencies
COPY requirements.txt .
COPY notebooks/ notebooks/
COPY scripts/ scripts/
COPY resources/ resources/
COPY main_script.py .
COPY kafka_config.json config/
RUN pip install --no-cache-dir -r requirements.txt

# Update apt-get and install default-jdk and wget (wget is needed for the download)
RUN apt-get update && apt-get install -y default-jdk wget && rm -rf /var/lib/apt/lists/*

# Download the jar file
RUN git clone https://github.com/synthetichealth/synthea.git
# Expose Jupyter port
EXPOSE 8888

# Start Jupyter Notebook when container runs
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root", "--NotebookApp.token=''", "--NotebookApp.password=''"]
