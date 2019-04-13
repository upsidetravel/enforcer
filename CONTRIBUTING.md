# Contributing Guide

You will need:

- Python 3.7
- Sign the [CLA](CLA.md)

## Getting started

Fork the project

To get your development environment setup, run:

```sh
pip install -e .
pip install -r requirements.txt
```

This will install the repo version of enforcer and then install the development
dependencies. Once that has completed, you can start developing.

## Good Bug Reports

Please be aware of the following things when filing bug reports:

1. Avoid raising duplicate issues. *Please* use the GitHub issue search feature
   to check whether your bug report or feature request has been mentioned in
   the past. Duplicate bug reports and feature requests are a huge maintenance
   burden on the limited resources of the project. If it is clear from your
   report that you would have struggled to find the original, that's ok, but
   if searching for a selection of words in your issue title would have found
   the duplicate then the issue will likely be closed extremely abruptly.
2. When filing bug reports about exceptions or tracebacks, please include the
   *complete* traceback. Partial tracebacks, or just the exception text, are
   not helpful. Issues that do not contain complete tracebacks may be closed
   without warning.
3. Make sure you provide a suitable amount of information to work with. This
   means you should provide:

   - Guidance on **how to reproduce the issue**. Ideally, this should be a
     *small* code sample that can be run immediately by the maintainers.
     Failing that, let us know what you're doing, how often it happens, what
     environment you're using, etc. Be thorough: it prevents us needing to ask
     further questions.
   - Tell us **what you expected to happen**. When we run your example code,
     what are we expecting to happen? What does "success" look like for your
     code?
   - Tell us **what actually happens**. It's not helpful for you to say "it
     doesn't work" or "it fails". Tell us *how* it fails: do you get an
     exception? A hang? The packages installed seem incorrect?
     How was the actual result different from your expected result?
   - Tell us **what version of Enforcer you're using**, and
     **how you installed it**. Different versions of Enforcer behave
     differently and have different bugs.
     
   If you do not provide all of these things, it will take us much longer to
   fix your problem. If we ask you to clarify these and you never respond, we
   will close your issue without fixing it.
        
## Opening Pull Requests

1. Please Provide a thoughtful commit message and push your changes to your fork using
   `git push origin master` (assuming your forked project is using `origin` for
   the remote name and you are on the `master` branch).

2. Open a Pull Request on GitHub with a description of your changes.

## Testing

All PRs, that change code functionality, are required to have accompanying tests.

# Upside CLA
We require all contributors to sign the [Upside CLA](CLA.md).

In simple terms, the CLA affirms that the work you're contributing is original, that you grant Upside permission to use that work (including license to any patents necessary), and that Upside may relicense your work for our commercial products if necessary. Note that this description is a summary and the specific legal terms should be read directly in the CLA.

The CLA does not change the terms of the standard open source license used by our software. You are still free to use our projects within your own projects or businesses, republish modified source, and more. Please reference the appropriate license of this project to learn more.

To sign the CLA, open a pull request as usual. If you haven't signed the CLA yet. We cannot merge any pull request until the CLA is signed. You only need to sign the CLA once.
