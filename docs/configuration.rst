
.. _config_maintenance:

**********************************
Configuration and Site Maintenance
**********************************

The HappyFace 3 configuration is very flexible and can be bent to suit almost all needs in deployment and usage. In contrast, its predecessor HappyFace 2 was limited to a mildly confusing configuration style.

Core Configuration
=======================
Several aspects of HappyFace can be tuned by configuration, but usually you don't need extensive customisation, therefore meaningful defaults are required. To accomplish this, the configuration of the core takes place in two stages and places.

**defaultconfig/**
    As the name suggests, HappyFace evaluates this directory first, gathering the configuration from all files ending in *\*.cfg* in alphabetical order. In a fresh checkout, there is only one such file, it contains all sections and options that are interpreted by HappyFace with their defaults. If you want to alter anything, copy&paste from there into a user configuration is a good start.

    You should not alter the configuration in this directory since it is under revision control and might be altered in future! The only thing you are supposed to do with this directory is adding a new, unrevisioned file like this

    .. code-block:: ini

        [paths]
        local_happyface_cfg_dir = /desired/path/to/configuration

    This will change the path of the next configuration stage, where your user configuration is saved. You might want this if you wish to move configuration to places like */etc*, but is not required for a default setup.

    .. note:: For the changes to be applied, make sure the name of the additional file is alphabetically after *happyface.cfg*!

