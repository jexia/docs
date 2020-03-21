# Authentication 
Jexia provides to the way of authentication:
1. via API-Key - for big amount of clients, unauthorized users, partners.
2. via Project User - for specific users to have specific actions, like UPDATE, DELETE 

By default, all data is closed for externals and you need to specify what and to whom to show.
Does not meter what option for authentication you choose, you will need to have a policy either for API-Key or for Users. 

<iframe width="700" height="394" src="https://www.youtube.com/embed/o2ZN3nvdhi8" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

## API-Keys
API-Key can be used to organize public access (for example readers of your blog). 
To create API-Key you need to navigate to *Access Control - API keys - Create API Keys*.
![API-Key](./api-key.png)

Here `Description` is a general-purpose field that can give you idea about current API-Key.
When you click on `Create API keys` API-Key and API Secret will be generated. Please, copy API Secret to someplace as you will not be able to get it again. We are doing one-way encryption for the secret. So the only way to get secret is to regenerate API-Key again. 
That is it, you are ready to put policy for current API-Key. 

For example, let's show how to provide `Read Only` access to `orders` dataset for current API:
![API Policy](./api_policy.png)

Now we can interact with our data. 

<CodeSwitcher :languages="{js:'JavaScript',bash:'cURL'}">
<template v-slot:js>

``` js
import { jexiaClient, ... } from "jexia-sdk-js/node"; 
// jexia-sdk-js/browser;

jexiaClient().init({
  projectID: "project_id",
  key: "API_KEY",
  secret: "API_SECRET",
}, module1, module2,...);
```
</template>
<template v-slot:bash>

```bash
# env variables to be set
export PROJECT_ID=<project_id>
export API_KEY=<key_here>
export API_SECRET=<secret_here>
# save API-Key token to env in case of API-Key usage
export APK_TOKEN=`curl -X POST -d '{
  "method":"apk",
  "key":"'"$API_KEY"'",
  "secret":"'"$API_SECRET"'"
}' "https://$PROJECT_ID.app.jexia.com/auth" | jq .access_token`
# Select all data with apk token
curl -H "Authorization: Bearer $APK_TOKEN"
  -X GET "https://$PROJECT_ID.app.jexia.com/ds/orders" | jq .
```
</template>
</CodeSwitcher>

## Users
Another way to authenticate at Jexia is to use Project Users. Usually, you need this when you want to provide more rights for specific users. Let's say `Update` and `Delete` actions for the blog. As a first step, you need to create user under Project Users section  
![UMS Users](./ums-2.png)

After you can go to Policies page, create new policy with Subject: **AllUsers**, Resource: **any you need**, Actions: **Update, Delete**.
![Policy](./policy.png)

This will allow any registered user to have full CRUD access to `orders` dataset. 

<CodeSwitcher :languages="{js:'JavaScript',bash:'cURL'}">
<template v-slot:js>

``` js
import { jexiaClient, UMSModule} from "jexia-sdk-js/node"; 
// jexia-sdk-js/browser;
const ums = new UMSModule(); 

jexiaClient().init({  
  projectID: "your-project-id",  
}, ums); 

// Sign In with user created in Jexia Panel
ums.signIn({  
  email: 'user@jexia.com',  
  password: 'secret-password'
});  
```
</template>
<template v-slot:bash>

``` bash
# env variables to be set
export PROJECT_ID=<project_id>
export TEST_USER=<user_here>
export TEST_USER_PSW=<password_here>
# save UMS token to env in case you use Project Users
export UMS_TOKEN=`curl -X POST -d '{
  "method":"ums",
  "email":"'"$TEST_USER"'",
  "password":"'"$TEST_USER_PSW"'"
}' "https://$PROJECT_ID.app.jexia.com/auth" | jq -r .access_token`
# get data with ums token
curl -H "Authorization: Bearer $UMS_TOKEN"
  -X GET "https://$PROJECT_ID.app.jexia.com/ds/orders" | jq .
```

</template>
</CodeSwitcher>

## Policies
As was mentioned above to authorize access to your data you need to have **Policy** created for API-Keys or Project Users. 
At this point in time, you cannot manipulate `Policy` via consumption API. All management is available only via Jexia administration panel.

<iframe width="700" height="394" src="https://www.youtube.com/embed/i4dKznoXry0" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

There are three main areas for Policy setup:
1. Subject (who has access) - can be API-Key, AllUsers (all sign-in users), namespaces (grouped users under the same name).
2. Resources (access to what) - can be any Dataset, Fileset, Channel. AllUsers - means you allow operation with Project Users table. 
3. Actions (what can I do) - here you can specify which action applicable for subject: Create, Read, Update, Delete. For Channels you have specific actions: Subscribe (read), Publish (write).      
![Policy](./policy.png)

::: tip
You can create as many policies as you need. All of them will be evaluated during the request. Changes in Policy have an immidiate effect. 
:::