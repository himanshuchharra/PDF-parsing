# Use an official Python runtime as an image
FROM python:3.6
MAINTAINER madhur.tandon@biz2credit.com <madhur.tandon@biz2credit.com>

# Update the Debian and Install Package
RUN apt-get update
RUN apt-get install -y pdftohtml

# Sets the working directory for following COPY and CMD instructions
# Notice we haven’t created a directory by this name - this
# instruction creates a directory with this name if it doesn’t exist
WORKDIR /app

# Install any needed packages specified in requirements.txt
COPY .env /app
COPY requirements.txt /app
COPY app/ /app
RUN pip install -r requirements.txt

# Run app.py when the container launches
CMD python app.py