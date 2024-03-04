# set base image
FROM python:latest

# set the working directory in container
WORKDIR /code

# copy the dependencies file to the working directory
COPY requirements.txt .

# install dependencies
RUN pip install -r requirements.txt

# copy the content of local src directory to the working directory
COPY src/ .

# command to run on container start
CMD ["python", "./app.py"]
