---
home: true
heroImage: null
heroText: null
tagline: Backend for your applications
actionText: Getting started →
actionLink: /get-started/
features:
  - title: Build & deploy applications
    details: Jexia has all what you need to create and run application. 
  
  - title: Fast development
    details: Set of integrated tools which will cut off repetative tasks in development process
  
  - title: Performant
    details: No need to keep on eye on performance and security. We will do it for you!
  
  - title: SDK's
    details: JS SDK and PySDK will help you to integrate your application with Jexia faster. 
  
  - title: AppHosting
    details: With our Appliction Hosting you will be able to host you static site and Node applications. 
  
  - title: CLI
    details: You can integrate Jexia into your CI/CD process by using our CLI tool. 
footer: Copyright © 2020 Jexia company
---

### As Easy as 1, 2, 3

```js
import { jexiaClient, dataOperations } from "jexia-sdk-js/node"; // jexia-sdk-js/browser;
const dataModule = dataOperations();

// You can need to use API Key / API Secret which is generated in Jexia. 
//Do not forget make Policy for API   
jexiaClient().init({
  projectID: "project_id",
  key: "API_KEY",
  secret: "API_SECRET",
},dataModule);

// Now you can run CRUD operations for DataSet: clients
dataModule.dataset("clients")
  .select()
  .subscribe(records => { 
     // you will always get an array of created records, including their 
     //generated IDs (even when inserting a single record) 
  }, 
  error => { 
     // you can see the error info here, if something goes wrong 
});
  ```
