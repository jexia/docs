# Getting started
## Create a project

**Jexia** is a platform with a set of services natively integrated between each other which takes out the routine task for application development and operation. Good thing that you can use services together or independently. It gives you the flexibility to choose the functionality that you need and have easy integration with your project via REST API and SDK.  

You can [create](https://app.jexia.com/signup) Jexia account by using email or GitHub account. 

The first place after sign in will be Jexia Dashboard. Here you can observe all your projects and switch between them. Inside the project, you can do all management operations as well as organize collaboration and integration. The same operation you can do via ours [CLI tool](https://jexia-cli.readthedocs.io/en/stable/)
![Jexia Dashboard](./dashboard.png)

You can create a project by clicking on the Create Project button.

<iframe width="700" height="395" src="https://www.youtube.com/embed/FY5QKc-gMj8" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

You can have maximum **3** projects with the free plan after you need to upgrade at least 1 project to the paid version or delete some projects. 

## Inside the project
![Jexia Services](./services.png)
1. **Collaboration** - under this menu you can coordinate access to your project setup. For example, you are working with a teammate who is busy with operation or development. You can invite him to be a collaborator for your project and together you can finish all much faster.  
1. **Settings** - under this menu, you can find the basic setup for the project (project name, description, URL) as well as you can delete the project.
1. **Integration** - this section allows you to set up a connection between Jexia project and external services. You will be able to use them in your automation setup. 

## Services
1. **Application Hosting** - is used to **host application in the cloud**. You can use it for static file hosting as well as for NodeJS applications. 
1. **Dataset** - is used to store your application data. For example products, orders, transactions, configurations, other.
1. **Fileset** - is used to manage files for your application. For example avatars, blog images, product images, pdf documents, others.
1. **Relations** - provide an easy way to establish data relations between Dataset-Fileset-Project Users. It allows you to get related data within one request. All connections and optimizations are managed by Jexia you do not need to care about this.    
1. **RTC Channels** - is used to organize **Pub/Sub** solutions such as chats, online games others. As well this module is adding real-time notification functionality for Dataset, Fileset, Project Users modules. 
1. **Project Users** - is used to manage users for your application. The module has some specific functions, like **change password**, **sing up**, **sign in** as well as supporting standard CRUD approach. You can choose any approach. 
1. **Automation** - this module allows you to set up actions that will run based on some event.

## Access control
1. **API-Keys** - module for API-Keys generations. You can make keys for public data, private data, partners, etc. By default ,all data is closed for the public. Authorization is managed via Policy. 
1. **Policy** - authorization access to resources in your application. To create the policy you need to have at least one Project User or API-Key. 

## Create DataSet
Let's create Dataset to have some cloud storage for our data.
<iframe width="700" height="350" src="https://www.youtube.com/embed/3Dt79oYyAsU" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

![Dataset fields](./ds_fields.png)
  
Good things Jexia Dataset has a schema and schemaless support as well as field validation, default values for fields. So you do not need to spend time for development and testing this. We will create Dataset Orders.

![Dataset](./ds.png)

The good thing about Dataset that it can store data with the Schema or Schemaless approach, it gives you the flexibility to start your development without any particular model and update all on the fly. 

::: warning
Please, be aware there are some rules related to the schema and schemaless data:

1. When you create schema field data from the schemaless filed is not transfer to a newly created field.
2. When you insert an object which has fields out of schema, Jexia will automatically create a schemaless field and put data there.
3. When you delete schema field data will be deleted as well versus transfer it into a schemaless field.  
:::

You do not need to care about indexes optimization etc. All this will be done by Jexia.

If you have some related data such as Order - Product or Book - Author you can establish a connection between them under the Relation menu. You do not need to specify any fields as a foreign key for this. Jexia will handle all work related to connections. After setup Jexia will automatically put data in proper Dataset. When you will fetch data you can get results with related data or without it.   

## Create API & Policy
As a next step, we would need to establish authorization rules. By default, all data are closed and we need to specify rules to show resources. 

There are two ways to organize this:
1. API-KEY - will be useful when you need to open data for many visitors. For example, show all blog posts or books or comments.
2. Project User - will be useful when you need to open access to a specific action, like Update or Delete. So only specific people can do this.
3. Namespace (under development now) - you can group users under some name and provide common access to specific actions and records. 

### Access via API-KEY
To have API-KEY access, first, you need to create API-KEY. For this, you need to go to Access Control - API-Keys and create a new one. **Please write somewhere API-secret, you will not be able to get it again.** 
![API-Key creation](./api-key.png)

After go to **Access Control - Policies** to specify which resources and actions available for this API-KEY. As a Subject you can selected newly created API-KEY, in Resources select needed Datasets(Filesets or Channels), select an allowed action: Create, Read, Update, Delete.  
![Policy setup](./policy.png)

### Access via Project User
Go to **Services - Project Users** and create one user with email and password. 
After go to **Access Control - Policies**, in Subject select **AllUsers** in Resources needed Datasets (Filesets or Channels) as well as actions. With this, all registered and activated users will have Read access to orders dataset
![AllUsers policy](./allusers.png)

## Interact with data
Now let's make simple CRUD to our dataset. For this, you can use the REST API or JS SDK. ![JS SDK](https://www.npmjs.com/package/jexia-sdk-js) is built on top of the RxJS library, so you can use all power of this library.

<iframe width="700" height="394" src="https://www.youtube.com/embed/i7v8FOS7_WI" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

To install JS SDK into our project we need to run:
```
npm install jexia-sdk-js node-fetch ws --save
```

Below you can see an example with all modules imported into the project. This is optional. If you do not need Fileset or Projec User(UMSModule), real-time feel free to skip importing them.  

<CodeSwitcher :languages="{js:'JavaScript',bash:'cURL'}">
<template v-slot:js>

``` js
// Jexia client
import { jexiaClient } from "jexia-sdk-js/node"; 
//DataSet operation
import { dataOperations } from "jexia-sdk-js/node";
// FileSet operations
import { fileOperations } from "jexia-sdk-js/node";
// Project Users
import { UMSModule } from "jexia-sdk-js/node";
// To have real-time notifications & channels 
import { realTime } from "jexia-sdk-js/node";
// jexia-sdk-js/browser - if you run Jexia from browser;

const ds = dataOperations();
const jfs = fileOperations();
const ums = new UMSModule(); 
const rtc = realTime(); 

jexiaClient().init({
  projectID: "project_id",
  key: "API_KEY",
  secret: "API_SECRET",
}, ds, jfs, ums, rtc);

const orders = dataModule.dataset("orders");
const archive = dataModule.dataset("arch");
const selectQuery = orders
      .select()
      .where(field => field("dislike").isEqualTo(true))
      .pipe(
        // put them into archive!
        switchMap(records => archive.insert(records)),
      );  
const insertQuery = orders.insert([order1, order2]);  
const updateQuery = orders.update([{ title: "Updated title" }]);  
const deleteQuery = orders.delete();  

// Either way, the response will be an array  
selectQuery.subscribe(records => { 
     // you will always get an array of created records, including their 
     //generated IDs (even when inserting a single record) 
  }, 
  error => { 
     // you can see the error info here, if something goes wrong 
});
```
</template>
<template v-slot:bash>

``` bash
# env variables to be set
export PROJECT_ID=<project_id>
export API_KEY=<key_here>
export API_SECRET=<secret_here>
export TEST_USER=<user_here>
export TEST_USER_PSW=<password_here>
# save API-Key token to env in case of API-Key usage
export APK_TOKEN=`curl -X POST -d '{
  "method":"apk",
  "key":"'"$API_KEY"'",
  "secret":"'"$API_SECRET"'"
}' "https://$PROJECT_ID.app.jexia.com/auth" | jq .access_token`
# save UMS token to env in case you use Project Users
export UMS_TOKEN=`curl -X POST -d '{
  "method":"ums",
  "email":"'"$TEST_USER"'",
  "password":"'"$TEST_USER_PSW"'"
}' "https://$PROJECT_ID.app.jexia.com/auth" | jq -r .access_token`
# Select all data with apk token
curl -H "Authorization: Bearer $APK_TOKEN"
  -X GET "https://$PROJECT_ID.app.jexia.com/ds/orders" | jq .
# or with ums token
curl -H "Authorization: Bearer $UMS_TOKEN"
  -X GET "https://$PROJECT_ID.app.jexia.com/ds/orders" | jq .
```

</template>
</CodeSwitcher>

## Delete project

To delete your project you need to remove all applications on Application Hosting. Then go on the Settings menu. 
You would need to provide your user password to make it happen. 

::: danger
Please, be aware. All data will be deleted and we will not be able to restore it. Please, use it carefully. 
:::

![Delete project](./delete_prj.png)

## Examples & Open-source
There many examples you can find in our [GitHub repo](https://github.com/jexia) as well as some part of our platform which was open-sourced. 

In the long run, we plan to open-source most of the parts for the Jexia platform. From another side, we understand that ope-source is a big responsibility and time demand to support communities. As for now, we decided to focus on adding new functionality to the platform, to provide more opportunities for our friends.  
Happy codding! 
