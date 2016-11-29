# Set the base image
FROM python:2.7

# File Author / Maintainer
MAINTAINER cdevilly

# Update the sources list
RUN apt-get update

# Copy the application folder inside the container
ADD /app /app

# Get pip to download and install requirements:
RUN pip install -r /app/requirements.txt

# Copy the boto file into the container
ADD .boto /root/.boto

# Expose listener port
EXPOSE 8080

# Set the default directory where CMD will execute
WORKDIR /app
RUN mkdir /data
# Set the default command to execute    
# when creating a new container
CMD python app.py
