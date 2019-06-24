# Use an official Python runtime as a parent image
FROM python:3.6-slim


# Set the working directory to /app
WORKDIR /test

# Copy the current directory contents into the container at /app
COPY . /test
#
RUN apt-get -y update
RUN apt-get install gcc
# Install any needed packages specified in requirements.txt

RUN pip3 install -r requirements.txt -i https://pypi.douban.com/simple

# Make port 80 available to the world outside this container
EXPOSE 8080

# Define environment variable
ENV NAME World

# Run app.py when the container launches
#CMD ["python3", "ry"]
RUN python3 runserver 0.0.0.0:8001