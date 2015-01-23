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

Write a test mail to bob@try.pixelated-project.org. You can find bob's credentials here: [https://try.pixelated-project.org:8080/](https://try.pixelated-project.org:8080/)

After that take some minutes to familiarize yourself with the user interface.

## Show me the code

To get a better feeling for the code base, let's try some smaller changes. Let's assume that we'd like to change the way subjects are displayed in the mail list.
First we want to find the location in the code that renders the subjects. 
Start your favorite text editor and open pixelated-user-agent/web-ui/app/js/mail_list/ui/mail_items/mail_item.js. Find the method named render. This seems to be the right location. To verify our assumption, let's change the html content. 

```javascript
  this.render = function () {
      this.attr.tagsForListView = _.without(this.attr.tags, this.attr.tag);
      var mailItemHtml = templates.mails[this.attr.templateType](this.attr); // <-- here
      this.$node.html(mailItemHtml);                                         // <-- and here
      this.$node.addClass(this.attr.statuses);
      if(this.attr.selected) { this.doSelect(); }
      this.on(this.$node.find('a'), 'click', this.triggerOpenMail);
    };
```

Set the mailItemHtml to a fixed string like "found the subject location". The render method should then look like this:
 
```javascript
  this.render = function () {
      this.attr.tagsForListView = _.without(this.attr.tags, this.attr.tag);
      // start of our change
      var mailItemHtml = "<span>found the subject location</span>";
      // end of our change
      this.$node.html(mailItemHtml);
      this.$node.addClass(this.attr.statuses);
      if(this.attr.selected) { this.doSelect(); }
      this.on(this.$node.find('a'), 'click', this.triggerOpenMail);
    };
```

Go back to your browser and refresh the page. You should immediatly see that your change is active.

Now that's nice. Congratulations. But what we really want is to change the way the subjects are displayed on every mail in the list, not to substitute the entire thing by a string.
The template line we removed seems to produce some more html. But where to find it? As it says **template** perhaps the file **views/templates.js** might be start.
The code snipped mentions templates.mails and in the mails declaration we see references to four files. The single.hbs is the one we are looking for, so let's open it.

```html
<span>
    <input type="checkbox" {{#if isChecked }}checked="true"{{/if}} />
</span>
<span>
    <a href="/#/{{ tag }}/mail/{{ ident }}">
        <span class="received-date">{{ header.formattedDate }}
          {{#if attachments}}
            <div class="attachment-indicator">
              <i class="fa fa-paperclip"></i>
            </div>
          {{/if}}
        </span>
        <div class="from">{{#if header.from }}{{ header.from }}{{else}}{{t "you"}}{{/if}}</div>
        <div class="subject-and-tags">
          {{ header.subject }}
        </div>
        <div class="subject-and-tags">
          <ul class="tags">
            {{#each tagsForListView }}
                <li class="tag" data-tag="{{this}}">{{ this }}</li>
            {{/each }}
          </ul>
        </div>
    </a>
</span>
```

Lets undo the changes in mail_item.js and instead add a span around the header.subject and set the class to 'search-highlight'. It should look like this:

```
...
        <div class="subject-and-tags">
          <span class='search-highlight'>{{ header.subject }}</span>
        </div>
...
```

Uuuups - nothing happened?? Well that is because we have to build the resources (that includes .hbs files) in order to make them available. To do so open another shell and go to the pixelated-user-agent folder and call: 

```shell
vagrant ssh hackday

cd web-ui
./go build
```

Now refresh your browser again to see the changes in effect.

Finally we would like to change the color of the highlighting. The pixleated user agent uses [SASS](http://sass-lang.com/) to make handling styles a little bit easier.
You can find the style sheets in web-ui/app/scss/. The search-hightlight is defined in styles.scss:

```scss
.search-highlight {
  background-color: $search-highlight;
}
```

It references a color variable defined in \_colors.scss 

```scss
 $search-highlight: #FFEF29;
```

Change the color value to something else. Then run the ./go build command again and refresh the page. 

## Next steps

The pixelated user agent is based on the reactive [FlightJS] (https://github.com/flightjs) framework and uses events as the primary way of control flow.

## The life of mail.

How does that list of mails get populated? We only had look onto the JavaScript side of things, there is also the Python side for the service. When we say service we mean a python application that delivers not only the resources for the web application but also provides a REST api to access and send mails.

To give you a brief overview lets follow an email through the service.

* Some javascript calls the MailsResource in service/pixelated/resources/mails_resource.py 
* The render_GET method asks the search engine for a list of matching mail ids. These mails are then request from the mail service.
* The mail service asks the soledad querier.
* The soledad querier fetches the mails from the soledad backend

