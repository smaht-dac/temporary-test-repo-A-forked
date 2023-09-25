=======
submitr
=======

----------
Change Log
----------

0.3.3
=====

* Make the heading for "Basic Setup" to be "Installing Prerequisites",
  since that naming is more standard.
* Rename the "Getting Started" option to more standard "Using submitr",
  since getting started is ambiguous between installation and usage.
* Add an "Implementation of submitr" heading on the implementation part
  to make it clear to end users they don't need to look at this.
* Reorganize to make experimental ``rclone`` support *not* be the first thing
  that you see in this doc,
  since non-experimental stuff needs to be first.
* Make ``rclone`` section not pretend to tell you about ``awscli``
  in the heading, since the actual text barely mentions ``awscli``.
* Light editing on the opening of the section about ``rclone`` to make
  the motivational part clearer.


0.3.2
=====

* Fix auto-publish on pushing a tag.
* Disabled ``scripts/publish`` since we're using functionality from ``dcicutils.scripts`` now.
* Adjusted headings to present with better indentation and better recursive header presentation.


0.3.1
=====

* Auto-submit to readthedocs on any non-beta version tag push (v* except v*b*).
* Fix a bug in readthedocs submission where we were using branches=master and getting an error saying
  ``{"detail":"Parameter \"ref\" is required"}``. ChatGPT thinks this is because we wanted a curl
  parameter of ``-d "ref=master"`` rather than ``-d "branches=master"`` like we had.
* Remove spurious "Module Contents" headings in three places.
  We do not put code in ``__init__.py`` so these sections would always be empty (and confusing).


0.3.0
=====

* Add a pretty logo
* Warn about not yet being still experimental.
* Better badges.


0.2.1
=====

* Some commands will now default the app to 'smaht' better.
* In general, a lot of rewriting of 'cgap' references to
  be either SMaHT or to reference a centrally defined default.


0.2.0
=====

* Fix a bug in the project-association in Sphinx config file.
* Add a warning about preliminary nature in README.rst
* Enable auto-publish to readthedocs on checkin to master.
* Enable auto-publish to pypi on tag.

0.1.1
=====

* Additional tweaks mostly related to readthedocs.


0.1.0
=====

* Initial changes to give submitr a bit of a different look that SubmitCGAP.

0.0.0
=====

* Forked from SubmitCGAP 4.1.0.

