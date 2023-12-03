# How to build and host

Note: all following commands are run from current directory.

Build a server image:

```bash
docker build -t fashionpulse .
```

Run the image locally to ensure it's working:

```bash
docker run -p 8000:8000 fashionpulse
```

Login to Azure container registry:

```bash
docker login fashionpulse.azurecr.io
```

Push the container (tagging with url is required). To get login credentials, go to 'Quick start' in the browser. Enable admin rights in order to push the image. The image should appear under 'Services / Repositories'.

```bash
docker tag fashionpulse fashionpulse.azurecr.io/fashionpulse 
docker push fashionpulse.azurecr.io/fashionpulse
docker pull fashionpulse.azurecr.io/fashionpulse # make sure everything is ok (image must be up-to-date)
```

When logged in, to create a new version of the container, build with a new tag (and then push):

```bash
docker build -t fashionpulse.azurecr.io/fashionpulse:new-tag .
```

To deploy, create a 'Container App' or a 'Container Instance'.
