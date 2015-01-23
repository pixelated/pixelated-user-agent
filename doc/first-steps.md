Pixelated User Agent First Steps
================================

## First things first - get a test account

In order to run the user agent, you will need an account at a Leap provider supporting mail. To do so sign up at [try.pixelated-project.org](https://try.pixelated-project.org/signup)

Notice: This account is only for test purposes and does not allow to send emails to external recipients.


## Starting the agent for the first time
---

The first thing you need to do is to clone the pixelated-user-agent github repo to your preferred location:

```
git clone https://github.com/pixelated-project/pixelated-user-agent.git
```

Before you can run the user agent you need to download and add the hackday vagrant box:

```
wget http://tbd.tld/hackday-pixelated-user-agent.box
vagrant box add hackday-pixelated-user-agent hackday-pixelated-user-agent.box
rm hackday-pixelated-user-agent.box
```

Now let's run the user agent for the first time

```
cd pixelated-user-agent
vagrant up hackday
vagrant ssh hackday

pixelated-user-agent --host 0.0.0.0

> 2015-01-23 11:18:07+0100 [-] Log opened.
> 2015-01-23 11:18:07+0100 [-] Which provider do you want to connect to:
try.pixelated-project.org
> 2015-01-23 11:18:52+0100 [-] What's your username registered on the provider:
username
> Type your password:
*******************
```

Now you can open the user agent in a browser: [http://localhost:3333/](http://localhost:3333/)

## Write your first mail

Write a test mail to bob@try.pixelated-project.org. You can find bob credentials here: [https://try.pixelated-project.org:8080/](https://try.pixelated-project.org:8080/)

After that take some minutes to familiarize yourself with the user interface.

## Show me the code

To get a better feeling for the code base, let's try some smaller changes. Let's assume that we'd like to change the way subjects are displayed in the mail list.
First we want to find the location in the code that renders the subjects. 
Start your favorite text editor and open pixelated-user-agent/web-ui/app/js/mail_list/ui/mail_items/mail_item.js. Find the method named render. This seems to be the right location. To verify our assumption, let's change the html content. 

```javascript
  this.render = function () {
      this.attr.tagsForListView = _.without(this.attr.tags, this.attr.tag);
      var mailItemHtml = templates.mails[this.attr.templateType](this.attr);
      this.$node.html(mailItemHtml);
      this.$node.addClass(this.attr.statuses);
      if(this.attr.selected) { this.doSelect(); }
      this.on(this.$node.find('a'), 'click', this.triggerOpenMail);
    };
```

Set the mailItemHtml to a fixed string like "found the subject location". The render method should then look like this:
 
```javascript
  this.render = function () {
      this.attr.tagsForListView = _.without(this.attr.tags, this.attr.tag);
      var mailItemHtml = "<span>found the subject location</span>";
      this.$node.html(mailItemHtml);
      this.$node.addClass(this.attr.statuses);
      if(this.attr.selected) { this.doSelect(); }
      this.on(this.$node.find('a'), 'click', this.triggerOpenMail);
    };
```

Go back to your browser and refresh the page. You should immediatly see that your change is active.

Now that's nice. Congratulations. But what we really want is to change the way the subjects are displayed on every mail in the list, not to substitute the entire thing by a string.



 

