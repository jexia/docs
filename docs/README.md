---
home: true
heroImage: null
heroText: null
tagline: The backend for your applications
actionText: Getting started →
actionLink: /get-started/
features:
  - title: Build & Deploy Applications
    details: Jexia has all you need to create and run applications. 
  
  - title: Fast Development
    details: Our set of integrated tools will end repetitive tasks from your development process
  
  - title: High Performance
    details: No need to keep on eye on performance and security. We will do it for you!
  
  - title: SDKs
    details: Our JS SDK and PySDK will help you to integrate your applications with Jexia faster. 
  
  - title: App Hosting
    details: With our Application Hosting you will be able to host you static site and Node applications with ease. 
  
  - title: CLI
    details: You can integrate Jexia into your CI/CD process by using our CLI tool. 
footer: Copyright © 2020 Jexia company
---

### As Easy as 1, 2, 3

```js
import { jexiaClient, dataOperations } from "jexia-sdk-js/node"; // jexia-sdk-js/browser;
const dataModule = dataOperations();

// You need to use your API Key / API Secret which is generated within your Jexia application. 
// Do not forget make a Policy for your API!
jexiaClient().init({
  projectID: "PROJECT_ID",
  key: "API_KEY",
  secret: "API_SECRET",
}, dataModule);

// Now you can run any CRUD operations for your Dataset: clients
dataModule.dataset("clients")
  .select()
  .subscribe(records => { 
     // You will always get an array of created records, including their 
     // generated IDs (even when inserting a single record) 
  }, 
  error => { 
     // If something goes wrong, the error information is accessible here 
});
  ```
