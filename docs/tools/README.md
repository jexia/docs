# Interact with data
## Install SDKs

<CodeSwitcher :languages="{js:'JavaScript',py:'Python',bash:'cURL'}">
<template v-slot:js>

```
npm install jexia-sdk-js node-fetch ws --save
```

</template>
<template v-slot:py>

```
pip install jexia-sdk
//or
easy_install jexia-sdk
```

</template>
<template v-slot:bash>

``` bash
cURL should be intalled
```

</template>
</CodeSwitcher>


## Make request
Now let's make simple CRUD to access our Dataset. For this, you can use the REST API or one of our SDKs. Our [JS SDK](https://www.npmjs.com/package/jexia-sdk-js) is built on top of the RxJS library, so you can use all the power of this library. Other SDKs can be found on our [GitHub](https://github.com/jexia).

<iframe width="700" height="394" src="https://www.youtube.com/embed/i7v8FOS7_WI" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

<CodeSwitcher :languages="{js:'JavaScript', py:'Python', bash:'cURL'}">
<template v-slot:js>

Below you can see an example with all the modules imported from SDK. If you do not need to access Filesets, Project Users (UMSModule) or real-time events, feel free to skip importing them.

``` js
import {
  jexiaClient,
  dataOperations, // To work with Datasets
  fileOperations, // To work with Filesets
  UMSModule, // To work with Project Users
  realTime // To get real-time notification for data changes and work channels
} from "jexia-sdk-js/node";

const ds = dataOperations();
const jfs = fileOperations();
const ums = new UMSModule();
const rtc = realTime();

// You need to use your API Key / API Secret which is generated within your Jexia application.
// Do not forget to create a Policy for your API and set the proper restrictions!

// In addition to key and secret, you need to provide either projectID and zone OR just provide projectURL
jexiaClient().init({
  projectID: "PROJECT_ID",
  key: "API_KEY",
  secret: "API_SECRET",
  /**
   * Zone parameter was introduced in v5.2.0
   * If your project uses a previous version it will keep working for a while.
   * You can find you project zone inside "Settings" section of your project.
   */
  zone: "PROJECT_ZONE",
}, ds, /* pass any other modules you need like jfs, ums, rtc */);

// or

jexiaClient().init({
  projectURL: "PROJECT_URL", // you can find it in your project settings
  key: "API_KEY",
  secret: "API_SECRET",
}, ds);

// Now you can run any CRUD operations for your Datasets
const orders = ds.dataset("orders");
const archive = ds.dataset("arch");
const selectQuery = orders
  .select()
  .where(field => field("dislike").isEqualTo(true));

// const insertQuery = orders.insert([order1, order2]);
// const updateQuery = orders.update([{ title: "Updated title" }]);
// const deleteQuery = orders.delete();

selectQuery.subscribe(records => {
    // You will always get an array of created records, including their
    // generated IDs (even when inserting a single record)
  },
  error => {
    // If something goes wrong, you'll get an IRequestError object
});
```
</template>
<template v-slot:bash>

``` bash
# Environment variables to be set
export PROJECT_ID=<project_id>
export API_KEY=<key_here>
export API_SECRET=<secret_here>
export TEST_USER=<user_here>
export TEST_USER_PSW=<password_here>

# save API key token to our environment in case we need to use it
export API_TOKEN=`curl -X POST -d '{
  "method":"apk",
  "key":"'"$API_KEY"'",
  "secret":"'"$API_SECRET"'"
}' "https://$PROJECT_ID.app.jexia.com/auth" | jq .access_token`

# save UMS token to our environment in case we need to access Project Users
export UMS_TOKEN=`curl -X POST -d '{
  "method":"ums",
  "email":"'"$TEST_USER"'",
  "password":"'"$TEST_USER_PSW"'"
}' "https://$PROJECT_ID.app.jexia.com/auth" | jq -r .access_token`

# Select all data with our API token
curl -H "Authorization: Bearer $API_TOKEN"
  -X GET "https://$PROJECT_ID.app.jexia.com/ds/orders" | jq .
# or with ums token
curl -H "Authorization: Bearer $UMS_TOKEN"
  -X GET "https://$PROJECT_ID.app.jexia.com/ds/orders" | jq .
```

</template>
<template v-slot:py>

``` py
from jexia_sdk.http import HTTPClient

JEXIA_PROJECT_ID = ''
JEXIA_API_KEY = ''
JEXIA_API_SECRET = ''

if __name__ == '__main__':
    client = HTTPClient()
    client.auth_consumption(
      project=JEXIA_PROJECT_ID,
      method='apk',
      key=JEXIA_API_KEY,
      secret=JEXIA_API_SECRET,
    )
    res = client.request(
          method='GET',
          url='/ds/orders',
          cond='[{"field":"dislike"},"=",true]',
          outputs='["id","total","title"]'
    )
    print(res)
```

</template>
</CodeSwitcher>

## Work from browser
You can work with Jexia platform directly from browser. For this you need to import Jexia SDK through unpkg

``` html
<html>
<head>
     <script src="https://unpkg.com/jexia-sdk-js/bundle/browser.umd.min.js"></script>
</head>
```

and then do similar commands to get data. Below you can find example:

``` html
<html>
<head>
     <script src="https://unpkg.com/jexia-sdk-js/bundle/browser.umd.min.js"></script>
</head>
<body>
<i>loading...</i>
<ul></ul>
<script type="text/javascript">
  window.onload = function() {
    if (!jexia) {
      throw new Error("Please inform support team of Jexia.");
    }
    // Initialize dataOperationsModule
    const dataModule = jexia.dataOperations();
    const credentials = {
      projectID: "<your-project-id>",
      key: "<your-project-api-key>",
      secret: "<your-project-api-secret>",
      zone: "<your-project-zone>",
    };
    jexia.jexiaClient().init(credentials, dataModule);
    const postsList = document.querySelector("ul");
    dataModule.dataset("posts")
      .select()
      .subscribe(
        (posts) => {
          posts.forEach((post) => {
            const postTitle = document.createElement("li");
            postTitle.innerText = post.title;
            postsList.appendChild(postTitle);
          });
        },
        (errors)=>{console.log(errors)}
      )
  }
</script>
</body>
</html>
```

