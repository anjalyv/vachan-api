# Deploy Vachan-api version-2 from scratch, using Docker

server: api.vachanengine.org(206.189.131.230)


## Stop existing services, if they are present
- vachan-api
- ngnix
- postgres(optional)
```
systemctl disable --now SERVICE-NAME
```

## For settingup Vachan-API repo

Decide a location and clone version-2 code(we have used /home/vachanproduction)

```
git clone --branch <branchname> <remote-repo-url>
git clone --branch version-2 https://github.com/Bridgeconn/vachan-api.git
```
After cloning, enter the following command to see the repo:
```
ls
```

If we need to remove the repo from the server using the following command:
```
rm -rf vachan-api

```

Next step is to include the `prod.env` file. First, navigate to the docker directory:
```
cd vachan-api
cd docker
touch prod.env

```
To add the required environmental variables in the `prod.env`  or `.env`  file.
```
nano prod.env

```

The environment values to be set in `prod.env` file and their expected format are:
```
VACHAN_SUPER_USERNAME="<super-admin-email-id>"
VACHAN_SUPER_PASSWORD="<a-strong-password>"
VACHAN_AUTH_DATABASE="postgresql://<DB-user>:<DB-passwords>@kratos-postgresd:<DB-port>/<DB-name>"
VACHAN_SUPPORT_EMAIL_CREDS="smtps://<email-id>:<password>:<email-service>:<smtp-port>/?skip_ssl_verify=true&legacy_ssl=true"
VACHAN_SUPPORT_EMAIL="<email-id>"
VACHAN_DOMAIN=api.vachanengine.org
VACHAN_KRATOS_PUBLIC_URL="http://api.vachanengine.org:4433/"
VACHAN_KRATOS_ADMIN_URL="http://api.vachanengine.org:4434/"
VACHAN_POSTGRES_PASSWORD="<a-strong-password>"
VACHAN_KRATOS_DB_USER="<vachan_auth_user>"
VACHAN_KRATOS_DB_PASSWORD="<a-strong-password>"
VACHAN_KRATOS_DB_NAME="<vachan_auth_db>"
VACHAN_GITLAB_TOKEN="<api-token-from-gitlab>"
VACHAN_REDIS_PASS="<a-strong-password>"
VACHAN_AI_DELETION_PERIOD=<no_of_days>
VACHAN_AI_CRON_DAY=<no_of_days>
VACHAN_AI_CRON_HOUR=<hour>
VACHAN_AI_CRON_MINUTE=<minute>
VACHAN_AI_DATA_PATH=<ai_data_path>
```

To see the contents of the `prod.env` file after editing, use the following command:
```
cat prod.env

```





## To install Docker and docker-compose

Prefered versions
docker: 24.0.1

For docker installation, if required
https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository

To avoid using `sudo` with Docker, follow these steps:
```
> sudo groupadd docker
> sudo usermod -aG docker $USER
> newgrp docker
> docker run hello-world #(to test)
```

If you encounter a `sudo permission denied` error, contact the server team for assistance.


## To start App

```
cd vachan-api/docker
```

For Staging:
```
docker compose -f docker-compose-staging.yml --profile deployment --env-file prod.env up --force-recreate --build -d
```

For Production:
```
docker compose -f docker-compose-production.yml --profile deployment --env-file prod.env up --force-recreate --build -d
```

Give correct path inside `web-server-with-cert` container inorder to avoid the errors related to the ssl path .
If you encounter ssl related errors, contact the server team for assistance.

## To Down the App

For Staging:

```
docker compose -f docker-compose-staging.yml --profile deployment --env-file prod.env down
```

For Production:

```
docker compose -f docker-compose-production.yml --profile deployment --env-file prod.env down
```


## Enable Auto deployment via github actions

### RSA Keys

```
> cd ~/.ssh # (cd ~ | mkdir .ssh , if not already present)
> ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
   # (name the file github-actions
   # dont give passphrase)
> cat github-actions.pub >> authorized_keys

```
refernce: https://zellwk.com/blog/github-actions-deploy/


### Add secrets in github

* VACHAN_DO_HOST = 206.189.131.230
* VACHAN_DO_USERNAME = gitautodeploy
* SSH_KEY 




## To Add SSL

Referenced article: 
https://mindsers.blog/post/https-using-nginx-certbot-docker/

Create an `ssl` folder in the home directory:

```
mkdir ssl
```

Copy the required files from your local machine to the RDS, then move them to the production server. You can use the `scp` or `mv` commands for this.



