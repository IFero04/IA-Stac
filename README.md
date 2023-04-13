# Artificial Intelligence | Informatics Engineering [@IPVC/ESTG](https://www.ipvc.pt/estg/)  #
Teachers: [Jorge Ribeiro](mailto:jribeiro@estg.ipvc.pt) and [Luís Teófilo](mailto:luisteofilo@estg.ipvc.pt)
___
### Introduction ###

The base code to create games in Python, using a Docker environment

### How to I setup my development environment? ###

* Install [Docker Desktop](https://www.docker.com/products/docker-desktop/)
* Build the Docker Image by running the following command in the project's root folder:
```
docker-compose build
```

### Where do I indicate Python dependencies? ###

* Use the file **requirements.txt**
* You need to rebuild the image if dependencies are changed before the next run. The command is the same as build.
```
docker-compose build
```

### How to I run my app? ###

* Run in a separate container (the *--rm* flag will clean up the container once done):
```
docker compose run --rm app
```
* Alternatively, you can use the *up* command
```
docker compose up --build
```
* Run a specific file *example.py*:
```
docker compose run --rm app python example.py
```
* Run a specific file *example.py* in **watch mode**:
```
docker compose run --rm app nodemon example.py
```