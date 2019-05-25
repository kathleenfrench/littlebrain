
## docker db setup

```
docker run -d -p 27017:27017 --name littlebrain_db -e MONGO_INITDB_ROOT_USERNAME=mongoadmin -e MONGO_INITDB_ROOT_PASSWORD=secret mongo
```

## TODO

- install as cli or flask app