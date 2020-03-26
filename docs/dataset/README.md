# Datasets
Dataset is used to store your data in the cloud. You can interact with your data via REST API and our SDKs. All data protected with policy authorization. You can establish a relation between different Datasets or other parts of the platform. You do not need to take care of indexes, foreign keys, scaling, backups, SQL injections and other headaches related to database management. Each project has own instance of Dataset and other projects can't impact the stability and security of your project.   

Datasets have built-in support for validation, schema, and schemaless support, default values for fields.  

To create Dataset click "Go to project" button and on the next screen "Create dataset":
![Create Dataset](./create_ds.png)

The name of the Dataset is used as an endpoint (`*.app.jexia.com/ds/dataset_name`) to allow you to communicate with the JEXIA REST API.The name of your Dataset can contain only Latin characters and digits. The name of the Dataset has to start with a character.

## Configuration

## Schema:

The next step is to add fields to your datasets. To create a field, click the "Add field" button. In the same window, you can select name, type, and validation for your field. You can also provide a default value for the field. Field name, validation parameters can be changed in the future via the edit field but not the field type. If you want to change the type then you can only delete and create the field again. However, by deleting the field you will also lose the data stored in the field. With the Schema approach in responding, you will get the field in specific types:  String, Integer, Float, Date, DateTime, Boolean, JSON or UUID. Before insert or update, data will be validated against the validators.
![Create Field](./create_field.png)

::: tip
If you will insert JSON object which has additional fields versus schema, those fields will be saved as schemaless fields. For those fields validation rules and default values are not applicable.  
:::

## Schemaless:
To apply the schemaless approach just insert your JSON object into JEXIA without creating any schema fields inside Dataset. Data will be stored automatically with the type provided inside JSON. Please, note that validations and default values do not apply to schemaless data. You can convert from Schemaless to Schema when the design for your project is stabilized. Jexia supports String, Integer, Float, Date, DateTime, Boolean, JSON and UUID as field types.

::: warning
Please, keep in mind when you convert the field from schemaless to schema data will not be migrated to schema fields. You need to do it on your own and control the quality of data. 

If you delete fields from schema data will be deleted as well. It will not be converted back to schemaless.

During fetching data next priority applies for fields with the same name: Schema - Schemaless

In case you have established relation between datasets, you will get next priority for fields with the same name: Schema - Related Schema - Schemaless  
:::

## Validation:

Depends on field-type different validation parameters will be available for you. The most validators are available for String type. Such as: Required, UpperCase, LowerCase, Alphanumeric, Numeric, Alpha, Min/ Max length, RegEx.

For Float and Integer, there are Required, Min/ Max value validators.

In the future, we plan to add Date range and other validators. 

You might admit that when you select some validators, another one might be unavailable. It is due to logical exclusion. For example, it is not logical to have Upper and Lower case validators at the same time. To reduce the possibility of human mistakes we decided to prevent selection for some combinations.  

::: tip
Please, keep in mind validation is applicable for schema fields only. Jexia applies the same validations for Create and Update actions.
:::

## Default values
You can set up default values for the field. The value will be validated against type and constraints. 

::: warning
Please, keep in mind that for String type it is not possible to put default value as an empty string '', you can get either some value or **null**
:::

## Insert record
To create a record in Jexia Dataset you need to Create action added for your User or API-Key Policy. 
Below I will show the User approach as it will be a more common use case for record creation.

::: tip
Please, keep in mind in responds you always get back array of records, even if you insert only 1 record. With this you can apply same approach for data manipulation.  
:::

<CodeSwitcher :languages="{js:'JavaScript',bash:'cURL'}">
<template v-slot:js>

