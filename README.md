# Caveman Honeypot

[c-honeypot-adminpanel](https://github.com/selmankon/c-honeypot-adminpanel) is the admin panel for this honeypot

---

docker tuto

1. [Docker Compose Build](#docker-compose-build) (recommended)
1. [Dockerfile Build](#docker-build)

---

## Docker Compose Build

```bash
docker-compose build --no-cache
```

`--no-cache`: build without cache

## Docker Compose Up/Down

```bash
docker-compose up -d
```

`-d`: run in background

```bash
docker-compose down
```

---

## Docker Build

```bash
docker build --no-cache -t c-honeypot .
```

`--no-cache`: build without cache\
`-t`: tag name\
`c-honeypot`: image name\
`.`: build context

## Docker Run

```bash
docker run --rm -d -p 45300:65400 --name=honeypot1 c-honeypot
```

`--rm`: remove container when it exits\
`-d`: run in background\
`-p`: port mapping. `45300` is the host port, `65400` is the container port\
`--name`: container name\
`c-honeypot`: image name

## Docker Stop

```bash
docker stop honeypot1
```

`honeypot1`: container name

## Docker Remove

### Remove Container

```bash
docker rm honeypot1
```

`honeypot1`: container name

### Remove Image

```bash
docker rmi c-honeypot
```

`c-honeypot`: image name
