# Project Users (UMS)
The Proect Users or User Management System is the central hub of all user-related aspects of an application. It manages and controls users like signing up and signing in users, manage passwords. 

::: tip
Jexia User Management System is only available on Professional project.
:::

UMS allow you to cover authentification part and manage which user can signin into your application. To grant specific access to resources you need to use Policy where Project Users become as a subject.   

## Sign up user
UMS uses email and password as user credentials. You can add as many extra fields as you need to keep all needed information.
For example information about user profile. As for now all fields stored as schemaless so you are not able to re-use validation or defualt values. We are working hard to make it available as soon as possible. 
 
<CodeSwitcher :languages="{js:'JavaScript',bash:'cURL'}">
<template v-slot:js>

``` js
import { jexiaClient, UMSModule } from "jexia-sdk-js";  

const ums = new UMSModule();   
jexiaClient().init({    
  projectID: "your-project-id"
}, ums); 

const user = await ums.signUp({    
  email: "robert@company.com",    
  password: "qwert1234", 
  age: 25, 
  address: { 
      city: "Apeldoorn",
      country: "NL"
  }
});  
```

</template>
<template v-slot:bash>

``` bash
POST https://<project-id>.app.jexia.com/ums/signup
{
  "email": "myemail@mail.com",
  "password": "my_password",
  "age": 25, 
  "address": { 
      "city": "Apeldoorn",
      "country": "NL"
   }
}
```

|Code | Description|
|-----|------------|
201 | User created successfully. Response contains the full user (except password) including default fields.
400 | Bad request. Request was somehow malformed and was not executed.
409 | User is already registered.
500 | There is an internal error

</template>
</CodeSwitcher>

As respond you will get next JSON object:
``` json
{  
 id: "005c8679-3fad-46fd-a93f-9484ea8ff738",
 email: "robert@company.com", 
 active: true,
 age: 25,
 address: { 
      city: "Apeldoorn",
      country: "NL"
 }, 
 created_at: "2017-12-31T23:59:59.123456Z", 
 updated_at: "2017-12-31T23:59:59.123456Z"
}

```

## Sign In user
UMS uses email and password as user credentials. User account should exist in a project.

<CodeSwitcher :languages="{js:'JavaScript',bash:'cURL'}">
<template v-slot:js>

``` js
import { jexiaClient, UMSModule } from "jexia-sdk-js";  

const ums = new UMSModule();   
jexiaClient().init({    
  projectID: "your-project-id",    
}, ums); 

const user = await ums.signIn({    
  email: 'Elon@tesla.com',    
  password: 'secret-password',    
  default: true,   
  alias: 'Elon Musk'  
});  

dom.dataset('rockets', 'Elon Mask').select();  
dom.dataset('rockets').select();  
```
Additional options (both are optional):
* default - if true, this user account will be used for all further data operations by default
* alias - account alias. You can use it to clarify which account is going to be used to perform data operation

::: tip
There are possibility to do sign in with many users and run request with different users. For this you need to use alias.
If you did not specify under which user to run query, SDK will use user with **default:true**.   
:::

</template>
<template v-slot:bash>

``` bash
```

</template>
</CodeSwitcher>

## Fetch a user
To get one of sign in user or current user you need to run next methods:

<CodeSwitcher :languages="{js:'JavaScript',bash:'cURL'}">
<template v-slot:js>

``` js
// via alias
const user = await ums.getUser('Elon Musk'); 
// via email 
const user = await ums.getUser('elon@tesla.com'); 
```
</template>
<template v-slot:bash>

``` bash
```

</template>
</CodeSwitcher>

 
## Delete user
To be able to delete user you need to provide password. It is needed mostly from security reason.
You can do user management via CRUD operations. This method is mostly for current user to delete himself. 
Will be depricated in future versions.

<CodeSwitcher :languages="{js:'JavaScript',bash:'cURL'}">
<template v-slot:js>

``` js
ums.deleteUser('Elon@tesla.com', password); 
```
</template>
<template v-slot:bash>

``` bash
```

</template>
</CodeSwitcher>

## Change password
There is two ways to change password for user by using his old password or by using automation.

By using his old password:

<CodeSwitcher :languages="{js:'JavaScript',bash:'cURL'}">
<template v-slot:js>

``` js
ums.changePassword('Elon@tesla.com', oldPassword, newPassword); 
```
</template>
<template v-slot:bash>

``` bash
```

</template>
</CodeSwitcher>

## Users CRUD
It is also possible to use CRUD methods. 

They have the same syntax and return values as corresponding data operations methods.
For this you need to put in policy setup: 
* subject:AllUsers 
* resource:AllUsers

<CodeSwitcher :languages="{js:'JavaScript',bash:'cURL'}">
<template v-slot:js>

``` js
// select all active users  
ums.select()  
 .where(field => field("active").isEqualTo(true))  
 .subscribe();  
// suspend Elon! 
ums.update({ active: false })  
 .where(field => field("email").isEqualTo("Elon@tesla.com"))  
 .subscribe();  
// delete all suspended users  
ums.delete()  
 .where(field => field("active").isEqualTo(false))  
 .subscribe(); 
```
</template>
<template v-slot:bash>

``` bash
```

</template>
</CodeSwitcher>