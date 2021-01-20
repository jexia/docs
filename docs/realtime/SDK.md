## WebSocket API with JavaScript SDK
Below you can find an overview of how to use channels with our JS SDK. 

``` js
import { jexiaClient, realTime } from "jexia-sdk-js";  
  
const rtm = realTime();  
// Initiate Jexia Client 
jexiaClient().init({  
  projectID: "your-project-id",  
  key: "your-api-key",    
  secret: "your-api-secret",
  zone: "PROJECT_ZONE",
}, rtm);  

// Initiate a channel
const channel = rtm.channel("my_channel");

// Subscribe to listen messages
channel.subscribe(
  message => {
    console.log(message); // we've got a message from the channel
  },
  error => {
    console.log(error); // Subscription Error: (1001): resource "my_channel" is unavailable
  },
  () => { // complete
    // connection to the channel has been closed
  }
); 
// Send message to channel 
channel.publish({
  product: "apple",
  amount: 42
});  
// or
channel.publish("Some text string here...");  

// Get channel Log
channel
.getLog(field => field("sender_id").isEqualTo(user.id))  // Same filters as in Dataset
.subscribe(
  messages => {
    console.log(messages); 
  },
  error => {
    console.log(error); // Subscription Error: (2): none of the given actions ["read"] for this resource are allowed
  }
```