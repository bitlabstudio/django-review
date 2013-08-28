Django Review
============

A reusable Django app that lets users write reviews for any model

Installation
------------

To get the latest stable release from PyPi

.. code-block:: bash

    $ pip install django-review

To get the latest commit from GitHub

.. code-block:: bash

    $ pip install -e git+git://github.com/bitmazk/django-review.git#egg=review

TODO: Describe further installation steps (edit / remove the examples below):

Add ``review`` to your ``INSTALLED_APPS``

.. code-block:: python

    INSTALLED_APPS = (
        ...,
        'review',
    )

Add the ``review`` URLs to your ``urls.py``

.. code-block:: python

    urlpatterns = patterns('',
        ...
        url(r'^review/', include('review.urls')),
    )

Don't forget to migrate your database

.. code-block:: bash

    ./manage.py migrate review


Usage
-----

TODO: Describe usage or point to docs.


Settings
--------

Default behaviour:

* Users can vote form 0 to 5
* Only authenticated users can post a review
* Users can post multiple reviews on one object

If you want to change this behaviour, or if you like to add some more
permission checks, read on.

REVIEW_VOTE_CHOICES
+++++++++++++++++++

If you want other voting choices than 0-5, you can define a new tuple, like:

.. code-block:: python

    REVIEW_VOTE_CHOICES = (
        ('1', 'bad'),
        ('2', 'average'),
        ('3', 'excellent'),
    )


REVIEW_ALLOW_ANONYMOUS
++++++++++++++++++++++

Allows anonymous review postings, if set to ``True``.


REVIEW_AVOID_MULTIPLE_REVIEWS
+++++++++++++++++++++++++++++

Avoids multiple reviews by one user, if set to ``True``.


REVIEW_PERMISSION_FUNCTION
++++++++++++++++++++++++++

Custom function to check the user's permission. Use a function and note that
the user is the only parameter.

.. code-block:: python

    REVIEW_PERMISSION_FUNCTION = lambda u: u.get_profile().has_permission()


Contribute
----------

If you want to contribute to this project, please perform the following steps

.. code-block:: bash

    # Fork this repository
    # Clone your fork
    $ mkvirtualenv -p python2.7 django-review
    $ python setup.py install
    $ pip install -r dev_requirements.txt

    $ git co -b feature_branch master
    # Implement your feature and tests
    $ git add . && git commit
    $ git push -u origin feature_branch
    # Send us a pull request for your feature branch