**config/**
    As stated in the previous section, the place of this directory can be changed, by default it is right inside the HappyFace directory.

    Again, all files ending in *\*.cfg* are interpeted in alphabetical order, files occuring "later" can override earlier statements. We advice adding files based on sections, or thematically grouped.

    We found it useful in HappyFace2 to place the site configuration in a local Subversion repository, so any developer can easily get a development configuration that is identical to production and reinstalling a site after a potential crash would be easy. Because sensitive information, like database passwords, should not be checked into the repository, they can be easily placed in a separate, unrevisioned file (HappyFace2 was not able to do that!).

Sections
--------

The following is a list of the different sections in the default configuration and their purpose and potential use. For an overview of all config variables, just look at the default configuration files. Everything should be sufficiently commented in-line.

**[auth]**
    Certificate authorization details, described in :ref:`config_certs`

**[database]**
    Everything in this section is passed to the sqlalchemy library. See the `sqlalchemy docs <http://docs.sqlalchemy.org/en/rel_0_7/core/engines.html#sqlalchemy.engine_from_config>`_ for details.

**[downloadService]**
    You can set the timeout for downloads as well as options passed to all wget downloads. This is useful for adding certificates globaly in HappyFace.

**[global]**, **[/]** and everything starting with /
    These are special sections, the values are Python statements, so strings need proper delimiters and lists are supported.

    CherryPy is configured directly from these sections, so if you want to add custom sub-pages to HappyFace (without altering the dispatcher in some way) you can do it here!

**[happyface]**
    If you want to specify a custom order of categories (the default one is "pseudo random"), you can do this here.

**[paths]**
    The longest section, many paths and URLs are specified here. In multi-HappyFace setups you want to change the root URL given by *happyface_url*. If you want to put HappyFace in the URL *http://example.com/HappyFace/gridka*, you set
    
    .. code-block:: ini

        happyface_url = /HappyFace/gridka

    Don't forget to change the path in the *WSGIScriptAlias* as in :ref:`hf-apache-wsgi`.

**[plotgenerator]**
    If you wish to use the HappyFace plot generator, you have to enable it here. Additionally, you can specify the matplotlib backend to use your favourite.


**[template]**
    A few tweaks on the things that are displayed in the web output.

Logfiles
========

The Python `logging <http://docs.python.org/library/logging.html>`_ module is used to generate log files. There are different configuration files possible for acquisition and rendering, by default they are the files ending in *\*.log* in the *defaultconfig/* directory. They are imported by the *logging* module, so please consult the Python documentation about their `format. <http://docs.python.org/library/logging.config.html#configuration-file-format>`_

Modules and Categories
======================

No actual work is done by the HappyCore, all input processing and displaying is implemented in the modules. The required configuration consists of a mechanism to create and configure module instances and then group them into categories for displaying.

Directory Layout
----------------
You can override the locations by changing the **paths** section of the HappyFace configuration, but basically all category configuration is in *config/categories-enabled* and all module configuration in *config/modules-enabled*.

The reason for the *-enabled* suffix is that we originally thought about a Debian-style configuration, where the configuration is in *-available* directories and symbolic links to them in *-enabled* directories. We do not use this at the moment, but if you like to, feel free to do it that way!

As with other configuration directories, all files ending in *.cfg* are parsed in alphabetical order. Because of this, you can split up the different categories and modules over files as you wish. It is possible to have only one massive file for either modules and categories.

We advice you to use one file per category, with the same name as the category, and a similarily named file for the modules, containing all the configuration for all modules in that one category. This supports the original Debian-style configuration idea, but is also a nice grouping, since it is always clear where the module is located. This also makes the maintenance and setup of similar categories rather simple.

Create and Configure Module Instances
-------------------------------------
Each module instance has to be assigned a unique name that, it should only contain alphanumerical characters and underscores. We advice you to use a C-style **underscore_separated_name**, *not* CamelCase or something. The name is used at several places, internally, e.g. as anchor in HTML hyper links.

There are certain config variables common to all modules, as well as a set of variables dependent on the module type.

The easiest way to obtain a skeleton configuration is to use the :ref:`tool-modconfig` tool. Just pass it the module type as a name and you get a skeleton you can easily adapt.

Common module configuration variables are

**module**
    The name of the module class that is used. If it does not correspond to one of the classes in the *modules/*, the world will be sucked into a cosmic singularity.

**name**
    A verbose name for the generated output

**description**
    .. todo:: what is it?

**instruction**
    What should a shifter do if this module fails? Displayed in the module panel on the weboutput.

**type**
    How the module will affect category status calculations. Possible values are
    
    *rated*
        Uses status mechanism and is taken into account when calculating the status of a rated category

    *unrated*
        A status is calculated and displayed for the module, but it is ignored when calculating the category status.

    *plots*
        The status only encodes "got data" and "got no data", taken into account by plots categories.

**weight**
    A numerical value that should be between 0.0 and 1.0 that might be taken into account by some algorithms to calculate the category status.
        

Example
^^^^^^^

As an example, consider we want to configure an instance of the *Plot* module, downloading an image from *https://example.com/file.png*. To obtain a basic configuration, we type the following command on the command line

.. code-block:: bash

    python ./tools.py modconfig Plot

and are rewarded with the following output

.. code-block:: ini

    [INSTANCE_NAME]
    module = Plot
    name = 
    description = 
    instruction = 
    type = rated
    weight = 1.0


    # Enable the mechanism to include two timestamps in the GET part of the URL
    use_start_end_time = False

    # Name of the GET argument for the end timestamp, which is now
    endtime_parameter_name = endtime

    # URL of the image to display
    plot_url = 

    # Name of the GET argument for the starting timestamp
    starttime_parameter_name = starttime

    # How far in the past is the start timestamp (in seconds)
    timerange_seconds = 259200

All we have to do now is replace the section name, change the *type* to *plots*, set a verbose name and insert a valid download command for the *plot_url* variable.

Configuring Categories
----------------------

Each category corresponds to a page on the HappyFace weboutput and is a logical group of HappyFace modules. Modules are specified by creating a uniquely named section in a *\*.cfg* file in the category config directory.

Configuration Variables
^^^^^^^^^^^^^^^^^^^^^^^

The *CATEGORY_ID*, the name of the config file section, is a short version of the name that should only constist of alphanumerical characters and underscores, since it is part of the URL pointing to the web page. The available variables inside the sections are

**name**
	The verbose name of the category

**description**
	A short description of the category that can be displayed somewhere (not used in default templates, at the moment).

**type**
	Choose if category is informational only or has a status value. Set to one of the following

	*plots*
		No status is calculated for this module, since only informational or not parsable data (e.g. images) are contained.

	*rated*
		Calculate a module status with the specified *algorithm* and display the result on the webpage accordingly.

**algorithm**
	The algorithm to calculate the category status with. At the moment, *worst* and *average* are available.

Setting the Order of Categories
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Usually, you want to display the categories in a certain order on the webpage. For this reason, there is the **categories** variable in the *[happyface]* section of the core configuration. Just enter a colon-separated list of categories there and they will be included on the weboutput. If you do not specify **categories**, the categories will appear in arbitrary order.


Updating the Site
=================

Basically, the update flow is as follows

1. update the core

2. update the modules

3. restart the server (e.g. *pkill apache2* as unprivileged HappyFace user with *mod_wsgi* configured accordingly)

4. run *python tools.py dbupdate -f*

.. note::

   You probably get warning messages when using *pkill* to restart your server process(es), because you might try to kill processes from other users. Just ignore those messages.
   
.. note::

   The process name in newer versions of Apache seems to be *apach*, so to restart you need to call *pkill apach*.

Updating the source code of HappyFace or its modules might render the database schema incompatible. In this case, HappyFace tries to throw supportive error messages, giving you hints that schema updates might be neccessary.

To update the database schema, the :ref:`tool-dbupdate` tool is used. To check if updates are neccessary, you can do a dry run. This will list all required changes.

.. code-block:: bash

    python tools.py dbupdate --dry

.. note::

    With some database backends, *dbupdate* falsely claims that altering some columns is neccessary. This is unfortunate, but should not cause any problems. Because of this a run through *dbupdate* might take some time, although basically nothing happens.

    We hope to resolve this issue soon in an updated version of the *dbupdate* tool.

If you see that updates are required, you can either run it interactively, without any command line parameters, or trust that all changes are valid and force the update by

.. code-block:: bash
    
    python tools.py dbupdate --force


.. _config_certs:

Certificate Authorization
=========================

In the section :ref:`apache_cert` we covered the neccessary configuration for the Apache server to support client certificates. We tie in with this and cover the configuration of HappyFace.

HappyFace gets a certificate DN from Apache but still has to decide if access is granted to that particular user. And secondly, we need to tell HappyFace which modules and categories need to be secured, after all.

HappyFace Configuration
-----------------------
After the client certificate is verified (it matches the given root certificates), HappyFace checks if its DN is authorized to access the secured parts of HappyFace.

Two mechanisms are available for this in HappyFace, which can be configured in the [auth] section of the HappyFace configuration. From the default configuration we have

.. code-block:: ini

    [auth]
    # A file containing authorized DNs to access the site.
    # One DN per line
    dn_file = 

    # If the given DN is not found in the file above, if any, the following
    # script is called with DN as first argument.
    # The script must return 1 if user has access, 0 otherwise.
    auth_script = 

At first, the DN from the client is checked against a list of DNs in a file. This is a quick check and since it is a plaintext file, it is easy to maintain.

The second mechanism allows the use of other data sources. A given executable is run, doing whatever it wants and exit with a certain status code. If the status code is 1, the user may access the secured parts of HappyFace, if the status is 0 (or anything != 1), the client may only access the public parts of HappyFace.

.. note:: The script is run whenever a URL below the HappyFace root url is accessed.

    If the authorization script needs to perform expensive or time consuming operations (complex DB queries or slow web queries), you should cache the results locally. For this, a simple SQLite Database should be sufficient.

An example utilizing a Python script to query sitedb. Anyone with a CMS account (technically, where the DN can be converted to a CMS account) has access. Since the script is very simple, it does not cache the results, therefore accessing HappyFace is slowed down noticeably.

.. code-block:: python

    #!/usr/bin/env python
    # -*- coding: UTF-8 -*-

    import os, sys, httplib, json, urllib, ast

    if __name__ == "__main__":
        if len(sys.argv) != 2:
            print "Single Argument, DN, required"
            sys.exit(0)

        con = httplib.HTTPSConnection('cmsweb.cern.ch', 443)
        con.connect()
        try:
            dn = urllib.quote_plus(sys.argv[1])
            con.request('GET', '/sitedb/json/index/dnUserName?dn='+dn)
            response = con.getresponse().read()
            response = ast.literal_eval(response)
            print "Authorized DN"
            sys.exit(1)
        except SyntaxError:
            # Literal eval failed, crazy exception "JSON"
            print "Unknown DN"
            sys.exit(0)
        finally:
            con.close()

Module and Category Configuration
---------------------------------
Limiting access to a module or complete category is very simple. In both the module and category configuration files, the *access* option is supported.

For modules, it must be set to *restricted* or *open*. By default, if *access* is not specified, *open* is assumed. These may be overridden by the category access.

Categories accept *restricted*, *permod* and *open* as valid values for *access*. Basically, *open* and *restricted* set the access option of all included module to the corresponding value, making either all modules open or requiring authorization for all of them.

If you only want to restrict some modules, use *permod*, which is the default. Only in this case the module access variable is used.

.. warning:: Be careful when using *open* together with categories, as you might involuntarily expose sensitive information.

For completeness, an example category configuration is given where the access to all modules restricted.

.. code-block:: ini

    [batch_system]
    name = Batch System
    algorithm = worst
    type = rated
    description = 
    modules = gridka_jobs_statistics

    access = restricted
    
Hints on Databases and Optimization
===================================
Since HappyFace stores alot of data in standard database systems, delivery time and performance of HappyFace depends on data retrieval. There are things that should be taken into account when choosing and configuring a database for HappyFace.

We are no database experts, so this section is mostly our experiences with HappyFace3 and the database systems we used and tested, this is by far not a complete overview of all possible databases, optimization variables or pitfalls. If you encounter issues that should be added to this guide, feel free to contact our development team.

SQLite
------
The database of choice for development environments is SQLite, mainly because no additional configuration is required. Taking backups of SQLite databases, besides copying the database file, is not sanely possible, so this is one reason not to use it in an production environment. To be honest, though, it can handle surprisingly large (~ 20GB) database files.

You might encounter situations where the database is locked, causing all database transactions with a **Database Locked** exception. We do not know where this comes from, probably simultaneous access across processes. So far it only occured on development machines, but with both HappyFace2 and HappyFace3. The common solutions found on the internet to fix the databae do not work for some reason, so your only option would be removing the database.

PostgreSQL
----------
*sqlalchemy* uses connection pooling to speed up sequential database access. For some reason, we had occasional performance issues after short, many HappyFace accesses, that were tracked to the database and idleing processes. It was possible to recover the usual page access times by restarting either PostgreSQL or the HappyFace process, so we assume the error had something to do with the database.

A permanent solution to fix this was setting the *recycle* option in *sqlalchemy*, so our database configuration looks like

.. code-block:: ini

    [database]
    url = postgres://USER@SERVER/DATABASE
    recycle = 10
  
Basically, this closes used connections after 10 seconds of inactivity and opens a fresh connection instead. We did not have these performance issues after wards.
