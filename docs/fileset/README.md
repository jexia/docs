# FileSets

<iframe width="700" height="394" src="https://www.youtube.com/embed/S4Yz3I3MwGU" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

JFS is used for indexing, fetching and manipulating files like any other user data. Fileset is a dataset but provides a way to maintain large data objects like files. At this point, we are working in cooperation with partners (Digital Ocean, AWS S3) so all your files will be saved under your cloud storage. On Jexia's site we will keep only metadata and the URL for the files and you can manipulate the data in the same way as with Dataset.

To work with files, you need to open access to specific fileset via policy.
Fileset is very similar to Dataset with configuration and usage so you don't need to have a long learning curve to start using it.

::: tip
Fileset is similar to other modules but can be used independently. It gives you the flexibility to choose what modules to use in your project. The future fileset will have more features related to files operations.
:::

When uploading or updating a file record, the following things should be kept in mind:
1. Each fileset contains a set of immutable fields: id, created_at, updated_at, size, type, url and status. These fields are generally used to contain the metadata of the file which is filled internally by our API. It is not possible to change validation, default values of these fields and their values.

2. If a request contains an immutable field, it's value must be it's current value. If this is not the case, it will fail with a bad request (400) error.

3. If a request contains an unknown field, it gets added automatically as a schemaless field for this record.

The fileset records contain the metadata of the file. Besides the custom fields there are some predefined ones:
1. name - Name of the file
2. size - Size of the file in bytes
3. type - File type (supported types, note not mime-types and if the type is not found the extension is stored)
4. url - Public URL to the file
5. status:
    * in_progress - Jexia is still processing the file
    * succeeded - File got uploaded and processed successfully
    * failed - something went wrong during the upload or processing of the file

Same as Dataset you can get real-time notifications for fileset. Below you can find the example for this.

## Upload a file
Each request consists of two parts:

1. data record - It can be used to add some metadata of your file. As mentioned above if the data object contains a field, which is not in the schema, it will be added automatically as a schemaless field for this record.

2. file record - It contains your actual file.

<CodeSwitcher :languages="{js:'JavaScript',bash:'cURL'}">
<template v-slot:js>

``` js
import { jexiaClient, fileOperations, realTime } from "jexia-sdk-js/node";
import * as fs from "fs";

const jfs = fileOperations({
  uploadWaitForCompleted: true    
});

jexiaClient().init({
  projectID: "your-project-id",
  key: "your-project-key",
  secret: "your-project-secret"
}, jfs, realTime());

const fileset = jfs.fileset("fileset_name");

const records = [{
  data: {
    description: "just a file"
  },
  file: fs.createReadStream("../assets/logo.png")
}];

fileset.upload(records).subscribe(fileRecord => {
  console.log(fileRecord);
});

```
</template>
<template v-slot:bash>

``` bash
POST https://<project-id>.app.jexia.com/fs/<fileset-name>
"Content-Type": "multipart/form-data;boundary=boundary"
--boundary 
Content-Disposition: form-data; name="description" 
 
this is my file 
--boundary 
Content-Disposition: form-data; name="file"; filename="my_file.txt" 
 
<file data>
--boundary--
```
::: warning
Only one file can be uploaded per request for now. If there are multiple files in the body, only the first one will be processed and the rest will be ignored.
:::

</template>
</CodeSwitcher>

As a result, you will get next JSON
``` json
    { id: "11a12f17-8367-4114-a588-ae98a6cb3cda",
      created_at: "2019-05-24T07:17:37.325882Z",
      updated_at: "2019-05-24T07:18:40.455764Z",
      name: "logo.png",
      size: 42341,
      type: "png",
      url: "https://...",
      status: "completed" }
```

or another result, in case file is under processing:

``` json
  { id: "11a12f17-8367-4114-a588-ae98a6cb3cda",
      created_at: "2019-05-24T07:17:37.325882Z",
      updated_at: "2019-05-24T07:17:37.325882Z",
      name: null,
      size: null,
      type: null,
      url: null,
      status: "in_progress" }
```

When you submit a file request you will receive back the request ID along with status. Most of the other metadata will be either empty or null.

This is because when you submit a request to us, we process the file and based on the size of the file it might take some time to process it. The response will be immediately returned when as soon as processing will be finished. The status at this time will be in progress.

When the process is finished and the file is uploaded we will send you an event via real-time to notify you of the status change. The final status can be a success or error depending on if the file was uploaded successfully.

::: tip
If you do not have real-time available for your project you can do a request to fileset to check metadata.  
:::

