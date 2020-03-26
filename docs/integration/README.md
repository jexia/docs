# Integration
The main purpose of this module is to provide the possibility to set up the integration between Jexia and other platforms. 
For example, I want to send some emails via my SMTP server, make a HTTP call or send a push notification. To achieve this, I need to set up a bridge to another service. With integration, this can be done in one place with ease.

![Integration setup](./integration.png)

1. Integration name - descriptive name, will be visible in the list of integrations.
2. Integration type - type of integration like SMTP, HTTP, etc. As for now, only SMTP is supported.
3. TLS - checkbox to specify if we need a TLS handshake for the SMTP gateway. If not, SSL will be used instead.
4. SMTP server - The SMTP server address.
5. SMTP PORT - The SMTP server port. In most cases, `587` is for a TLS connection, `486` - for SSL. You can apply desired ports based on your set up.
6. SMTP username - user name to connect to SMTP server.
7. SMTP password - password to connect to SMTP server. We are hashing the password and will not be able to revert it. You need to enter this again during the editing process. 
8. Replay To - email which your client will see while getting an email in a replay to option.

As you can see there is a button `Test integration`, it allows you to test your credentials and will send a test email to your Jexia account email, so you can be sure that all setup is good and the integration is working as expected.


