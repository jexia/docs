# Integration
The main purpose of this module is to provide the possibility of setting up integrations between Jexia and other platforms or services. 
For example, if you want to send emails via a SMTP server, make a HTTP call or send a push notification. To achieve this, you will need to set up a bridge to another service. With integrations, this can be done in one place with ease.

![Integration setup](./integration.png)

1. **Integration name** - The descriptive name. This will be visible in the list of integrations.
2. **Integration type** - The type of integration, such as: SMTP or HTTP etc. As for now, only SMTP is supported.
3. **TLS** - A checkbox to specify if we need a TLS handshake for the SMTP gateway. If not, SSL will be used instead.
4. **SMTP server** - The SMTP server address.
5. **SMTP PORT** - The SMTP server port. In most cases, `587` is for a TLS connection, `486` is for SSL. You can apply desired ports based on your set up.
6. **SMTP username** - The username required to connect to the SMTP server.
7. **SMTP password** - The password required to connect to the SMTP server. We hash the password and will not be able to revert it. You will need to enter this again during any editing processes. 
8. **Replay To** - The email of which your client will as the reply option.

As you can see there is a **Test integration** button, this allows you to test your credentials and will send a test email to your Jexia account email, this will ensure that the integration is working as expected.


