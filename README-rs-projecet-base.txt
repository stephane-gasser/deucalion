Quickstart
==========

$ git clone git@bitbucket.org:dmarclay/rs-project-base.git NewProjectName
$ cd NewProjectName
$ python bootstrap.py
(interact, y, yes, ...)
$ source env/bin/activate
(env) $ python manage.py runserver ## it works


Snapshot management
===================

We use snapshots of user content (typically cms pages and uploaded files) to synchronize accross production, preproduction and developpers works. Those are archives of media/ directory and of fixtures of selected db tables.

Typical workflow
----------------

1) Developper A who has entered a basic sitemap in the CMS dumps it and add it to the repository

$ source env/bin/activate
(env) $ sh make_snapshot.sh
(...)
(env) $ git add snapshot-YYMMDD.tgz ## freshly created archive
(env) $ git commit -m 'New content snapshot' 


2) Developper B want to update his local database with the new snapshot

$ source env/bin/activate
(env) $ git pull
(env) $ tar xvfz snapshot-YYMMDD.tgz                  # uncompress the archive
(env) $ python manage.py loaddata content-YYMMDD.json # load the fixtures

Notes:
* there might be several fixtures in the snapshot (e.g. secondary app, such as shop products)
* it is sometimes needed to reset the database before loading fixtures if the db has changed a lot (e.g. cms pages have been deleted ; deleted content cannot be marked in fixtures)
* if a new app is created with cms plugins, make_snapshot.sh must be updated accordingly

Branches
========

* base-django1.4 (aka master) - base raw project
* base-django1.4-cms2.3       - base django cms project

Other branches are kept as historical material.


Project layout
==============

* [root]
** [common apps here]
** main
*** settings.py      ## global default settings
*** urls.py          ## main url file
*** views.py         ## misc views
*** static           ## global assets
*** templates        ## project templates
*** [custom apps here]
** --------------- non versioned ------------
** local_settings.py ## local config
** static/           ## collected assets
** media/            ## user content
** django.log
