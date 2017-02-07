CHANGELOG
=========

This project uses `semantic versioning <http://semver.org/>`_.
This change log uses principles from `keep a changelog <http://keepachangelog.com/>`_.

[Unreleased]
------------

Added
^^^^^


Changed
^^^^^^^

- ``JobSpec`` class now stores absolute paths


Deprecated
^^^^^^^^^^


Removed
^^^^^^^


Fixed
^^^^^



Security
^^^^^^^^

[0.2.0] - 2017-02-06
--------------------

Added
^^^^^

- singularity job command backend
- sketchjob CLI options for selecting wrapper script
- Templates for both job command and wrapper script creation
- ``jobarchitect.backends.render_script`` function
- Hosting of docs on `readthedocs <http://jobarchitect.readthedocs.io/>`_
- API documentation to sphinx generated docs
- Change log to sphinx generated docs
- Better docstrings


[0.1.0] - 2017-02-03
--------------------

Added
^^^^^

- ``sketchjob`` CLI
- ``_analyse_by_ids`` CLI
- Support script and files to build docker image
- ``jobarchitect.JobSpec`` class
- ``jobarchitect.agent.analyse_by_identifiers`` function
- ``jobarchitect.agent.Agent`` class
- ``jobarchitect.backends.generate_docker_job`` backend
- ``jobarchitect.sketchjob.generate_jobspecs`` function
- ``jobarchitect.sketchjob.sketch`` function
- ``jobarchitect.sketchjob.JobSketcher`` class
- ``jobarchitect.utils.mkdir_parents`` function
- ``jobarchitect.utils.output_path_from_hash`` function
- ``jobarchitect.utils.split_dataset`` function
- ``jobarchitect.utils.path_from_hash`` function

Changed
^^^^^^^


Deprecated
^^^^^^^^^^


Removed
^^^^^^^


Fixed
^^^^^


Security
^^^^^^^^

