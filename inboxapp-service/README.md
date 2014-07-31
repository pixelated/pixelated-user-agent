SMail Back
==========

This is the backend for SMail. The primary purpose of this is to integrate well with LEAP and provide all the capabilities necessary for the frontend to work well.

The aim is to support these resources/endpoints:

```
GET    /mails
DELETE /mails
POST   /mails
PUT    /mails
POST   /mails/read

GET    /mail/:id
DELETE /mail/:id
POST   /mail/:id/star
POST   /mail/:id/unstar
POST   /mail/:id/replied
POST   /mail/:id/unreplied
POST   /mail/:id/read
POST   /mail/:id/unread
GET    /mail/:id/tags
POST   /mail/:id/tags

GET    /draft_reply_for/:id

GET    /contacts
GET    /contact/:id

GET    /stats

GET    /tags
POST   /tags
```

The implementation of SMail Back will be in Python, in order to better work together with LEAP. Another goal of SMail Back will be to run well on all major client platforms. Finally, there will be a lot of support for search and indexing, and also for encryption and signing. However, we want to push most of these features back to LEAP so that Bitmask can leverage them as well.

We will likely start by implementing a simple SMTP and IMAP implementation in order to make it easier to test - and we will then gradually implement a LEAP backend that provides the production functionality we are aiming for.

Instructions
===

To run the app we suggest you using python + virtualenv. If you are developing in with TW Brazil you can fetch a vagrant base box from secret.local:~/smail-back-precise64.box.

Inboxapp as provider
---
You will need to install inboxapp in your machine and sync an account to it. Follow instructions from inboxapp [instalation](https://www.inboxapp.com/docs/gettingstarted#installation) guide. Once you have an account sync you can configure it in config/inboxapp.cfg and you should be good to go.
 

