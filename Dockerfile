# Use an official Python runtime as a parent image
FROM centos:default


# Set the working directory to /app
WORKDIR /test

# Copy the current directory contents into the container at /app
COPY . /test
#

RUN wget http://mirrors.jenkins.io/war-stable/latest/jenkins.war


RUN pip3 install -r requirements.txt -i https://pypi.douban.com/simple

# Make port 80 available to the world outside this container
EXPOSE 8001

# Define environment variable
ENV NAME World

# Run app.py when the container launches
#CMD ["python3", "ry"]
RUN cd /test
#RUN python3 manage.py runserver 0.0.0.0:8001

CMD ["java" ,"-jar", "jenkins.war", "--httpPort=8080"]
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8001"]
