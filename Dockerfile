FROM python:3.11.4

# Install base dependences
RUN apt update \
    && apt install libpq-dev gcc python3-dev iputils-ping wait-for-it python3-venv -y \
    && pip install --upgrade pip \
    && apt-get install tzdata -y

# Set default timezone
ENV TZ=America/Sao_Paulo
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && dpkg-reconfigure -f noninteractive tzdata

# Create new user and set workdir
RUN useradd --create-home rinha_backend --groups www-data
USER 1000
WORKDIR /home/rinha_backend/rinha-de-backend-2023-q3-python-flask

# Install project dependences
COPY ./requirements.txt /home/rinha_backend/rinha-de-backend-2023-q3-python-flask/requirements.txt
RUN python -m venv venv
ENV PATH="/home/rinha_backend/rinha-de-backend-2023-q3-python-flask/venv/bin:$PATH"
RUN pip install -r /home/rinha_backend/rinha-de-backend-2023-q3-python-flask/requirements.txt

# Copy source code to container
COPY . /home/rinha_backend/rinha-de-backend-2023-q3-python-flask

# Set workdir from src/ and
WORKDIR /home/rinha_backend/rinha-de-backend-2023-q3-python-flask/src
USER root
RUN chmod +x init.sh
USER 1000

# Set entrypoint and run python project
ENTRYPOINT ["/bin/bash", "-c"]
CMD ["wait-for-it -h rinha_backend_redis_db -p 6379 --strict --timeout=300 -- \
      wait-for-it -h rinha_backend_postgres_db -p 5432 --strict --timeout=300 -- \
      wait-for-it -h rinha_backend_ngnix_server -p 80 --strict --timeout=300 -- \
      ./init.sh"]
