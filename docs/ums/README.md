# <pro/> Project Users (UMS)
The **Project Users** or **User Management System** is the central hub of all user-related aspects of an application. It manages and controls users like signing up and sign-in, managing passwords, user groups, etc. 

UMS allows you to organize the sign-in process for your application without any development. To grant specific access to resources, you need to use policies where **Project Users** is the subject. 

<iframe width="700" height="394" src="https://www.youtube.com/embed/ZjffXZDuoGk" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>  

## Sign-up a User
UMS uses an email and password as user credentials. You can add as many extra fields as you need to keep all the needed information in one place (username, department and age etc). As for now, all fields are stored as schemaless so you are not able to setup validation or default values. We are working hard to make it available as soon as possible. 

Below you can find an example of how to sign-up a new user. 

<CodeSwitcher :languages="{js:'JavaScript',py:'Python',bash:'cURL'}">
<template v-slot:js>

``` js
import { jexiaClient, UMSModule } from "jexia-sdk-js";  

const ums = new UMSModule();   
jexiaClient().init({    
  projectID: "PROJECT_ID"
}, ums); 

ums.signUp({    
    email: "user@company.com",    
    password: "my_password"
  }, 
  {
    age: 25, 
    address: { 
      city: "Apeldoorn",
      country: "NL"
    }
  }).subscribe(
    user => {..do something with registered user}, 
    error=>{..handle error}
  );  
```

</template>
<template v-slot:py>

``` py
from jexia_sdk.http import HTTPClient

JEXIA_PROJECT_ID = 'project_id'
USER_EMAIL = 'user@jexia.com'
USER_PASSWORD = 'secret-password'

if __name__ == '__main__':
    client = HTTPClient()
    user = {{
      "email": "user@company.com",
      "password": "my_password"
    }, {
        "age": 25,
        "address": {
            "city": "Apeldoorn",
            "country": "NL"
        }
    }}
    # to request password reset
    res = client.request(
          method='POST',
          data=user,
          url='/ums/signup'
    )
    print(res)
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

Below you can find possible errors that may be returned:

|Code | Description|
|-----|------------|
201 | User created successfully. The response contains the full user (except the password) including default fields.
400 | Bad request. The request was somehow malformed and was not executed.
409 | User is already registered.
500 | There is an internal error

</template>
</CodeSwitcher>

After execution, you will receive an array similar to the following object:
``` json
{  
 "id": "005c8679-3fad-46fd-a93f-9484ea8ff738",
 "email": "user@company.com", 
 "active": true,
 "age": 25,
 "address": { 
      "city": "Apeldoorn",
      "country": "NL"
 }, 
 "created_at": "2017-12-31T23:59:59.123456Z", 
 "updated_at": "2017-12-31T23:59:59.123456Z"
}

```

## Sign-in a User
UMS uses an email and password as user credentials.  The user account should already exist in your project to successfully sign them in.

<CodeSwitcher :languages="{js:'JavaScript',py:'Python',bash:'cURL'}">
<template v-slot:js>

``` js
import { jexiaClient, UMSModule } from "jexia-sdk-js";  

const ums = new UMSModule();   
jexiaClient().init({    
  projectID: "PROJECT_ID",    
}, ums); 

ums.signIn({    
  email: 'Elon@tesla.com',    
  password: 'secret-password',    
  default: true,   
  alias: 'Elon Musk'  
}).subscribe(user => {
  // run request with current user token
}, error=>{
  console.log(error)
});  


```
Additional optional options:
* **default** - if true, this user account will be used for all further data operations by default.
* **alias** - account alias, you can use it to clarify which account is going to be used to perform data operation.

::: tip
Within Jexia's SDKs there is a possibility to sign-in with many users and run requests with different users. For this, you need to use an alias. If you did not specify under which user to run a query, the SDK will use user with the value **default:true**.   
:::

</template>
<template v-slot:py>

``` py
from jexia_sdk.http import HTTPClient

JEXIA_PROJECT_ID = 'project_id'
USER_EMAIL = 'user@jexia.com'
USER_PASSWORD = 'secret-password'

if __name__ == '__main__':
  client = HTTPClient()
  client.auth_consumption(
      project=JEXIA_PROJECT_ID,
      method='ums',
      email=USER_EMAIL,
      password=USER_PASSWORD
  )
  
