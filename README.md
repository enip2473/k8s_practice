0. 

1. Build your Docker image: Open a terminal, navigate to the directory containing your Dockerfile, and run the following command to build your Docker image. Replace yourapp with the name you wish to give your Docker image.

```
docker build -t yourapp .
```


2. Run your Docker container: After the build completes, you can run your FastAPI application inside a Docker container using:
This command runs your application in a detached mode (-d), maps port 8000 of the container to port 8000 on your host (-p 8000:8000), and names the container yourapp-container.

```
docker run -d --name yourapp-container -p 8000:8000 yourapp
```

