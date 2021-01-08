# <pro/> Project Users (UMS)
The **Project Users** or **User Management System** is the central hub of all user-related aspects of an application. It manages and controls users like signing up and sign-in, managing passwords, user groups, etc. 

UMS allows you to organize the sign-in process for your application without any development. To grant specific access to resources, you need to use policies where **Project Users** is the subject. 

<iframe width="700" height="394" src="https://www.youtube.com/embed/ZjffXZDuoGk" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>  

## Sign-up a User
UMS uses an email and password as user credentials.

You can pass extra fields to the `ums.signUp()` method. All extra fields will be stored as schemaless (unless you have created appropriated field at the UMS page of 
our management application [https://app.jexia.com](https://app.jexia.com)) therefore you are able to save as many fields as you need.

<CodeSwitcher :languages="{js:'JavaScript',py:'Python',bash:'cURL'}">
<template v-slot:js>

``` js
import { jexiaClient, UMSModule } from "jexia-sdk-js";  

const ums = new UMSModule();   
jexiaClient().init({    
  projectID: "PROJECT_ID"
}, ums); 

// For SDK > v5.0.0 
ums.signUp({    
    email: "user@company.com",    
    password: "my_password",
    age: 25, 
    address: { 
      city: "Apeldoorn",
      country: "NL"
    }
}).subscribe(
    user => {..do something with registered user}, 
    error=> {..handle error}
);  

//before < JS SDK v5.0.0.
ums.signUp({    
    email: "user@company.com",    
    password: "my_password"
}, {
    age: 25, 
    address: { 
        city: "Apeldoorn",
        country: "NL"
    }
}).subscribe(
    user => {..do something with registered user}, 
    error=> {..handle error}
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

### Return value
After execution, you will receive an object similar to the following:
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
There are two methods for signing in:

- [Providing email and password as credentials](#sign-in-with-e-mail-and-password).
- [Using Social Authentication (OAuth)](#sign-in-with-oauth).

### Sign-in with e-mail and password
In order to sign-in a user with regular credentials, user account should already exist in your project (that means you have to [sign-up](#sign-up-a-user) or create an user from the Jexia [WebApp](http://app.jexia.com/)).

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
    alias: 'Elon Musk',
}).subscribe(currentUser => {
    // return the user object of the currentUser
}, error => {
    console.log(error)
});
```

#### Additional options:
* **default** - if `true`, this user account will be used for all further data operations by default.
* **alias** - account alias, you can use it to clarify which account is going to be used to perform data operation.

#### Return value
The current User will be return, [check the details about the user object](#return-value)

::: tip
Within Jexia's SDKs there is a possibility to sign-in with many users and run requests with different users. 
For this, you need to use an alias. If you did not specify under which user to run a query, 
the SDK will use user with the value `default: true`
:::
::: tip
To switch between accounts that are logged-in, refer to [switchUser](#switch-user)
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

### Sign-in with OAuth
Because the way [OAuth 2.0 Protocol](https://oauth.net/2/) works, using it means there is an additional step which you authorize the application at the provider's page.
To enable OAuth for your users, you need to go to "Project Users" in your project management and setup the required settings in "OAuth Providers" tab.

After that, in your application you'll need to initialize the authorization process:

<CodeSwitcher :languages="{js:'JavaScript'}">
  <template v-slot:js>

  ``` js
  const oauthOptions = {
    /*
     * possible values: 'sign-up' or 'sign-in'
     */
    action: 'sign-up',
    /*
     * The name of the provider, the list will be available in the management of your project
     */
    provider: 'facebook',
    /*
     * The URL which the oauth provider should redirect to.
     * This is optional and when not provided, the url you setup in your project will be used.
     */
    redirect: 'https://mydomain.com/oauth/init',
  };

  /*
   * When running in the browser, it will automatically redirect to the provider's page.
   */
  ums.initOAuth(oauthOptions).subscribe();

  /*
   * When running in NodeJS, it will resolve to the URL which user should navigate to in order to start authentication.
   * You can also pass `false` to the second argument so you can redirect some other time.
   */
  ums.initOAuth(oauthOptions, false).subscribe(url => {
    // you can also redirect by yourself
    window.location.assign(url);
  });

  ```
  </template>
</CodeSwitcher>

After the user redirected to the provider's page, they should authorize and be redirected back to the `redirect` URL you passed. This request will contain two query parameters, `code` and `state`, you should get them and pass to sign in:

<CodeSwitcher :languages="{js:'JavaScript'}">
  <template v-slot:js>

  ``` js
  // Let's say the full redirected URL was: https://mydomain.com/oauth/init?code=some-random-code&state=sign-up
  ums.signIn({
    code: 'some-random-code',
    state: 'sign-up',
    default: true, // optional
    alias: 'Elon Musk', // optional
  }).subscribe(currentUser => {
    // return the user object of the currentUser
  }, error => {
    console.log(error)
  });
  ```
  </template>
</CodeSwitcher>

## Sign-out a User

The sign-out function is fairly simple as it just deletes all tokens that belongs to a user. That means, also the aliases 
that where set during the [sign-in](#sign-in-a-user) are removed.

<CodeSwitcher :languages="{js:'JavaScript'}">
<template v-slot:js>

``` js
import { jexiaClient, UMSModule } from "jexia-sdk-js";

const ums = new UMSModule();
jexiaClient().init({
    projectID: "PROJECT_ID",
}, ums);

// ... user sign in

// via alias
ums.signOut('Elon Musk');

// via email
ums.signOut('Elon@tesla.com');

// fallback on the DEFAULT alias, if set during login.
ums.signOut();
```
</template>
</CodeSwitcher>

## Switch user
With SDK you can log in multiple users without logging out the user(s). 
To switch between users you can use the following code.

<CodeSwitcher :languages="{js:'JavaScript'}">
<template v-slot:js>

``` js
import { jexiaClient, UMSModule } from "jexia-sdk-js";

const ums = new UMSModule();
jexiaClient().init({
    projectID: "PROJECT_ID",
}, ums);

// ... user sign in

// via alias
ums.switchUser('Elon Musk');

// via email
ums.switchUser('Elon@tesla.com');
```
</template>
</CodeSwitcher>

## Current user
When logged in we also set the current logged-in user for you so you can refer to it on request.

#### Return value
See the detailed object [here](#return-value)

<CodeSwitcher :languages="{js:'JavaScript',py:'Python',bash:'cURL'}">
<template v-slot:js>

``` js
const currentUser = ums.currentUser;
```
</template>
</CodeSwitcher>

## Fetch a User
Fetching a user can be done by providing an alias or without, so the SDK will fetch a user based on the `DEFAULT` alias.

#### Return value
See the detailed object [here](#return-value)


::: tip
When logging in, we fetch and set the current to `ums.currentUser` See [here](#current-user). 
:::

<CodeSwitcher :languages="{js:'JavaScript',py:'Python',bash:'cURL'}">
<template v-slot:js>

``` js
// via alias
ums.getUser('Elon Musk').subscribe(user => {
    // user holds the currentUser object
});

// via email
ums.getUser('elon@tesla.com').subscribe(user => {
    // user holds the currentUser object
});

// fallback on the DEFAULT alias, if set during login.
ums.getUser().subscribe(user => {
    // user holds the currentUser object
});
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

## Is User logged in
In some situations you need to check inside your app if a user has been logged in.

<CodeSwitcher :languages="{js:'JavaScript',py:'Python',bash:'cURL'}">
<template v-slot:js>

``` js
// via alias
ums.isLoggedIn('Elon Musk').subscribe(isLoggedIn => {
    // return if the user is logged-in or not
});

// via email
ums.isLoggedIn('elon@tesla.com').subscribe(isLoggedIn => {
    // return if the user is logged-in or not
});

// by omiting the "alias", the SDK will check upon the default alias
ums.isLoggedIn().subscribe(isLoggedIn => {
    // return if the user is logged-in or not
});
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
. subscribe(user => {}, error=>{});   

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
    .subscribe(user => {}, error => {});   

// Suspend Elon! 
ums.update({ active: false })  
    .where(field => field("email").isEqualTo("Elon@tesla.com"))  
    .subscribe(user => {}, error => {});    

// Delete all suspended users  
ums.delete()  
    .where(field => field("active").isEqualTo(false))  
    .subscribe(user => {}, error => {});   
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

## RTC
Using RTC and the UMS will work perfectly together. The SDK will handle all Token management from and to Websocket connection. 

<CodeSwitcher :languages="{js:'JavaScript'}">
<template v-slot:js>

``` js
import {
  jexiaClient,
  dataOperations,
  UMSModule,
  realTime,
} from "jexia-sdk-js/node";

const ds = dataOperations();
const jfs = fileOperations();
const ums = new UMSModule();
const rtc = realTime();

jexiaClient().init({
        projectID: '6d3fc0ca-4f7c-4a25-9c54-e6761b25ae08',
    },
    ums,
    ds,
    rtc,
);

ds.dataset('orders')
    .watch('all')
    .subscribe(
        res => console.log(res),
        error => console.log(error),
    );

ums.signIn({
    email: 'john@doe.com',
    password: 'secretPassword',
    default: true,
});

// from here the RTC will using the "john@doe.com" tokens

ums.signIn({
    email: 'willem@doe.com',
    password: 'secretPassword',
    default: true,
});

// from here the RTC switch and set the tokens from "willem@doe.com"
// the same applied for the switchUser() and signOut()

```
</template>
</CodeSwitcher>
