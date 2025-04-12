# Base image
FROM ubuntu:24.04

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    bzip2 \
    ca-certificates \
    libglib2.0-0 \
    libxext6 \
    libsm6 \
    libxrender1 \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Miniconda
ENV CONDA_DIR /opt/conda
RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh && \
    /bin/bash ~/miniconda.sh -b -p $CONDA_DIR && \
    rm ~/miniconda.sh && \
    $CONDA_DIR/bin/conda clean -tipsy && \
    ln -s $CONDA_DIR/etc/profile.d/conda.sh /etc/profile.d/conda.sh && \
    echo ". $CONDA_DIR/etc/profile.d/conda.sh" >> ~/.bashrc && \
    echo "conda activate TradingSystem" >> ~/.bashrc

# Add Conda to PATH
ENV PATH $CONDA_DIR/bin:$PATH

# Copy environment.yml
COPY environment.yml /tmp/environment.yml

# Create Conda environment
RUN conda env create -f /tmp/environment.yml

# Activate Conda environment & install pip packages
RUN echo "conda activate TradingSystem" >> ~/.bashrc && \
    /bin/bash -c "source ~/.bashrc && pip install gunicorn==23.0.0 packaging==24.2 redis==5.2.1"

# Set working directory
WORKDIR /app

# Copy application files
COPY . /app

# Expose Flask port (adjust if needed)
EXPOSE 5000

# Run the Flask app with Gunicorn (adjust entrypoint as needed)
CMD ["/bin/bash", "-c", "source ~/.bashrc && gunicorn --bind 0.0.0.0:5000 app:app"]
