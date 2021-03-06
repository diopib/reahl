.. Copyright 2013-2016 Reahl Software Services (Pty) Ltd. All rights reserved.
 
Persistence
===========

.. sidebar:: Behind the scenes (or, not so much *behind* this time)

   Persistence is done directly using `SqlAlchemy
   <http://www.sqlalchemy.org/>`_. If you are not
   familiar with this tool, please refer to its
   documentation.

For those programmers who have an object oriented model (which is
recommended, but not strictly necessary to use Reahl), we provide glue
to the object relational mapping tools provided by `SqlAlchemy
<http://www.sqlalchemy.org/>`_.

Reahl allows you :doc:`to build and distribute parts of your program
as reusable components<enduserfunctionality>` that do not contain knowledge
about the web application such components will be used in. Reahl 
extends existing database migration tools to make it possible to write
database migrations per component regardless of where that component
will be used. (:ref:`See the tutorial for more on this topic
<database-schema-evolution>`.)

Here is an example showing the use of SqlAlchemy. Reahl merely
provides versions of SqlAlchemy's `Session`, `Base` and `metadata`
objects for use with Reahl applications. Further use is just normal
SqlAlchemy.

Our example first comes up with only a (somewhat prettied up) form
asking the user to leave a comment:

   .. figure:: ../_build/screenshots/persistence1.png
      :align: center
      :alt: A screenshot of a form with input for a user's email.

When the user clicks on submit, the new comment is persisted in
the database. When the page is refreshed, the form is still rendered,
but a list of all the comments in the database is shown below it:

   .. figure:: ../_build/screenshots/persistence2.png
      :align: center
      :alt: A screenshot of a form with input for a user's email, and also a list of previously entered email addresses.

In the example's source code (below), the Comment class is persisted via SqlAlchemy's declarative:


.. literalinclude:: ../../reahl/doc/examples/features/persistence/persistence.py