``` js
import { jexiaClient, dataOperations,UMSModule } from "jexia-sdk-js/node"; 
const ds = dataOperations();
const ums = new UMSModule(); 

jexiaClient().init({
  projectID: "project_id",
}, ds, ums);

const user = await ums.signIn({    
  email: 'Elon@tesla.com',    
  password: 'secret-password'
});  

let orders = [{
    "title":"Order1",
    "total":10,
    "verified":false
}, {
    "title":"Order2",
    "total":100,
    "verified":false
}]
const orders = dataModule.dataset("orders");
const insertQuery = orders.insert(orders);  
insertQuery.subscribe(records => { 
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
export TEST_USER=<user_here>
export TEST_USER_PSW=<password_here>
# save UMS token to env in case you use Project Users
export UMS_TOKEN=`curl -X POST -d '{
  "method":"ums",
  "email":"'"$TEST_USER"'",
  "password":"'"$TEST_USER_PSW"'"
}' "https://$PROJECT_ID.app.jexia.com/auth" | jq -r .access_token`

#Insert record
curl -H "Authorization: Bearer $UMS_TOKEN" -X POST -d '[{
  "title":"Order1",
  "total":10,
  "verified":false
},
{
  "title":"Order2",
  "total":100,
  "verified":false
}]' "https://$PROJECT_ID.app.jexia.com/ds/orders" | jq .
```

</template>
</CodeSwitcher>

As a result, you will get the next array of objects:
```JSON
[{
    "id": "e0e17683-f494-4f33-8343-ffed792b324e",
    "created_at": "2020-02-15T19:43:39.784342Z",
    "updated_at": "2020-02-15T19:43:39.784342Z",
    "title":"Order1",
    "total":10,
    "verified":false
}, {
    "id": "e0e17683-f494-4f33-9563-dded795e3121",
    "created_at": "2020-02-15T19:43:39.784342Z",
    "updated_at": "2020-02-15T19:43:39.784342Z",
    "title":"Order2",
    "total":100,
    "verified":true
}]
```
## Read records
To get your data you need to have Read action available for you for particular resource. You can apply different filters to get specific data. In example I will show example with API-Key usage as the most common approach.

<CodeSwitcher :languages="{js:'JavaScript',bash:'cURL'}">
<template v-slot:js>

As soon as JS SDK built on top of RxJS you can use the power of this library and re-use all available methods from here.  

``` js
// Jexia client
import { jexiaClient, dataOperations, field } from "jexia-sdk-js/node"; 
// jexia-sdk-js/browser;
const ds = dataOperations();

jexiaClient().init({
  projectID: "project_id",
  key: "API_KEY",
  secret: "API_SECRET",
}, ds);

const orders = dataModule.dataset("orders");
const selectQuery = orders
      .select()
      .where(field => field("verified").isEqualTo(true))
   // .where(field("title").isDifferentFrom("test")) 
   // .where(field("total").isBetween(1,30))
   // .where(field("total").isEqualOrGreaterThan(15))
   // .where(field("total").isEqualOrLessThan(7))
   // .where(field("total").isEqualTo(100))
   // .where(field("total").isGreaterThan(57))
   // .where(field("total").isLessThan(100))
   // .where(field("id").isInArray(my_val))   // my_val=[uuid1,uuid2];
   // .where(field("id").isNotInArray(my_val)) // my_val=[uuid1,uuid1];
   // .where(field("title").isLike("Moby dick"))
   // .where(field("title").isNotNull())
   // .where(field("title").isNull())
   // .where(field("title").satisfiesRegexp('a-z0-9'))   
      .pipe(
        // put them into archive!
        switchMap(records => archive.insert(records)),
      );  
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
#Select all data
curl -H "Authorization: Bearer $UMS_TOKEN" 
  -X GET "https://$PROJECT_ID.app.jexia.com/ds/orders" | jq .

