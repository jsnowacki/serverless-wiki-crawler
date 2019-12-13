# serverless-wiki-crawler

Wikipedia crawler example using Serverless

## Required software

To run this repo you'll need:

1. Install Node.js https://nodejs.org/ 
2. Install Serverless https://serverless.com/framework/docs/getting-started/
3. Install Python distribution, e.g. Anaconda https://www.anaconda.com/download/
4. Install your favorite Python ID, e.g. VSCode https://code.visualstudio.com/; support for JavaScript, NodeJS, YAML etc. is a plus.
5. Install Git https://git-scm.com/
6. Register on AWS https://aws.amazon.com/ and install AWS CLI; you should not surpass the free tier.
7. For Windows 10 users it is useful to have Ubuntu for Windows https://tutorials.ubuntu.com/tutorial/tutorial-ubuntu-on-windows#0
8. For deployment package builder it is good to have Docker installed (https://www.docker.com/get-started) along with Serverless Python Requirements Plugin (https://www.npmjs.com/package/serverless-python-requirements)

To install required plugins type:

```bash
npm install 
```

### Resolving Docker Toolbox Daemon Is Not Running Error (Windows)

The way to fix Docker Toolbox daemon error is to set a number of environment variables, as follows:

```cmd
SET DOCKER_TLS_VERIFY=1
SET DOCKER_HOST=tcp://192.168.99.100:2376
SET DOCKER_CERT_PATH=%USERPROFILE%\.docker\machine\machines\default
SET DOCKER_MACHINE_NAME=default
SET COMPOSE_CONVERT_WINDOWS_PATHS=true
```

`%USERPROFILE%` should point to your home directory (you can check it using `echo %USERPROFILE%`); if it is not set correctly, change manually to your home in `DOCKER_CERT_PATH` given above.

The description is taken from https://www.mydatahack.com/resolving-docker-deamon-is-not-running-error-from-command-prompt/

## Serverless framework usage

To check the package content use:

```bash
sls info
```

To deploy the functions to AWS Lambda use the following command:

```bash
sls deploy -v
```

To test the function `wiki` you can do it in local mode:

```bash
sls invoke local -f wiki -d "{\"lang\": \"pl\"}"
```

of with the test file

```bash
sls invoke local -f wiki -p tests/wiki_test.json
```

Similarly, you can invoke deployed function on AWS Lambda:

```bash
sls invoke -f wiki -p tests/wiki_test.json -l
```

Note that without `-l` the logging will not be shown.

To see the logs from the deployed function `wiki` use the following command:

```bash
sls logs -f wiki
```

### Note on building

There are occasionally some issues with using `serverless-python-requirements` plugin using Docker, especially on Windows. You can use the plugin with option `dockerizePip: false` and use local Python (in this case executable `python3.7`) for zip creation; on Windows it is best to use Ubuntu for Windows, as the target image on AWS is Linux. 

If you want to use Docker build, which is best if you use packages requiring compilation(e.g. `numpy`), set `dockerizePip: true`, on Windows `dockerizePip: non-linux`.

## Docker

Alternatively, you can containerize your function using Docker as a web service, in this case using Flask. This can be used in many container orchestration systems like [Kubernetes](https://kubernetes.io/) and similar. Note that the service is simpler and just returns the crawled data; you need to handle data adding yourself either in the crawler service or as a separate service. See `app.py` and `Dockerfile` for details.

To build the service on your machine use the build command, e.g.:

```bash
docker build -t wiki-crawler .
```

To run the service use the run command, e.g.:

```bash
docker run -p 8080:8080 wiki-crawler
```

You can push the image to the repository of your choosing if it works correctly, see [the documentation](https://docs.docker.com/engine/reference/commandline/push/) for details.

## Google Cloud Run

Recently number of providers added an option to run Docker containers in a serverless fashion. One of them is [Google Cloud Run](https://cloud.google.com/run/), which is effectively managed version of [Knative](https://knative.dev/). It allows for easy shipping of Docker containers, scales them up and down, even to 0, an allows for event triggering; see the respective products' documentation for details.

Before deployment you need to build your image and ship it to a container registry, like the [Google Cloud](https://cloud.google.com/container-registry/) one.

To use Google Cloud you need to register and get the account. Also, you need to get the Google Cloud SDK, see [the documentation](https://cloud.google.com/sdk/docs/quickstarts) for details.  

Build the docker locally with the below naming scheme.

```bash
docker build -t gcr.io/$PROJECT_ID/wiki-crawler .
```

Where `PROJECT_ID` is your Google Cloud Project project ID; you can get it via Google Cloud SDK:

```bash
export PROJECT_ID=$(gcloud config get-value project)
```

You can test the image the same way as before locally; note the name change.

```bash
docker run -p 8080:8080 gcr.io/$PROJECT_ID/wiki-crawler
```

Before pushing the image the the registry you may need to setup the authentication for docker via the below command.

```bash
gcloud auth configure-docker
```

You should now be able to push the image to the registry using the command.

```bash
docker push gcr.io/$PROJECT_ID/wiki-crawler
```

To deploy the cloud run you need to use `gcloud`; see [quick start manual](https://cloud.google.com/run/docs/quickstarts/build-and-deploy) for details. To deployed the pushed image use the command as below; it will ask you few questions about the deployment.

```bash
gcloud beta run deploy wiki-crawler --image gcr.io/$PROJECT_ID/wiki-crawler
```

Alternatively, you can use the provided `cloudbuild.yaml` file, which is [Cloud Build](https://cloud.google.com/cloud-build/) config definition; see [the documentation](https://cloud.google.com/cloud-build/docs/) for details. To submit the build use the below command.

```bash
gcloud builds submit
```

To change the default substitution variables, type as follows, e.g. to change the service name:

```bash
gcloud builds submit --substitutions=_SERVICE_NAME=new-wiki-crawler
```
