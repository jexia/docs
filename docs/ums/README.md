# Project Users (UMS)
The Project Users or User Management System is the central hub of all user-related aspects of an application. It manages and controls users like signing up and sign-in users, manage passwords, user groups, etc. 

::: tip
Jexia User Management System is only available for the project with a Professional subscription.
:::

UMS allows you to organize the sign-in process for your application without any development. To grant specific access to resources you need to use Policy where Project Users become a subject.   

## Sign up user
UMS is using email and password as user credentials. You can add as many extra fields as you need to keep all the needed information in one place(user name, department, age, etc). As for now all fields stored as schemaless so you are not able to setup validation or default values. We are working hard to make it available as soon as possible. 

Below you can find an example of how to make sign-up for a new user. 

<CodeSwitcher :languages="{js:'JavaScript',bash:'cURL'}">
<template v-slot:js>

``` js
import { jexiaClient, UMSModule } from "jexia-sdk-js";  

const ums = new UMSModule();   
jexiaClient().init({    
  projectID: "your-project-id"
}, ums); 

const user = await ums.signUp({    
  email: "user@company.com",    
  password: "my_password", 
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
curl -X POST -d '{
  "email": "user@company.com",
  "password": "my_password",
  "age": 25, 
  "address": { 
      "city": "Apeldoorn",
      "country": "NL"
   }
}' "https://$PROJECT_ID.app.jexia.com/ums/signup" | jq .
```

Below you can find possible errors:

|Code | Description|
|-----|------------|
201 | User created successfully. The response contains the full user (except the password) including default fields.
400 | Bad request. The request was somehow malformed and was not executed.
409 | User is already registered.
500 | There is an internal error

</template>
</CodeSwitcher>

As respond you will get next JSON object:
``` json
{  
 id: "005c8679-3fad-46fd-a93f-9484ea8ff738",
 email: "user@company.com", 
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
UMS is using email and password as user credentials. The user account should exist in a project.

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
With JS SDK there is a possibility to do sign in with many users and run requests with different users. For this, you need to use an alias.If you did not specify under which user to run query, SDK will use user with **default:true**.   
:::

</template>
<template v-slot:bash>

``` bash
export UMS_TOKEN=`curl -X POST -d '{
  "method":"ums",
  "email":"'"$TEST_USER"'",
  "password":"'"$TEST_USER_PSW"'"
}' "https://$PROJECT_ID.app.jexia.com/auth" | jq -r .access_token`
```

</template>
</CodeSwitcher>

## Fetch a user
To get current sign in user you need to run next methods:

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
curl 
-H "Authorization: Bearer $UMS_TOKEN"
-X GET "https://$PROJECT_ID.app.jexia.com/ums/user/" | jq .
```

</template>
</CodeSwitcher>

 
## Delete user
To be able to delete the user you need to provide a password. It is needed most for security reasons.
You can do user management via CRUD operations. This method is mostly for the current user to delete himself. 
Will be deprecated in future versions.

<CodeSwitcher :languages="{js:'JavaScript',bash:'cURL'}">
<template v-slot:js>

``` js
ums.deleteUser('Elon@tesla.com', password); 
```
</template>
<template v-slot:bash>

``` bash
curl 
-H "Authorization: Bearer $UMS_TOKEN"
-X DELETE "https://$PROJECT_ID.app.jexia.com/ums/user/" | jq .
```

</template>
</CodeSwitcher>

## Change password
There are two ways to change the password for the user by using his old password or by using automation.

By using his old password:

<CodeSwitcher :languages="{js:'JavaScript',bash:'cURL'}">
<template v-slot:js>

``` js
ums.changePassword('Elon@tesla.com', oldPassword, newPassword); 
```
</template>
<template v-slot:bash>

``` bash
curl 
-H "Authorization: Bearer $UMS_TOKEN"
-X POST -d '{
  "new_password": "my_new_password",
  "old_password": "my_old_password"
}' "https://$PROJECT_ID.app.jexia.com/ums/changepassword/" | jq .
```

</template>
</CodeSwitcher>

by using Automation module. You need to set up automation which will catch `UMS: password reset request`. Then, when you initiate a reset password, the user will get an email with a templated message (see Automation). Inside you should create a link on a page with new password entry form. From this page you can make a call `resetPassword` with a token from URL, so Jexia will apply changes for a new password.     

<CodeSwitcher :languages="{js:'JavaScript',bash:'cURL'}">
<template v-slot:js>
 
```js
// To request email with new token: 
ums.requestResetPassword('Elon@tesla.com');

// To apply newpassword
ums.resetPassword(Token, newPassword);
```

</template>
<template v-slot:bash>

``` bash
# To request token for change password for specific email
curl 
-X POST -d '{
  "email":"user@email"
}' "https://$PROJECT_ID.app.jexia.com/ums/resetpassword/" | jq .


# To apply new password
curl 
-X POST -d '{
  "new_password": "jexia_super"
}' "https://$PROJECT_ID.app.jexia.com/ums/resetpassword/token" | jq .
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
curl -H "Authorization: Bearer $UMS_TOKEN"
  -X GET "https://$PROJECT_ID.app.jexia.com/ums/users?cond=[....]" | jq .
```

</template>
</CodeSwitcher>