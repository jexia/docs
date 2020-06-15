# <pro/> Application Hosting

Jexia's Application Hosting can be used to serve your static files as well as hosting for you backend. Currently, you can host your Node JS, Go, Python, PHP applications, your Docker images or simply static files. You can fetch an application directly from a git repository and deploy it on our cloud. Application Hosting can be used for example with React, VueJs, and Angular as frameworks. The only requirement is that the project listens on port `80`, please see the examples below.

## Common requirements: 

1. GitHub repository (open or private)
2. Project in Jexia
3. Configuration based on Runme.io
4. The application must listen on `0.0.0.0`
5. The application might use port `80` or expose port via `runme` config file

## Build and run requirements:

Jexia supports `Runme.io` specification. It means you can deploy multiple containers including needed databases and language you prefer to use. So, if you already have `.runme` folder inside your repo, you can deploy it without any changes. If you do not have it you can use runme.io generator to generate specification. 
Please, visit [runme.io](https://runme.io)

::: tip
You can run your docker image as well. Check runme.io to make proper configuration for this.  
:::

## What do you get? 

1. Hosting for your React, VueJS, Angular, NodeJS, Deno, Python, Go, PHP and many more projects built in a variety of languages 
2. A subdomain provided by Jexia, such as `*.jexia.app`
3. The possibility of adding your custom domain
4. SSL certificates for your subdomain
5. More free time to develop without spending time on issues regarding your deployment, setup, control and monitor processes

## How does it work? 

When you initiate your application via Jexia's Application Hosting, Jexia will clone your GitHub repository into a secure environment. After this Jexia will read configuration file from `.runme/config.yaml` and will apply building instructions. As soon as it is finished, the repository will be deployed into the cloud environment and a URL will be generated for your application. When the deployment has been completed, Jexia will run the command from your Dockerfile. As a last step, the cloned repository will be deleted from the secure environment.

## Limitations
Below you can see limitation per container:
* Number of requests - no limit
* Number 
* 1 CPU 
* 1Gb RAM
* 5Gb of storage (root file system inside container)
* We use K8s for Application Hosting. Within this, there is no state management inside each 'pod', please ensure you use persistent storage for all data.


## How to deploy?

### Step 1: Check if your GitHub repository has .runme folder

First of all, you need to be sure that your repository contains a `.runme/config.yaml` file. 
See the example below:

```yaml
version: 1.0
publish: app
services:
  app:
    build:
      type: dockerfile
      config: ./.runme/Dockerfile
    ports:
      - container: 4000
        public: 80
```
It gives instruction for Jexia to use Dockerfile from `./.runme/Dockerfile` to build an app and expose port 4000 to port 80 

Dockerfile can be as you need, below you can find some common for NodeJs app:

```Dockerfile
FROM node:14.0.0
WORKDIR /app
COPY . .
RUN npm install
ENTRYPOINT npm run serve
```


### Step 2: Organize your projects at Jexia

*For Open Source GitHub projects.*

Go to the Application Hosting menu, then click on **Setup Application**.

![No Application](./step_1.png)

The next page is related to the GitHub repository setup. You can get it by clicking the **Clone or Download** button on the GitHub webpage. It should look like: **https://github.com/jexia/test-node-app.git**

![No Application](./step_2.png)

Jexia will check if it can read the repository and will show the repository name on the page. Under the name, you will see the generated URL for your application. You can use this after your project has been deployed.

![No Application](./step_3.png)

Under the **General** tab, you can add environment variables. Inside your NodeJS application, those variables will be available via `process.env.<env name>`.

Under the **Settings** tab, you can adjust your GitHub repository.

![No Application](./step_4.png)

As soon as the setup is done and you are ready to go - click the **Deploy** button. You will be transferred to a page where you can select your API Key and API Secret. That information will be transferred to your NodeJS application and will be accessible as:

* `process.env.API_KEY`
* `process.env.API_SECRET`
                                                                                                                                                                                        
It is not possible to use the `process.env.*` approach with Angular, VueJS and React applications. This is because your API Key and Secret will be available on the frontend. In this case, we recommend using a NodeJS backend, which will enable the ability for additional validation.    

![No Application](./step_5.png)

After clicking **Done**, the deployment process will start. You will be able to see an indication to whether the deployment process has completed or not. Depending on the size of the repository, the deployment process can take around 3 to 7 minutes. 

![No Application](./step_6.png)

There are two states for deployment: Done (green dot) or Fail (red dot). In the case of a red dot, confirm you can build your repository locally and check if you have a `package.json` with the `build` and `start` commands. If these are correct and present, try to re-deploy by clicking the **Deploy** button again. If you need further support, feel free to contact our support team.

::: tip
Failures can also be caused if you try to deploy a private repository on a free project plan. This will result in the error message: "Could not clone repository".
:::

If everything completes successfully, you will see a green dot:

![No Application](./step_7.png)

As soon as the deployment is done your application will be accessible via a URL marked in blue on the screen.

## How to update the application once deployed?

There are two possibilities to make a re-deployment. Jexia is supporting deployment without rebuilding code, this is useful when you need to update environment variables only. If you require a full re-build, the repository code will be downloaded from GitHub and the deploy process will begin again, with all previous environment variables.

To initiate a re-deployment, you need to click the **Redeploy** button (top right), which will appear as soon as the initial deployment has finished, instead of the **Deploy** button. 

![No Application](./step_8.png)

After this, you will see a window with deployment options, this is where you can specify your **API_KEY** and **API_SECRET** as well as switch between building options. By default, we redeploy only environment variables, without pulling the repository from GitHub and rebuild the source code.

## For private GitHub projects.

The flow for private repositories is almost the same. The only difference is that you need to allow Jexia to access your repository.

![No Application](./step_8.png)

You will see another button that will allow you to authorize Jexia to clone your private repository. The rest of the process is the same as previously described. 

## Custom domain

There is a possibility to add your domain to your application.

For this you need to have:
1. Successfully deployed application 
2. A domain with an `A` DNS record that points to your application's IP
3. Only one `A` record per domain should exist
4. After the domain has been added to your Jexia configuration, you would need to redeploy your application. You can re-deploy without the rebuild option (see above) 

It might take some time for your application to be accessible via the new domain as your DNS needs to update its records.

![No Application](./step_1.png)

## Delete application
To delete the application you can go to the **Settings** tab and then click the **Delete** button. You will need to enter the repository name to confirm the deleting operation. Please note, you are not able to delete the project until you have an application running. 

In our example, the repository name will be: `jexia-vue-todo`

![Delete Application](./step_1.png)

## Examples
As for now, you can use these examples for deployment:
* VueJS TodoMVC: `https://github.com/jexia/jexia-vue-todo.git`
* NodeJS application: `https://github.com/jexia/test-node-app.git`
* VueJS Jexia DataViwer: `https://github.com/jexia/DataViewer.git`
