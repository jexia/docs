# FileSets
JFS is used for uploading, fetching and manipulating files as any other user data. Basically, fileset is a dataset, but provides a way to maintain large data objects (files). At this point of time we are working in cooperation with partners (AWS S3) so all your files will be saved under your cloud storage. On Jexia site we will keep metadata and linkage for files, so you can easly get needed information (for example article images or user files).

To work with files you need to open access to specific Fileset via Policy.
Fileset is very similar to Dataset from configuration and usage so you do not need to have long learning curve to start using it. 

::: tip
Fileset similar to other modules can be used independently. It gives you flexibility to choose what modules to use in your project. For the future Fileset will have more and more features related to files operations. 
:::

When uploading or updating a file (record) the following things should be kept in mind:
1. Each Fileset contains a set of immutable fields. Some of them are id, created_at, updated_at, size, type, url and status. These fields are generally used to contain the metadata of the file which is filled internally by our API's. It is not possible to change the structure of these fields neither their values. These fields are optional in the fileset request. 

2. If a request contains an immutable field, its value must be its current value. Otherwise, it'll fail with a bad request (400).

3. If a request contains an unknown field, it gets added automatically as a schemaless field for this record.

The Fileset records contain the metadata of the file, besides the custom fields there are some predefined ones:
1. name - Name of the file
2. size - Size of the file in bytes
3. type - File type (supported types, note not mime-types and if the type is not found the extension is stored)
4. url - Public URL to the file
5. status:
    * in_progress - Jexia is still processing the file
    * succeeded - File got uploaded and processed successfully
    * failed - something went wrong during upload or processing of the file

Same as Dataset you can get real-time updated for Fileset. Below you can find example for this.

## Upload a file
Each request consists of two parts:

1. data record - It can be used to store metadata of your file or any other data that you want to associate with your file. As mentioned above if data contains an unknown field, it gets added automatically as a schemaless field for this record. The values of the data have to be a JSON object containing all the data related to file.

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
<template v-slot:ts>

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
Only one file can be uploaded per request for now. If there are multiple files in the body, only the first one will be processed and rest all will be ignored.
:::

</template>
</CodeSwitcher>

As result you will get next JSON
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

or another result in case file is under processing:

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

This is because when you submit a request to us we process the file and based on the size of file it might take us some time to process it. So we immediately return a response. The status at this time will be in progress.

When the process is finished and the file is uploaded we will send you an event via real-time to notify you of the status change. The final status can be a success or error depending on if the file was uploaded successfully.

::: tip
If you do not have real-time available for your project you can do request to Fileset to check methadata.  
:::

## Fetch file (metadata)
It's possible to query filesets in the same way as datasets, except insert query - you need to use upload() instead.
All fileset records are basically FileRecords, they have additional fields, such as name, size, url, etc.
These fields, as well as any custom fields, can be used for select queries (but you cannot update them).

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
<template v-slot:ts>

``` bash
```

</template>
</CodeSwitcher>

## Update file (metadata)
Update fileset in the same way as dataset. Updating a fileset record with new file is not supported.

<CodeSwitcher :languages="{js:'JavaScript',bash:'cURL'}">
<template v-slot:js>

``` js
jfs.fileset("fileset_name")  
 .update({ "isDefaultImage": false })  
 .where(field => field("name").isEqualTo("companyLogo.png"))
 .subscribe();  
```
</template>
<template v-slot:ts>

``` bash
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
<template v-slot:ts>

``` bash
```

</template>
</CodeSwitcher>

::: warning
Please, keep in mind while deleting methadata we are not deleting file itself. It is done for decoupling managing and storage for files. When you delete methadata Jexia exclude file from all fetching result but you can access file itself by direct link.
:::

## Setup for AWS S3
Currently, Jexia support connector to AWS S3 bucket. Below I will show you steps what needs to be done to setup S3 for you.

As soon as you log in to AWS console, go to the S3 service. 
![Create bucket](./s3_bucket.png)

Here you need to click the Create bucket button and enter the name for your bucket. 
![](./s3_createbacket.png)

In the next step you can choose to configure options if you wish or leave the default values.

Then on the Set permissions page, select all points related to ACL and deselect the others.
![S3 ACL setup](./s3_acl.png)

Make your final review and then create the bucket. As soon as it's done, open the bucket and move it to Permissions -> Bucket Policy. Here you will be able to put json to configure access policy for your bucket. You can find a template for this on our [GitHub page](https://github.com/jexia/aws-info/blob/master/permissions.json)

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

Now we need to create access key for your bucket. Click on your account, then select My Security Credentials.
![S3 Permission](./s3_mysecurity.png)

Go to Access keys row and create a new one.
![S3 Key Generation](./s3_keygen.png)

A pop-up with credentials will appear. Make sure you save these credentials as you will need to use them later for Jexia configuration.

![S3 Key](./s3_keys.png)

Now let's jump to the Jexia admin panel and create a new Fileset.
![New Fileset](./newjfs.png)

In this step you need to enter the Access Key ID and Secret Access Key that you received from AWS, and your bucket name. 
![New Fileset](./jfs2.png)

During creation we will try to load an empty file to your bucket and then try to read it back. If all goes well the new Fileset will be created. In case of any error with access, the Fileset will be created with an error sign. If that happens you will need to double-check all steps described in this document.

That's all, happy coding!

