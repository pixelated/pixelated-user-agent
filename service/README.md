Pixelated User Agent Service
============================

This is the service for the Pixelated User Agent. The primary purpose of this is to integrate well with the Pixelated Provider and provide all the capabilities necessary for the UI to work well.

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

The implementation of the User Agent Service will be in Python, in order to better work together with LEAP. Another goal of the User Agent Service will be to run well on all major client platforms. Finally, there will be a lot of support for search and indexing, and also for encryption and signing. However, we want to push most of these features back to LEAP so that Bitmask can leverage them as well.
