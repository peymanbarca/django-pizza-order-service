# Start from the official Python base image.
FROM python:3.9

# Set the current working directory
WORKDIR /django-pizza-order-service

# Copy the file with the requirements to the target directory.
COPY ./requirements.txt /django-pizza-order-service/requirements.txt

# Install the package dependencies in the requirements file.
RUN pip install --no-cache-dir --upgrade -r /django-pizza-order-service/requirements.txt

# Copy the ./ directory inside the /code directory.
COPY . /django-pizza-order-service

# Run the command to perform db migrate
RUN cd /django-pizza-order-service && make makemigrations
RUN cd /django-pizza-order-service && make migrate

# Run the command to collect static files (for Swagger)
RUN cd /django-pizza-order-service && make collectstatic

# Set the command to run the server.
CMD ["cd", "/django-pizza-order-service", "make", "server"]