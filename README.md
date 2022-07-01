# How to

```
cp .env.analysis.example .env.analysis # Make changes if you want
cp .env.hydra.example .env.hydra # Make changes if you want
cp .env.csvapi.example .env.csvapi # Make changes if you want
./get_source.sh # To execute services with source instead of pypi. NB : csvapi with kafka integration has no pypi package yet, you have to download source anyway.
docker-compose up -f docker-compose-with-source.yml --build -d # if you want to execute with source
docker-compose up -f docker-compose-with-pypi.yml --build -d # if you want to execute with pypi packages
```

# Services

- kafka with zookeeper
- minio
- hydra service :
  - redis
  - postgres
  - consumer kafka
  - crawler
- analysis service :
  - redis
  - consumer kafka
  - worker
- csvapi service
  - server # localhost:8000
  - consumer
