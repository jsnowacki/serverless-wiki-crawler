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

## Usage

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

There are occasionally some issues with using `serverless-python-requirements` plugin using Docker, especially on Windows. You can use the plugin with option `dockerizePip: false` and use local Python (in this case executable `python3.6`) for zip creation; on Windows it is best to use Ubuntu for Windows, as the target image on AWS is Linux. 

If you want to use Docker build, which is best if you use packages requiring compilation(e.g. `numpy`), set `dockerizePip: true`, on Windows `dockerizePip: non-linux`.