## Fetch file (metadata)
It's possible to query fileset in the same way as Datasets, except insert query - you need to use upload() instead.
All fileset records will have fields such as name, size, URL, etc. These fields, as well as any custom fields, can be used for select queries (but you can't update them).

<CodeSwitcher :languages="{js:'JavaScript',bash:'cURL'}">
<template v-slot:js>

``` js
jfs.fileset("fileset_name")  
 .select("name", "url")  
 .where(field => field("size").isGreaterThan(1024000))  
 .subscribe();  

// array of files that fit to the condition will be returned  
// files === [{ name: "file1.jpj", url: "https://..." }, {...}, ...]  
```
</template>
<template v-slot:bash>

``` bash
$ curl -s 
-H "Authorization: Bearer $JEXIA_TOKEN" 
-X GET "https://$PROJECT_ID/ds/fileset_name?cond=\[\{\"field\":\"size\"\},\">\",1024000\]" | jq .
```

</template>
</CodeSwitcher>

## Update file (metadata)
Update a fileset in the same way as a Dataset. 

::: warning
Updating a fileset record with a new file is not supported. Only the metadata can be changed. If you need to upload new file, please, create a new record. 
:::

<CodeSwitcher :languages="{js:'JavaScript',bash:'cURL'}">
<template v-slot:js>

``` js
jfs.fileset("fileset_name")  
 .update({ "isDefaultImage": false })  
 .where(field => field("name").isEqualTo("companyLogo.png"))
 .subscribe();  
```
</template>
<template v-slot:bash>

``` bash
$ curl -s 
-H "Authorization: Bearer $JEXIA_TOKEN" -d '{
  "id":"3005a8f8-b849-4525-b535-a0c765e1ef8e",
  "isDefaultImage":false
}'
-X PATCH "https://$PROJECT_ID/ds/fileset_name?cond=\[\{\"field\":\"size\"\},\">\",1024000\]" | jq .
```

</template>
</CodeSwitcher>


## Delete file (metadata)

<CodeSwitcher :languages="{js:'JavaScript',bash:'cURL'}">
<template v-slot:js>

``` js
jfs.fileset("fileset_name")  
 .delete()  
 .where(field => field("size").isGreaterThan(1024000))  
 .subscribe();
```
</template>
<template v-slot:bash>

``` bash
$ curl -s 
-H "Authorization: Bearer $JEXIA_TOKEN" 
-X DELETE "https://$PROJECT_ID/ds/fileset_name?cond=\[\{\"field\":\"size\"\},\">\",1024000\]" | jq .
```

</template>
</CodeSwitcher>

::: warning
Please, keep in mind while deleting metadata we are not deleting the file itself. It is done for decoupling, managing and storage for files. When you delete metadata Jexia excludes the file from all fetching result but you can access the file itself by the direct link.
:::

## Setup for AWS S3
Currently, Jexia supports the connector to AWS S3 bucket. Below you can see the steps that are needed to be done to setup S3.

As soon as you log in to AWS console, go to the S3 service. 
![Create bucket](./s3_bucket.png)

Here you need to click the Create bucket button and enter the name for your bucket. 
![](./s3_createbacket.png)

In the next, step you can choose to configure options if you wish or leave the default values.

Then on the Set permissions page, select all points related to ACL and deselect the others.
![S3 ACL setup](./s3_acl.png)

Make your final review and then create the bucket. As soon as it's done, open the bucket and move it to Permissions -> Bucket Policy. Here you will be able to put a JSON to configure access policy for your bucket. You can find a template for this on our [GitHub page](https://github.com/jexia/aws-info/blob/master/permissions.json)

::: warning
!!!Please, change this row from template with your bucket name:  "Resource": "arn:aws:s3:::bucket-name/*"
:::

``` json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicAccess",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::bucket-name/*"
        } 
    ]
}
```
![S3 Permission](./s3_permission.png)

Now we need to create an access key for your bucket. Click on your account, then select My Security Credentials.
![S3 Permission](./s3_mysecurity.png)

Go to Access keys row and create a new one.
![S3 Key Generation](./s3_keygen.png)

A pop-up with credentials will appear. Make sure you save these credentials as you will need to use them later for Jexia configuration.

![S3 Key](./s3_keys.png)

Now let's jump to the Jexia admin panel and create a new fileset.
![New Fileset](./newjfs.png)

In this step, you need to enter your bucket name, the Access Key ID and Secret Access Key that you received from AWS.
![New Fileset](./jfs2.png)

During creation, we will try to load an empty file to your bucket and then try to read it back. If all goes well, the new fileset will be created. In case of any error, the fileset will be created with an error sign. If that happens, you will need to double-check all steps described in this document.

That's all, happy coding!

