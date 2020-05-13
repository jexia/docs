[![Runme](https://svc.runme.io/static/button.svg)](https://runme.io/run?app_id=09eb2539-28c8-4feb-9f63-007d18247681) [![Chat on Discord](https://img.shields.io/badge/chat-on%20discord-7289da.svg?sanitize=true)](https://chat.jexia.com)

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

// Now you can run CRUD operations for Dataset: clients
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
