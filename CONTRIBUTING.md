# How to contribute

Here's the brief:

* We welcome contributions of all kinds, including but not limited to features, bug fixes, quality assurance, documentation, security review or asking questions
* Pull requests are based off, integrated into & rebased against master
* Write automated tests, ideally using TDD. CI needs to be green in order to merge.
* Feel free to review the repository's issues for ideas on what to work on
* Contact us for questions & suggestions:
  * Email: [pixelated-team@thoughtworks.com](mailto:pixelated-team@thoughtworks.com)


This document gives hints and outlines the steps to make your contribution to Pixelated as smooth as possible. You're not required to read this before getting started. We're giving suggestions to make sure you're having a good experience and can make best use of the time you're contributing to our project.

## Contributions steps

This is the lifecycle of a contribution. See our [README](README.md) for details on how to set up your development environment.

We follow a simplified fork + pull request workflow:

* To start, fork this repository and create a branch that's based off the latest commit in the `master` branch
* Implement the change
* Send a pull request against the master branch. Please make sure the automated tests are passing, as indicated by GitHub on the pull requests.
* Please keep your feature branch updated. Rebase your branch against upstream changes on the master branch, resolve any conflicts and make sure the tests are staying green.
* Your pull request will be reviewed and merged

### Getting acquainted with the code

If you're not sure how to start development, check out [our short guide](https://github.com/pixelated/pixelated-user-agent/wiki/Starting-Development) on how to start getting to know the code.

### What to work on

Our Github provides an overview of issues that are ready to play. If you're just getting familiar with Pixelated, see the [issues labeled 'Volunteer Task'](https://github.com/pixelated/pixelated-user-agent/labels/Volunteer%20task).

Generally, all issues that have no user assigned are awaiting work and free to play.

### Guidelines

When implementing your change, please follow this advice:

* Your change should be described in an issue, or latest in the pull request description.
* For bugs, please describe, in an issue or pull request:
  1. Steps to reproduce the behavior
  2. Expected behavior
  3. Actual behavior. Please also include as much meta-information as reasonable, e.g. time & date, software version etc.
* Pull requests need not to be finished work only; you can also submit changes in consecutive Pull Requests as long as CI stays green. Also, please send a PR with the intention of discussion & feedback. Please mark those Pull Requests appropriately.
* We review your pull request. This review is prioritised and done as part of our priotisation. During this time, we ask you to keep it up to date by frequently rebasing against master

### Review Criteria

When reviewing your contribution, we apply the following criteria:

* Test must be green. This usually includes an automatic check of the style guide using e.g. pep8 or jshint. All tests should be executed locally before you push, as outlined in the [wiki](https://github.com/pixelated/pixelated-user-agent/wiki/Running-Tests), as well as on CI.
* Your change should be in line with Pixelated's direction. Chances that it is are good if, in descending priority:
  * It is described by an existing issue
  * You've fixed a bug for which no issue existed yet, but described it in the pull request as explained in the section *Guidelines*
  * You've implemented a feature for which no issue existed yet. While we don't require up-front consensus, we strongly encourage you to describe feature suggestions in issues to get feedback before you spent significant time on implementation.
* We won't tolerate abusive, exploitative or harassing behavior in every context of our project and refuse collaboration with any individual who exposes such behavior.

## Types of contributions

Pixelated evolves upon the source code it's made of. This evolution is fueled by a variety of tasks; some of which require developing source code, some of which do not.

Contributions we appreciate:

* Features: New functionality is described in issues in the form of a user story to capture the end-user benefit.
* Bug fixes: Things go wrong from time to time.
* Quality Assurance: While every software change should be covered by automated tests, there are certain types of errors that are best spotted by a human.
* Documentation: Feedback & improvements of our guides & tutorial copywritings.
* Security review
* Design: We have some issues which needs prototypes. You can contribute with sketches, wireframes, etc. See the [issues labeled 'Needs Prototype'](https://github.com/pixelated/pixelated-user-agent/labels/Needs%20Prototype).
* Translations

## I think I might be able to hack together a quick-and-dirty lo-fi solution for the issue I’m working with… what do I do?

Do it the easy way first, and submit a pull request as a “work in progress” as soon as you have a quick-and-dirty solution (or even an unfinished solution) — that means you can get feedback from the other developers about whether you’re heading in the right direction sooner rather than later. Include “WIP” (work in progress) in the description of your pull request and ask for review, or feedback on anything specific.

## Translating UI

Anyone can contribute with Pixelated translating our user interface and making it accessible for more people. To learn how to contribute to Pixelated's translations, see the [Translations page](https://github.com/pixelated/pixelated-user-agent/wiki/Translating-Pixelated).
