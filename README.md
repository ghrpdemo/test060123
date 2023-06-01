## Step 1 api using flask
tested with locally curl and works
```
curl -v -X GET http://localhost:5000/users

curl -v -X GET http://localhost:5000/users/1

curl -v -X POST http://localhost:5000/users curl -v -X POST http://localhost:5000/users -H 'Content-Type: application/json' -d '{"id":"6","name":"Jeff Bezo"}'
```
## Step 2 for local
run make services to start local postgres for the python app
this will import the csv and create db and table
```
 "make services"
```
## Step3 kubernetes manifests
im using kustomize here, it was faster to handle transforms/overrides for dev/stag/prod
the main thing here, is using init to prep db and using env var for overrides and secrets
```
to install postgres
from kustomize/postgres 
kubectl apply -k environments/prod

to install flaskapi
from kustomize/flaskapi
kubectl apply -k environments/prod
```
