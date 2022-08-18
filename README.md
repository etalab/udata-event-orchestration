# How to

```
cp config/.env.analysis.example config/.env.analysis # Make changes if you want
cp config/.env.hydra.example config/.env.hydra # Make changes if you want
cp config/.env.csvapi.example config/.env.csvapi # Make changes if you want
./get_source.sh # To execute services with source instead of pypi. NB : csvapi with kafka integration has no pypi package yet, you have to download source anyway.
docker-compose -f docker-compose-shared.yml -f docker-compose-with-source.yml up --build -d  # if you want to execute with source
docker-compose -f docker-compose-shared.yml -f docker-compose-with-pypi.yml up --build -d # if you want to execute with pypi packages
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

# Tooling

You can install the udata event orchestration package for udata event tooling.
```
pip install -e .
```

Now you can use `uket` cli to produce or consume particular messages.
Example to produce a `resource.created` message:
```
uket produce -t resource.created
```
Message type will be prompted for you to pick one.

You can easily consume any topic registered in `messages.json` by running:
```
uket consume
```

# Testing

After installing udata event orchestration package, you can run end-to-end tests.

Make sure you have your docker-compose with all services running and run:
```
pip install pytest
pytest tests/
```

We assume a default `SLEEP_BETWEEN_BATCHES` of 60 seconds for `udata-hydra` crawler.
If you have a different value, you can set it to make sure to wait the corresponding time, ex:
```
SLEEP_BETWEEN_BATCHES=10 pytest
```

 ## TODO
Clean hydra db after running tests (checks and catalog) -> else `resource.checked` is not sent.
Meanwhile you need to clean the corresponding entries manually in Postgres.
We could also add a dummy hash to the url to make sure that it gets recrawled `http://my_url.com/data.csv?_=dummy_hash`,
but we would add useless entries to our catalog.
