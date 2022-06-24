# How to

```
cp .env.analysis.example .env.analysis # Make changes if you want
cp .env.hydra.example .env.datalake # Make changes if you want
./init.sh # Beware, download of catalog is desactivated by default, you have to uncomment it for the first time
docker-compose up --build -d
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
  - crawler

# Next

- [] Add csvapi (and maybe udata-search-service ?)
- [] Implement udata-kafka-event-testing into this repo  

