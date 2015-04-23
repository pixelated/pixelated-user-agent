Pixelated User Agent Maintenance
================================

## Overview

The command line tool pixelated-maintenace allows you to run some common tasks, mostly related to soledad.

```
usage: pixelated-maintenance [-h] [--debug] [--dispatcher file]
                             [--dispatcher-stdin] [-c <configfile>]
                             [--home HOME] [-lc <leap-provider.crt>]
                             [-lf <leap provider certificate fingerprint>]
                             {reset,load-mails,dump-soledad,sync} ...

pixelated maintenance

positional arguments:
  {reset,load-mails,dump-soledad,sync}
                        commands
    reset               reset account command
    load-mails          load mails into account
    dump-soledad        dump the soledad database
    sync                sync the soledad database

optional arguments:
  -h, --help            show this help message and exit
  --debug               DEBUG mode.
  --dispatcher file     run in organization mode, the credentials will be read
                        from specified file
  --dispatcher-stdin    run in organization mode, the credentials will be read
                        from stdin
  -c <configfile>, --config <configfile>
                        use specified file for credentials (for test purposes
                        only)
  --home HOME           The folder where the user agent stores its data.
                        Defaults to ~/.leap
  -lc <leap-provider.crt>, --leap-provider-cert <leap-provider.crt>
                        use specified file for LEAP provider cert authority
                        certificate (url https://<LEAP-provider-
                        domain>/ca.crt)
  -lf <leap provider certificate fingerprint>, --leap-provider-cert-fingerprint <leap provider certificate fingerprint>
                        use specified fingerprint to validate connection with
                        LEAP provider
```

The commands you can run are:

* reset - Use this to remove all mails from your account. Existing encryption keys like your GnuPG key is not affected
* sync - Sync your soledad database
* load-mails - Loads existing mails into your account
* dump-soledad- Get a soledad database dump. Mostly for debugging use cases

Like with other such tools, to get detailed help for a single command, call it with the --help option.

```
$ pixelated-maintenace load-mails --help
usage: pixelated-maintenance load-mails [-h] file [file ...]

positional arguments:
  file        file(s) with mail data

  optional arguments:
    -h, --help  show this help message and exit
```

## How to load mails into an account:

With the load-mails command you are able to import existing mails into your account. The mails have to be in the **mbox** format, i.e. the need a 'From' line in the first line:
```
From someone@somedomain.tld
Subject: This is a testmail
To: else@somedomain.tld
X-TW-Pixelated-Tags: nite, macro, trash

This is a test mail
```

*Preparation* 

Steps you might want to consider before importing mails into an account:

* You have started the pixelated-user-agent at least once for this account
* No pixelated-user-agent is currently running

To import this mail into your soledad database, put it into an empty folder. Let's assume its called just 'example_mails'.

```
$ pixelated-maintenace load-mails /path/to/example_mails
```

---
## Troubleshooting

### load-mails fails with soledad sync errors

This happens sometimes, kill the pixelated-maintenance process and start it again, but this time with the *sync* command. **Don't run the load-mails again as you will end up with double the mails**.

