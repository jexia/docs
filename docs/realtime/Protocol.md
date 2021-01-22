# RTC protocol

The WebSocket API provides means to receive events on change resources (that the JWT has access to).

## Connecting to the WebSocket API

Build the URL according to the template below:

```
wss://<project-id>.<zone>.app.jexia.com/rtc?access_token=<jwt>
```
ARGUMENT     | TYPE   | DESCRIPTION                           | EXAMPLE
-------------|--------|---------------------------------------|----------------------------------------
project-id   | UUID   | unique identifier/hash of the project | `4f8c6ee3-f2d1-47b8-83c4-c5250b86cab4`
zone         | string | project zone                          | `nl00`
jwt          | string | valid token obtained after logging into the project using the API key credentials or any other method | `eyJhbGciOiJS... ...aev96IlwB1OFzDmyw`

Connecting to the WebSocket API is done using a WebSocket client and connect it to the WebSocket address. Use one of the available WebSocket clients to create a connection:
- [Simple WebSocket Client](https://chrome.google.com/webstore/detail/simple-websocket-client/pfdhoblngboilpfeibdedpjgfnlcodoo) (Chrome extension)
- [Smart Websocket Client](https://chrome.google.com/webstore/detail/smart-websocket-client/omalebghpgejjiaoknljcfmglgbpocdp) (Chrome extension)
- [WebSocket King](https://websocketking.com) (Online WebSocket client)

## Before you start
1. Create a User/API key.
2. Log In providing valid credentials and method (check [here](../auth/README.md) for documentation).
3. Create some resources with WebApp or management API.
4. Make sure that User/API key you are going to use has all reuired permissions (policies) on the resources, create policies if not.

## Sending and Receiving messages
After establishing the connection to the WebSocket API, the client can send messages to perform actions, like subscribing to particular events and receive messages, like notifications about changes. Both send and received messages must be using JSON encoding.

```json
{
  "type": "<message type>",
  "data": "<message data>"
}
```

ARGUMENT | TYPE   | DESCRIPTION            | EXAMPLE
---------|--------|------------------------|-----------------------------------------------
type     | String | message type           | `subscribe` / `unsubscribe` / `publish` ...
data     | Any    | message data (payload) | `{"command":"unsubscribe","arguments":{...}}`


### Command messages

```json
{
  "type": "command",
  "data": {
    "command": "<command>",
    "correlation_id": "<correlation ID: any valid JSON value>",
    "arguments": { "<command arguments>" }
  }
}
```

Each command has the `command` field in the `data` object to specify the command and optionally an `arguments` object to specify the arguments of the command.
Field `correlation_id` is OPTIONAL and ignored by RTC, it is generated/provided by the client and returned back as apart of command response AS IS (in case it was provided by WebSocket client).

The client/JWT needs to have the proper permissions for the command to be accepted and executed.

#### Command Response messages

```json
{
  "type": "command response",
  "data": {
    "request": "<request fields including correlation_id if it was provided>",
    "response": "<response fields>",
    "error": {
      "code": "<error code>",
      "info": "<human-readable information>"
    }
  }
}
```

* `<request fields>` - object containing a copy of the request message
* `<request fields>` - object containing the command response data (if available)
* `error` - when the command failed, this object contains the error information
  * `<error code>` - Easy to use code for application to determine what went wrong (see [list of errors](#error-codes))
  * `<human-readable information>` - Textual (English) information about the error

#### Event messages
```json
{
  "type": "event",
  "data": {
    "action": "<action>",
    "resource": {
      "type": "<resource type>",
      "name": "<resource name>",
    },
    "modifier": {
      "id": "<modifier identifier>",
    },
    "timestamp": "<timestamp of change>",
    "data": [{ "<event data>" }]
  }
}
```

* `<action>`, `<resource type>`, `<resource name>` - Describe the event that happened on which resource (see [Events](#events) for more information).
* `<modifier identifier>` - Optional field describing who/what changed the event (see [Events](#events) for more information).
* `<timestamp>` - ISO 8601 timestamp as an indication when the event occurred.
* `<event data>` contains the data of the event, which includes only the `ID` field for the moment.


#### Notification messages

  ```json
  {
    "type": "notification",
    "data": {
      "code": "<notification code>",
      "info": "<human readable information>",
      "data": "<additional data>"
    }
  }
```
* `<additional data>` contains the data of the notification, if available, depending on the notification (code).

### Notification codes

Code | Description           | Details
-----|-----------------------|---------
1    | Token about to expire | The token is about to expire, it is a good time to send a [replacement token](#replace-jwt).

### Error codes

Code  | Description           | Details
------|-----------------------|---------
1     | Internal Error        | Something went wrong in RTC which is not due to wrong user input.
2     | Unauthorized          | The client JWT is not allowed to execute the command.
3     | Invalid token         | The provided token is not valid
4     | Formatting error      | The received message could not be decoded.
5     | Unknown type          | The provided type was not recognized/supported.
6     | Unknown command       | The provided command was not recognized.
1000  | Unknown resource type | The provided resource type was not recognized.
1001  | Unknown resource name | The provided resource name does not exists for the given type.
1002  | Unknown action        | One of the provided action(s) is not recognized/supported.

## Refreshing JWT

The JWT has an expiration time, so to keep the WebSocket connection alive, a new JWT token needs to be provided before the old one is expired.

The WebSocket server will notify the client that it is time to replace the token with a new one, or the client can send new tokens manually.

### Replace JWT

Use the following command to replace the current [JWT token](#connecting-to-the-websocket-api) with a new one (e.g. when the current token is about to expire).

Note that `<new JWT>` is the (access) token, not the refresh token!

```json
{
  "type": "command",
  "data": {
    "command": "jwt replace",
    "arguments": {
      "token": "<new JWT>"
    }
  }
}
```

A typical [error response](#error-codes) is 3 (Invalid token)

### Reminder

To remind the client to send a new token, the WebSocket server will send a [notification message](#notification-codes):

```json
{
  "type": "notification",
  "data": {
    "code": 1,
    "info": "<human readable information>"
  }
}
```

The client can choose to ignore this message (and send the token itself periodically), or use this message as a reminder.

## Events
Some commonly used variables are:
* `<action>` - Event action to receive, can be for example `created`, `updated`, `deleted`. `all` is used to receive all (applicable) events.
* `<resource type>` - Type of resource that is referred to, for example the type `ds` stands for datasets (provided by the DataSet module) and `ums` stands for user management system (provided by the UMS module). Check module documentation to see what resource type it is providing.
* `<resource name>` - Name of the resource, for example it is the name of a dataset that is used, when it got created in the project management UI. Some modules have hard-coded resource names, so check the module documentation if unsure.
* `<modifier type>` - Type of modifier (entity) that changes the resource, for example `apikey`
* `<modifier identifier>` - Unique identifier of the modifier

### Subscribe to resource event

Send the following command to subscribe to the specified event(s).
```json
{
  "type": "command",
  "data": {
    "command": "subscribe",
    "correlation_id": 42,
    "arguments": {
      "action": [ "<action(s)>" ],
      "resource": {
        "type": "<resource type>",
        "name": "<resource name>"
      }
    }
  }
}
```

The response indicates if the subscription succeeded or not, typical [error responses](#error-codes) are 1000 (Unknown resource type), 1001 (Unknown resource name), and 1002 (Unknown action).

### Unsubscribe from resource event

Send the following command to unsubscribe to the specified event(s).
```json
{
  "type": "command",
  "data": {
    "command": "unsubscribe",
    "correlation_id": 43,
    "arguments": {
      "action": [ "<action(s)>" ],
      "resource": {
        "type": "<resource type>",
        "name": "<resource name>"
      }
    }
  }
}
```

The response indicates if subscribing succeeded or not, typical [error responses](#error-codes) are 1000 (Unknown resource type), 1001 (Unknown resource name), and 1002 (Unknown action).

## Channels

RTC module supports event channels that allow applications to publish custom events/payloads.
Technically they are similar to events the only difference you have to subscribe to the `published` action:

```json
{
  "type": "command",
  "data": {
    "command": "subscribe",
    "correlation_id": "some unique value",
    "arguments": {
      "action": [ "published" ],
      "resource": {
        "type": "channel",
        "name": "example"
      }
    }
  }
}
```

### Publishing messages

1. Use WebApp to create a channel or check the [API documentation](../mgm/README.md) to learn more about management operations on channels.

2. Create a user/API key and policies with "publish" permissions on created channel(s).

3. Send `publish` command to publish message to the specified channel(s):

```json
{
  "type": "command",
  "data": {
    "command": "publish",
    "correlation_id": ["it", "can", "be", "any", "valid", "JSON", "value"],
    "arguments": {
      "channel": "test",
      "data": {
        "foo": 42
      }
    }
  }
}
```

Command data:

FIELD          | TYPE   | DESCRIPTION                                                        | EXAMPLE
---------------|--------|--------------------------------------------------------------------|----------------
command        | String | command to be executed on the server                               | `publish`
correlation_id | Any    | corellation id (to associate the response with particular request) | `42` / `foo-123`
arguments      | Object | list of arguments for the command                                  |

Arguments:

ARGUMENT     | TYPE   | DESCRIPTION         | EXAMPLE
-------------|--------|---------------------|----------------
channel      | String | name of the channel | `test`
data         | Any    | command payload     | `{"foo":42}`

As usual every `publish` command response will be sent back to check if the message was published or not.

### Receiving data from the channel

When something is published to the channel, the message is forwarded to every subscriber:

```json
{
  "type": "event",
  "data": {
    "action": "publish",
    "resource": {
      "type": "channel",
      "name": "example",
    },
    "modifier": {
      "id": "apk:4c192dec-05ca-4152-91f5-3168bc1486d7",
    },
    "timestamp": "2019-09-06T15:53:00",
    "data": {
      "foo": "bar"
    }
  }
}
```
