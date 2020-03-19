# Application hosting

Jexia Application Hosting can be used to organize your static files hosting or to add some logic that is missing from Jexia functionality yet. Currently, you can host your Node JS application.  All can be started in one click. Application Hosting can be used as Static File Hosting as well, using for example React, VueJs, and Angular as frameworks. Only what will be needed is to add the HTTP server as a dependency and make sure it listens on port 80. See the examples below.  

## Requarements 

1. GitHub repo (open or private)
2. project in Jexia
3. your application is supporting NodeJS version 12 and NPM 
4. your application must contain package.json file with the build and start scripts
5. the application must use port 80 for its API
6. application must listen 0.0.0.0

## What do I get? 

1. hosting for your React, VueJS, Angular, NodeJS application 
2. subdomain in zone jexia.app available in Internet
3. possibility of adding your custom domain (available for paid projects only)
4. SSL certificates for your subdomain
5. more free time without headaches to select, setup, control and monitor all of those points

## How does it work? 

When you initiate your Application Hosting, Jexia will clone you GitHub repo into a secure environment. In this environment Jexia will run npm install, npm run build. As soon as it will be finished, the repo will be deployed into the cloud environment and it will generate URL for your application. When the deployment is done Jexia will run the npm run start command from your package.json file. As a last step cloned repo will be deleted from the secure environment. Your application must expose PORT: 80. Currently, we support NodeJS 12.10 and NPM

## How to deploy?

### Step 1: Check if your GitHub repo has package.json file

First of all, you need to be sure that your repo contains a package.json file. Inside it must contain the build and start commands.  See an example below:

```json
{
    "name" :  "My mega app",
    "version" :  "0.1.0",
    "scripts" : {
           "build" : "vue-cli-service build",
           "start" : "http-server ./dist -p 80"
     },
  "dependencies" : {
          "http-server" : "^0.11.1",
          "jexia-sdk-js" : "^4.1.0",
           "vue" : "^2.6.10"
    },
  "devDependencies" : {
  }
}
```
scripts.build should contain the command that builds your release pack. 

For example:

1. VueJS : "build": "vue-cli-service build"
2. React :  "build": "cd packages/react-scripts && node bin/react-scripts.js build"
3. Angular: "build":"ng build *project* [options]"
4. NodeJS : "build":"" -  can be empty string. 

If you need to run some Pre- / Post-install scripts you need to combine them under build script.

As you can see in our example we use next to the start script:  "start": "HTTP-server ./dist -p 80". We use HTTP-server to organize serving for a static file. Here we listen to port 80 and use the dist folder, which contains our release. More options can be found on the HTTP-server package page. Feel free to implement the approach that suits you. All you need to remember is to use PORT:80 for your server. 

::: tip
If you have a docker file present in your repo, we will use it to build & deploy the application. 
:::

### Step 2: Organize your projects at Jexia

*For Open Source GitHub projects.*

Go to the Application Hosting menu, then click on 'Setup Application'

![No Application](./step_1.png)

The next page related to the GitHub repo setup. You can get it by clicking the Clone or Download button on the GitHub webpage. It should look like: **https://github.com/jexia/test-node-app.git**

![No Application](./step_2.png)

Jexia will check if it can read the repo and will show the repo name on the page. Just under the name, you will see the generated URL for your application which you can use after the deployment is done.

![No Application](./step_3.png)

Under the General tab, you can add environment variables. Inside your NodeJS application, those variables will be available via `process.env.<env name>`

Under the Settings tab, you can adjust your GitHub repo

![No Application](./step_4.png)

As soon as the setup is done and you are ready to go - click the Deploy button. You will be transferred to a page where you can select your API Key and API Secret. That information will be transferred to your NodeJS application and will be accessible as

* process.env.API_KEY
* process.env.API_SECRET
                                                                                                                                                                                        
It is not possible to use process.env.* approach with Angular, VueJS, React applications. Otherwise, your API Key and Secret will be available on the frontend. In this case, we recommend using the NodeJS backend, which will make additional validation. NodeJS can be run with Jexia Application Hosting.    

![No Application](./step_5.png)

by clicking Done the deployment process will start. You will be able to see an indication if the deployment is done or not. Depending on the size of the repo deployment process this can take from 3 to 7 minutes. 

![No Application](./step_6.png)

There are two states for deployment: Done (green dot) or Fail (red dot). In the case of a red dot confirm you can build your repo locally, check if you have a package.json with the build and start sections and try to re-deploy by clicking the Deploy button again. As well feel free to contact our support team.

Failures can also be caused if you try to use a private repo with a free project. Then the deployment will fail with the message: Could not clone repo...

when all goes well you will see a green dot:

![No Application](./step_7.png)

As soon as the deployment is done your application will be accessible via a URL marked in blue on the screen.

## How to update the application once deployed?

There are two possibilities to make redeployment. Jexia is supporting deployment without rebuilding code - when you need to update environment variables only, or full rebuild  - when code will be downloaded from GitHub, build and redeploy with all mentioned environment variables.  

To initiate redeployment, you need to click the Redeploy button (top right), which will appear as soon as the initial deployment will be finished instead of the Deployment button. 

![No Application](./step_8.png)

after you will see a window with deployment option, where you can specify your API_KEY and API_SECRET as well as switch between building options. By default, we redeploy only environment variables, without pulling repository from GitHub and rebuild source code.

## For private GitHub projects.

The flow for private repos is almost the same. The only difference is that at the beginning you need to have a Jexia subscription and provide access for Jexia to your repo.

![No Application](./step_8.png)

As soon as you have a subscription you will be able to see another button which will allow you to authorize Jexia in your private repo
to rest part of the process as previously described. 

## Custom domain

There is a possibility to add to your application your domain.

For this you need to have:
1. Successfully deployed application 
2. Domain have A DNS record and this record should point to your application IP
3. Only one A record per domain should exist
4. After domain will be added to Jexia configuration you would need to redeploy your application. You can redeploy without rebuild option (see above) 
It might take some time until your application will be accessible via domain as DNS refreshment needs to happen.

![No Application](./step_1.png)

## Delete application
To delete the application you can go under the Settings tab and then use the Delete button. You would need to enter the repo name to confirm the deleting operation. Be aware you are not able to delete the project until you have an application running. 

In our example, below repo name will be: jexia-vue-todo

![Delete Application](./step_1.png)

## Examples
As for now, you can use those 2 repos as examples for deployment:
* https://github.com/jexia/jexia-vue-todo.git (VueJs TodoMVC)
* https://github.com/jexia/test-node-app.git (NodeJS application)

## Limitations
* Currently, your application can have 265MB of RAM.
* We support NodeJS version 12.10
* We support NPM as the default package manager
* We are using K8s for Application Hosting. There is no state management inside the pod, please be sure you are using some persistent storage.
