# Authentication 
At this point of time there are two ways of autentification in Jexia. 
1. Via API-Key
2. Via Project User
By default all data is closed for externals and you need to specify what and to whom to show.
Does not meter what option you choose, you will need have policy either for API-Key or for Users. 

## API-Keys
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
<template v-slot:ts>
``` bash
```
</template>
</CodeSwitcher>

API-Key can be used to organise access for many unauthorised users, for example readers of your blog. Your application will have read access to data and evryone who is usign your application will have sane access as API-Key.

To make API-Key you need to navigate to *Access Control - API keys - Create API Keys*.
![API-Key](./api-key.png)

Here Description is a general purpouse field which can give you idea what is this API-Key about.
When you click on *Create API keys* API-Key and API-Secret will be generated automatically. Please, copy it in some place as you will not be able to get secret anymore. We aer doing one way encryption of this.
That is it, you are ready to put policy for current API-Key. 

Let's show how to use API-Key in code to run Auntentification. 

## Users
<CodeSwitcher :languages="{js:'JavaScript',bash:'cURL'}">
<template v-slot:js>

``` js
import { jexiaClient, UMSModule, ... } from "jexia-sdk-js/node"; 
// jexia-sdk-js/browser;
const ums = new UMSModule(); 

jexiaClient().init({  
  projectID: "your-project-id",  
}, ums, other modules); 

// Sign In with user created in Jexia Panel
ums.signIn({  
  email: 'elon@tesla.com',  
  password: 'secret-password'
});  
```
</template>
<template v-slot:ts>

``` bash
```

</template>
</CodeSwitcher>

Another way to autentificate at Jexia is Project Users. Usually you need this, when you want to provide more grants for specific resources. Let's say Update and Delete options for blog. So as a first step you need to crete user under  
![UMS Users](./ums-2.png)

With this you can go to Policies page, create new policy with Subject: **AllUsers**, Resource: **any you need**, Actions: **Update, Delete**.
![Policy](./policy.png)

On picture you can see setup for all registered users to have access to *feedback* dataset with full CRUD authorization. 

## Policies
As it was mentioned above to have access to you data you need to have **Policy** created for your API-Keys or Project Users. 
Policy does not have consumption API. Management avaialbe in Jexia webapp.

There are three main topics during Policy setup:
1. Subject (who has access) - can be API-Key, AllUsers (all sign in users)
2. Resources (access to what) - can be any Dataset, Fileset, Channel. AllUsers - means you allow operation with Project Users table. 
3. Actions (what can do) - here you can specify which action applicable Create, Read, Update, Delete. For Channels you have specific actions: Subscribe (read), Publish (write).      
![Policy](./policy.png)

You can create as many policies as you need. All of them will be evaluated during request. 