# Select by id
curl -H "Authorization: Bearer $UMS_TOKEN" 
  -X GET "https://$PROJECT_ID.app.jexia.com/ds/orders?
  cond=\[\{\"field\":\"id\"\},\"=\",\"2a51593d-e99f-4025-b20b-159e226fc47d\"\]" | jq .

# Select special fields
curl -H "Authorization: Bearer $UMS_TOKEN" 
  -X GET "https://$PROJECT_ID.app.jexia.com/ds/orders?
  outputs=\[\"title\",\"verified\"\]" | jq .

# Select special fields + where
curl -H "Authorization: Bearer $UMS_TOKEN" 
  -X GET "https://$PROJECT_ID.app.jexia.com/ds/orders?
  outputs=\[\"title\",\"verified\"\]&cond=\[\{\"field\":\"total\"\},\">\",10\]" | jq .

# Select special fields + where
#Find any record that does not have total or total equals 1 or 2:
#[GET] /ds/orders?cond=[{"field":"total"},"null",true, "or", {"field":"total"},"in",["1","2"]]

#Find any record that has title or its total equals 1 or 2, but the results must be older than one day:
#[GET] /ds/orders?cond=[[{"field":"title"},"null",false, "or", {"field":"total"},"in",["1","2"]], "and", {"field":"created_at"}, ">", "24h"]

#Get any orders where title starts with the letter "A" and total > 21:
#[GET] /ds/orders?cond=[{"field":"title"},"regexp","^A", "and", {"field":"total"},">",21]

#Find a record by nested field where field some.field exists (is not null):
#[GET] /ds/orders?cond=[{"field":"some.field"},"null", false]
 
```

You can have the next comparator in `?cond` request:

Comparator group|**comparator**|**value**|Applicable field types
----------------|------------|-------|----------------------
Equality comparators|“>”, “<”, “=”, “!=”, “>=”, “<=”|single value matching field type|all fields
Emptiness comparators|“null”|true or false|all fields
Range comparator|“between”|[start, end]|textual, numbers, date/times
Array comparators|“in”, “not in”|Array of allowed values (matching field type)|all fields
Pattern comparator|“like”|string value|textual
Regex comparator|“regexp”|string value|textual

You can use next operator to make advanced requests:
* "and" 
* "&&" 
* "or" 
* "||"

Next aggregation functions are supported:

Function|Argument type(s)|Description
--------|----------------|-----------
avg()|number|Returns the average value of the field for the selected records
count()||Returns number of selected records
max()|number|Returns maximum value of the field for the selected records
min()|number|Returns minimum value of the field for the selected records
now()||Returns current time(stamp)
sum()|number|Returns the total value of the field for the selected records

</template>
</CodeSwitcher>

As a result, you will get the next the array of objects:

```JSON
[{
    "id": "e0e17683-f494-4f33-9563-dded795e3121",
    "created_at": "2020-02-15T19:43:39.784342Z",
    "updated_at": "2020-02-15T19:43:39.784342Z",
    "title":"Order2",
    "total":100,
    "verified":true
}]
```

## Delete a record
To delete a record you need to have Delete action available in policy for this resource. 
I will show examples with Project User usage as it will be common usage. 

When you run Delete, you will get back an array of affected records so you can sync changes with front end.  

<CodeSwitcher :languages="{js:'JavaScript',bash:'cURL'}">
<template v-slot:js>

``` js
import { jexiaClient, UMSModule, dataOperations } from "jexia-sdk-js/node"; 
// to use .where and .outputs
import { field } from "jexia-sdk-js/node"; 

const ds = dataOperations();
const ums = new UMSModule(); 

jexiaClient().init({
  projectID: "project_id",
}, ds, ums);

const user = await ums.signIn({    
  email: 'Elon@tesla.com',    
  password: 'secret-password'
});

const orders = dataModule.dataset("orders");
const deleteQuery = orders
.delete()
.where(field => field("verified").isEqualTo(true));  

// Either way, the response will be an array  
deleteQuery.subscribe(records => { 
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
# Select by id
curl -H "Authorization: Bearer $UMS_TOKEN" 
  -X DELETE "https://$PROJECT_ID.app.jexia.com/ds/orders?
  cond=\[\{\"field\":\"id\"\},\"=\",\"2a51593d-e99f-4025-b20b-159e226fc47d\"\]" | jq .
```

</template>
</CodeSwitcher>

As a result, you will get the next array of objects:

```JSON
[{
    "id": "e0e17683-f494-4f33-9563-dded795e3121",
    "created_at": "2020-02-15T19:43:39.784342Z",
    "updated_at": "2020-02-15T19:43:39.784342Z",
    "title":"Order2",
    "total":100,
    "verified":true
}]
```
## Update records

To update record you need to have Update action available for you for a particular resource. You can set up it in Policy area. 
I will show examples with Project User usage as it will be common usage. 

When you run Update action you will get back an array of affected records so you can sync changes with front end as well.  

::: tip
You can put id into update object, Jexia will find and update it automatically. 
:::

<CodeSwitcher :languages="{js:'JavaScript',bash:'cURL'}">
<template v-slot:js>

``` js
import { jexiaClient, UMSModule, dataOperations } from "jexia-sdk-js/node"; 
// to use .where and .outputs
import { field } from "jexia-sdk-js/node"; 

const ds = dataOperations();
const ums = new UMSModule(); 

jexiaClient().init({
  projectID: "project_id",
}, ds, ums);

const user = await ums.signIn({    
  email: 'Elon@tesla.com',    
  password: 'secret-password'
});

const orders = dataModule.dataset("orders");
const updateQuery = orders
                    .update([{id:"3005a8f8-b849-4525-b535-a0c765e1ef8e", verified: true }])
                    .where(field => field("total").isBetween(0,50).and(field("name").isLike('%avg')));  
// Either way, the response will be an array  
updateQuery.subscribe(records => { 
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
# Update by id
curl -H "Authorization: Bearer $UMS_TOKEN" -d '{
  "id":"3005a8f8-b849-4525-b535-a0c765e1ef8e",
  "text":"New post",
  "author":"Roy Ban",
  "views":2
}' -X PUT "https://$PROJECT_ID.app.jexia.com/ds/orders" | jq .
```

</template>
</CodeSwitcher>

As a result, you will get the next array of objects:

```JSON
[{
    "id": "3005a8f8-b849-4525-b535-a0c765e1ef8e",
    "created_at": "2020-02-15T19:43:39.784342Z",
    "updated_at": "2020-02-16T13:15:00.784342Z",
    "title":"Order1",
    "total":10,
    "verified":true
}]
```

## Related data
If you created multiple Datasets you can establish relations between them. You can do it under the Relations menu. Currently, Jexia supports **1-1, 1-m, m-1** relation types. 

<iframe width="700" height="394" src="https://www.youtube.com/embed/E_wxTnQ3clQ" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

![Relations](./ds_relation.png)

When do you need this? For example, you can keep users and their TODOs in separate Dataset's. With Jexia you do not need to care about external keys and index optimizations to organize all off this. All will be optimally managed by Jexia. 

Another cool thing, as soon as you set up relation, you can insert an object which has a parent - chield data inside and Jexia automatically put data in the proper places so you do not need care about this. For example, I have Dataset: `orders` and Dataset: `items` with 1 to many relations, between them. So I can insert into `orders` next object and data will land in the proper place: 

```json
{
    "title":"Order1",
    "total":10,
    "verified":false,
    "items": [
        {
            "name":"Item 1",
            "qty":2
        },
        {
            "name":"Item 3",
            "qty":20
        }
    ]
}
```
During fetching data you can specify if you want to get only parent or parent + chiled data.

<CodeSwitcher :languages="{js:'JavaScript',bash:'cURL'}">
<template v-slot:js>

``` js
sdk.dataset("orders")
  .select()
  .related("items", items => items.fields("qty"))
  .subscribe(res => {
    console.log(res);
  });
```
</template>
<template v-slot:bash>

``` bash
#GET https://<your-app-id>.app.jexia.com/ds/<your-dataset>?outputs=["<related_dataset>"]
#Next request will return only Qty field from related items dataset
https://{{projectID}}.app.jexia.com/ds/orders?outputs=["items.qty"] 
```

</template>
</CodeSwitcher>

```json
[
//   {
//     id: ...
//     created_at: ...
//     updated_at: ...
//     title:"Order1",
//     total:10,
//     verified:false,
//     items: [
//       {
//         id: ...
//         qty: 2
//       },
//       {
//         id: ...
//         qty:20
//       }
//     ]
//   }
// ]
```

If you want to get other related data, you just need to add them to request, Jexia will do matching automatically and send it back in result JSON. Easier than GaphQL, yeh? :)

::: tip
Please, keep in mind, currently, it is not possible to make a relation with Dataset itself(for example for multi-level menu). From another side, nobody stops you to store chield in a separate dataset and have 1-m relation between them. 
:::


## Multi-levels relations
You can have multiple levels of relation. For example: Article - Comments - Author - Salary. With Jexia you can build such a case and you will be able to get all data in one the response.   

<CodeSwitcher :languages="{js:'JavaScript',bash:'cURL'}">
<template v-slot:js>

``` js
dom.dataset("article")
  .select()
  .related("comments", comments => comments
    .fields("name", "likes")
    .related("authors"), author => author
      .fields("name", "id")
      .related("employee"), data => data
          .fields("salary", "id")
      )
    )
  )
  .subscribe()
```
</template>
<template v-slot:bash>

``` bash
#Next call will return all parent and chiled records and fields 
GET /ds/article/comments/authors/employee
#To get some specific fields:
GET /ds/article?outputs=["article.comments.author.name", "article.comments.author.employee.salary"]
```

</template>
</CodeSwitcher>

## Attach and detach records
If you would need to relate already existing data you can use `.attach()` and `.detach()` methods.
For this you need to specify to which parrent you want to attach chield record. In example I am adding to order with id = my_uuid
two items with id's "b4961b6a-85a2-4ee8-b946-9001c978c801" and "e199d460-c88f-4ab9-8373-1d6ad0bd0acb". 

<CodeSwitcher :languages="{js:'JavaScript',bash:'cURL'}">
<template v-slot:js>

```js
dom.dataset("order")
    .where(field("id").isEqualTo('my_uuid'));
    .attach("items", [
      "b4961b6a-85a2-4ee8-b946-9001c978c801",
      "e199d460-c88f-4ab9-8373-1d6ad0bd0acb",
    ])
    .subscribe();
```
</template>
<template v-slot:bash>

```bash
#PUT https://<your-app-id>.app.jexia.com/ds/<your-dataset>?action=attach&cond=...&action_cond=...&action_resource=...&action_etc=...
```
Parameter|Type/Value|Description
---------|----------|-----------
action|"attach"/"detach"|Select the action to perform
action_cond|JSON array|Condition for the action (to select the child records) same as Filter parameter filtering
action_resource|string|Name of the child resource must be accessible via relation from parent
action_order|JSON object|same as Filter parameter order
action_range|JSON object|same as Filter parameter range

</template>
</CodeSwitcher>

## Real-Time notification
If you want to have a real-time update about changes on the sets, you can use real-time notification which is built-in into Dataset, Fileset and Project Users. This is Pro function and you need to have a subscription for this. 

<iframe width="700" height="394" src="https://www.youtube.com/embed/TR9fcT8gXtM" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

After the action, you will get a notification with records ID which was modified. You can re-fetch data from Jexia. We are sending ID only due to security reasons, as it might be a situation that many users will be subscribed to notifications but they should not have access to data itself. With current approach, you can decide whom to show what.

You can use `.watch()` method to subscribe to the notifications. Allowed actions can be provided either as arguments or as an array:
1. created
2. updated
3. deleted
4. all (used by default)

You can unsubscribe from notifications any time by calling `.unsubscribe()` method.
Keep in mind that you would need to import `realTime` module

``` js
import { jexiaClient, dataOperations, realTime } from "jexia-sdk-js/node";
const ds = dataOperations();
const rtc = realTime();

// initialize jexia client
jexiaClient().init(credentials, ds, rtc);

const subscription = dataModule.dataset("orders")
  .watch("created", "deleted")
  .subscribe(messageObject => {
    console.log("Realtime message received:", messageObject.data);
  }, error => {
    console.log(error);
  });


subscription.unsubscribe();
```


## Filtering
With filtering, you can use to specify which data to fetch. As a result, you always will get an array of records, even if it will be only one record. There are different approaches applied to different languages. Please, check the preferable for you. 

<CodeSwitcher :languages="{js:'JavaScript',bash:'cURL'}">
<template v-slot:js>

``` js
import { field } from "jexia-sdk-js/node"; 
....
// below possible examples for filters:
   .where(field("title").isDifferentFrom("test")) 
   .where(field("total").isBetween(1,30))
   .where(field("total").isEqualOrGreaterThan(15))
   .where(field("total").isEqualOrLessThan(7))
   .where(field("total").isEqualTo(100))
   .where(field("total").isGreaterThan(57))
   .where(field("total").isLessThan(100))
   .where(field("id").isInArray(my_val))   // my_val=[uuid1,uuid2];
   .where(field("id").isNotInArray(my_val)) // my_val=[uuid1,uuid1];
   .where(field("title").isLike("%oby"))
   .where(field("title").isNotNull())
   .where(field("title").isNull())
   .where(field("title").satisfiesRegexp('[A-Z][0-9]*')) 

const isAuthorTom = field("user_name").isEqualTo("Tom");  
const isAuthorDick = field("user_name").isEqualTo("Dick");  

//example for applying AND / OR grouping.
const isAuthorTomOrDick = isAuthorTom.or(isAuthorDick);  
const isAuthorTomOrDick = isAuthorTom.and(isAuthorDick);  
// In order to use these conditions, they need to be added to a query through `.where` method  

dataModule.dataset("posts")  
 .select()
 .where(isAuthorTomOrDick)
 .subscribe(records => // posts of Tom and Dick); 
```
</template>
<template v-slot:bash>

Optional filtering parameters to specify which records to select. If it is not provided the request is applied on all records.
All filters build with the help of 3 variables: `field`, `comparator`, `value`.
Multiple queries within a (nested) condition are combined using `operator`.

``` bash
#cond=[<expression>, <comparator>, <expression>|<nested cond>, [<operator>, <expression>, <comparator>, <expression>|<nested cond>, [...]]]

$ curl -s 
-H "Authorization: Bearer $JEXIA_TOKEN" 
-X GET "https://$PROJECT_ID/ds/orders?cond=\[\{\"field\":\"total\"\},\">\",\"0\"\]" | jq .

#?cond=[{"field":"total"},">",0] // “<”, “=”, “!=”, “>=”, “<=”
#?cond=[{"field":"total"},"=",null]
#?cond=[{"field":"total"},"between",[0,8]]
#?cond=[{"field":"total"},"in",[0,5,15]]  // "not in"
#?cond=[{"field":"title"},"like","as"]
#?cond=[{"field":"title"},"regex","^[a-z]+$"]
#?cond=[{"field":"total"},">",100,["and",{"field":"title"},"like","as"]]
```

Below you can find examples for available comparators:

Comparator group | comparator| value | Applicable field types
-----------------|-----------|-------|-----------------------
Equality comparators|“>”, “<”, “=”, “!=”, “>=”, “<=”|single value matching field type|all fields   
Emptiness comparators|“null”|true or false|all fields
Range comparator|“between”|[start, end]|textual, numbers, date/times
Array comparators|“in”, “not in”|Array of allowed values (matching field type)|all fields
Pattern comparator|“like”|string value|textual
Regex comparator|“regex”|string value|textual

There are next operator available to combine filters: "and", "&&", "or" or "||"

</template>
</CodeSwitcher>


## Response fields
Sometimes you want to show specific fields from record versus all record. With Jexia you can have this. During data fetching, you need to specify what fields to get back. It is applicable to related data as well. 

<CodeSwitcher :languages="{js:'JavaScript',bash:'cURL'}">
<template v-slot:js>

``` js
const orders = dataModule.dataset("orders");

orders.select()
  .fields("title", "items.qty") // you can also pass an array of field names 
  .subscribe(records => {}); // you will get array of {id, title, author} records (id is always returned));
```
</template>
<template v-slot:bash>

``` bash
$ curl -s -H "Authorization: Bearer $UMS_TOKEN" -X GET "https://$PROJECT_ID.app.jexia.com/ds/orders?&outputs=\[\"titels\",\"items.qty\"\]" | jq .
```

</template>
</CodeSwitcher>

```json
[
  {
    "title": "Order1",
    "id": "bc3f13fd-5e0c-4319-98d4-f4373222488f",
    "items":[
      {
        "id":....,
        "qty":2
      }
    ]
  }
]
```


## Limit & Offset
You can use limit and offset on a Query to paginate your records. They can be used separately or together. Only setting the limit (to a value X) will make the query operate on the first X records. Only setting the offset will make the query operate on the last Y records, starting from the offset value.

<CodeSwitcher :languages="{js:'JavaScript',bash:'cURL'}">
<template v-slot:js>

``` js
const orders = dataModule.dataset("orders");

orders.select()
  .limit(2)
  .offset(5)
  .subscribe(records => // paginatedPosts will be an array of 2 records, starting from position 5);
```
</template>
<template v-slot:bash>

``` bash
$ curl -s -H "Authorization: Bearer $UMS_TOKEN" -X GET "https://$PROJECT_ID.app.jexia.com/ds/orders?range={\"limit\": 5, \"offset\": 3}" | jq .

```

</template>
</CodeSwitcher>

## Sorting
To sort output you can apply sort methods of Jexia, you can apply `Asc` and `Desc` directions. 

<CodeSwitcher :languages="{js:'JavaScript',bash:'cURL'}">
<template v-slot:js>

``` js
const orders = dataModule.dataset("orders");

posts
  .select()
  .sortAsc("total")
//.sortDesc("total")
  .subscribe(records => { 
    // you've got sorted records here 
  });
```
</template>
<template v-slot:bash>

``` bash
#order={"direction":"asc|desc","fields":["field_one","field_two","field_N"]}
$ curl -s -H "Authorization: Bearer $UMS_TOKEN" 
-X GET "https://$PROJECT_ID.app.jexia.com/ds/orders?order={\"direction\":\"desc\",\"fields\":[\"total\",\"created_at\"]}" | jq .
```

</template>
</CodeSwitcher>



## Aggregation functions
There are a few aggregation functions you can use in order to calculations before obtaining data:
1. max
2. min
3. sum
4. avg
5. count

You can combine output with other fields. 


<CodeSwitcher :languages="{js:'JavaScript',bash:'cURL'}">
<template v-slot:js>

``` js
const posts = dataModule.dataset("orders");

posts.select()
  .fields({ fn: "sum", field: "total" })
  .subscribe(result => {
  });
```
</template>
<template v-slot:bash>

``` bash
$ curl -s -H "Authorization: Bearer $UMS_TOKEN" -X GET "https://$PROJECT_ID.app.jexia.com/ds/orders?outputs=\[\"sum(total)\"\]" | jq .
```

</template>
</CodeSwitcher>

As a result, you will get next JSON
```json
[
  {
    "sum": 202
  }
]
```

## REST API Errors
During REST API request you can get next errors:

Code|Description
----|-----------
200|Record(s) created successfully. The response contains the full record(s) including its default fields.
400|Bad request. The request was somehow malformed and was not executed.
401|Invalid authentication. Access token was not provided or incorrect.
403|Forbidden. Access token does not have permission to insert the record(s) into this dataset.
404|Dataset not found
500|There is an internal error