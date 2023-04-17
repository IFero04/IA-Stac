FROM python:3.9.15-slim

WORKDIR /app

# install nodemon
RUN apt update
RUN apt install curl -y
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash
RUN apt install nodejs
RUN npm install -g npm@9.2.0
RUN npm install -g nodemon

# install pg_config
RUN apt install libpq-dev -y
RUN apt install build-essential -y

# upgrade pip
RUN python -m pip install --upgrade pip

# install x11
RUN apt install -qqy x11-apps

# install pygame
RUN pip3 install pygame
RUN pip3 install opencv-python

# dependencies from requirements.txt
COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

CMD python main.py