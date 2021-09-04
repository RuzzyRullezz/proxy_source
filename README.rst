PROXY SOURCE
==================

Postgres configure
------------------
**psql commands**:

.. code-block:: sql::

   CREATE ROLE proxy_source WITH PASSWORD 'proxy_source' LOGIN;
   CREATE DATABASE proxy_source WITH OWNER proxy_source;

