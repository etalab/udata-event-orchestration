# How to

```
cp analysis/.env.analysis.example analysis/.env.analysis # Make changes if you want
cp hydra/.env.hydra.example hydra/.env.hydra # Make changes if you want
cp csvapi/.env.csvapi.example csvapi/.env.csvapi # Make changes if you want
./get_source.sh # To execute services with source instead of pypi. NB : csvapi with kafka integration has no pypi package yet, you have to download source anyway.
docker-compose -f docker-compose-with-source.yml up --build -d  # if you want to execute with source
docker-compose -f docker-compose-with-pypi.yml up --build -d # if you want to execute with pypi packages
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
