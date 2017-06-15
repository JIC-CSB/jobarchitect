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

- Singularity template


Deprecated
^^^^^^^^^^


Removed
^^^^^^^


Fixed
^^^^^

- Naming of ``sketchjob`` input argument


Security
^^^^^^^^


[0.5.0] - 2017-06-15
--------------------

Added
^^^^^

- Ability to access file level metadata from dataset items when running
  a Python analysis script


Changed
^^^^^^^

- Tools now need to comply with a specific command line interface to
  be able to run using scripts produced by ``sketchjob``. The command
  line interface of such "smart" scripts should have no positional arguments
  and has three required named arguments: ``--dataset-path``, ``-identifier``,
  and ``--output-path``. Furthermore, the such "smart" analysis scripts
  should only work on one item in a dataset as it is the responsibility of
  ``sketchjob`` and the jobarchitect ``agent`` to split the dataset into
  individual jobs.
- For jobs that do not adhere to the command line interface above one will
  have to write thin Python wrappers, for examples have a look at the scripts
  in ``tests/sample_smart_tools/``
- Requiring use of "smart" tools removes the need to make use of CWL, so it's
  support has been removed
- See the :doc:`design` document for more details about the thought process
  that led to this redesign.


Removed
^^^^^^^

- CWL support


[0.4.0] - 2017-06-08
--------------------

Changed
^^^^^^^

- Now using CWL (Common Workflow Language) to specify program to be run on dataset.



[0.3.0] - 2017-02-07
--------------------

Changed
^^^^^^^

- Move ``JobSpec`` from ``jobarchitect`` to ``jobarchitect.backends`` module
- ``JobSpec`` class now stores absolute paths
- Update Dockerfile to set entrypoint to sketchjob


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

