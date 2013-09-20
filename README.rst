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

The only step you'll have to take is to link to the review views. For example,
you created a ``Book`` model, which should be reviewed by users.

Create a button and add some markup like:

.. code-block:: html

    <a href="{% url "review_create" content_type='book' object_id=book.pk %}">{% trans "Review this book" %}</a>


Settings
--------

Default behaviour:

* Users can rate form 0 to 5
* Only authenticated users can post a review
* Users can post multiple reviews on one object
* Users can always update their posted reviews

If you want to change this behaviour, or if you like to add some more
permission checks, read on.

REVIEW_RATING_CHOICES
+++++++++++++++++++++

If you want other rating choices than 0-5, you can define a new tuple, like:

.. code-block:: python

    REVIEW_RATING_CHOICES = (
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

    REVIEW_PERMISSION_FUNCTION = lambda u, item: u.get_profile().has_permission(item)


REVIEW_UPDATE_PERIOD
++++++++++++++++++++

You can limit the period, in which a user is able to update old reviews.
Make sure to use minutes, e.g. 2880 for 48 hours.


REVIEW_CUSTOM_FORM
++++++++++++++++++

You can create your own review form (e.g. if you want to make use of the review
extra info). Just name it.

.. code-block:: python

    REVIEW_CUSTOM_FORM = 'myapp.forms.MyCustomReviewForm'

Take a look at the included test app to get an example.


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