```

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

## Fetch a User
To fetch an user you can look at the following methods:

<CodeSwitcher :languages="{js:'JavaScript',py:'Python',bash:'cURL'}">
<template v-slot:js>

``` js
// via alias
ums.getUser('Elon Musk').subscribe(user => {}, error=>{});    
// via email 
ums.getUser('elon@tesla.com').subscribe(user => {}, error=>{});   
```
</template>
<template v-slot:py>

``` py
currUser = client.request(
            method='GET',
            url='/ums/user/'
          ) 
print(currUser)
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

 
## Delete a User
To be able to delete a user, you need to provide a password. This is needed for security reasons.
You can do user management via CRUD operations. This method is mainly for the current user to delete themselves.
::: warning
This will be deprecated in future versions.
:::
<CodeSwitcher :languages="{js:'JavaScript',py:'Python',bash:'cURL'}">
<template v-slot:js>

``` js
ums.deleteUser('Elon@tesla.com', password)
.subscribe(user => {}, error=>{});    
```
</template>
<template v-slot:py>

``` py
res = client.request(
        method='DELETE',
        url='/ums/user/'
      ) 
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

## Change Password
There are two ways to change the password for a user by using their old password or by using automation.

### Using Their Password

<CodeSwitcher :languages="{js:'JavaScript',py:'Python',bash:'cURL'}">
<template v-slot:js>

``` js
ums
.changePassword('Elon@tesla.com', oldPassword, newPassword)
.subscribe(user => {}, error=>{});   
```
</template>
<template v-slot:py>

``` py
user = {
    "new_password": "my_new_password",
    "old_password": "my_old_password"
}
res = client.request(
        method='POST',
        data=user,
        url='/ums/changepassword/'
      ) 
print(res)  
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

### Using the Automation Module
You need to set up automation which will catch the `UMS: password reset request` event. Then, when you initiate a reset password, the user will get an email with a pre-made template message ([see Automation](/automation)). Inside you should create a link to a page with a new password entry form. From this page you can make a call `resetPassword` with a token from URL, thjs will allow Jexia to handle the request and apply changes to the new user to enable a new password.     

<CodeSwitcher :languages="{js:'JavaScript',py:'Python',bash:'cURL'}">
<template v-slot:js>
 
```js
// To request email with new token: 
ums
.requestResetPassword('Elon@tesla.com')
.subscribe(user => {}, error=>{});   

// To apply newpassword
ums
.resetPassword(Token, newPassword)
.subscribe(user => {}, error=>{});   
```

</template>
<template v-slot:py>

``` py
user = {
    "email": "user@email"
}
# to request password reset
res = client.request(
      method='POST',
      data=user,
      url='/ums/resetpassword/'
    )
# to apply changes
res = client.request(
      method='POST',
      data={"new_password": "jexia_super"},
      # token - user will get by email if you have Integration for SMTP
      url='ums/resetpassword/token'
    )
print(res)  
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

They have the same syntax and return values as corresponding data operation methods.
For this you need to create a policy with the following values: 
* **Subject**: All Users 
* **Resource**: All Users

<CodeSwitcher :languages="{js:'JavaScript',py:'Python',bash:'cURL'}">
<template v-slot:js>

``` js
// Select all active users  
ums.select()  
 .where(field => field("active").isEqualTo(true))  
 .subscribe(user => {}, error=>{});   
// Suspend Elon! 
ums.update({ active: false })  
 .where(field => field("email").isEqualTo("Elon@tesla.com"))  
 .subscribe(user => {}, error=>{});    
// Delete all suspended users  
ums.delete()  
 .where(field => field("active").isEqualTo(false))  
 .subscribe(user => {}, error=>{});   
```
</template>
<template v-slot:py>

``` py
  res = client.request(
          method='GET',
          url='/ums/users',
          cond='[....]'
        ) 
  print(res)
  
```

</template>
<template v-slot:bash>

``` bash
curl -H "Authorization: Bearer $UMS_TOKEN"
  -X GET "https://$PROJECT_ID.app.jexia.com/ums/users?cond=[....]" | jq .
```

</template>
</CodeSwitcher>