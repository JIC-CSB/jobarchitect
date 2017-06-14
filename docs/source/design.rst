Design
======


Background
----------

The first implementations of jobarchitect used a basic templating language for
defining jobs, with two reserved keywords ``input_file`` and ``output_file``.
An example input ``job.tmpl`` file would look like the below.

.. code-block:: none

    shasum {{ input_file }} > {{ output_file }}

A later revision made use of the Common Workflow Language, still making use
of the reserved keywords ``input_file`` and ``output_file``. 
The same example as a ``shasum.cwl`` file would look like the below.

.. code-block:: yaml

    cwlVersion: v1.0
    class: CommandLineTool
    inputs:
      input_file:
        type: File
        inputBinding: { position: 1 }
    baseCommand: shasum
    outputs:
      shasum: stdout
    stdout: $(inputs.output_file)

The jobarchitect tool always had an explicit knowledge of ``dtoolcore`` datasets.
The ``sketchjob`` utility uses this knowledge to split the dataset into batches.

When ``dtoolcore`` datasets' gained the ability to store and provide access to
file level metadata our tools started making use of this. However, ``sketchjob``
or more precisely ``_analyse_by_id``, assumed that the tools it ran would not
have an understanding or need to access this dataset file level metadata.

The section below outlines our thinking with regards to overcoming this problem.


Solution
--------

Now that our scripts work on datasets, rather than individual files, they work at
a similar level to ``_analyse_by_id``.

One solution would be to make ``_analyse_by_id`` more complex allowing it to know
when to work on files in a dataset and when to work on datasets and associated
identifiers. The latter is what would be required for our new scripts to work.

Another solution would be to by-pass ``_analyse_by_id`` completely with our
script of interest (that works on datasets and identifiers). The ``_analyse_by_id``
script could remain accessible, via a ``--use-cwl`` option which would invoke
the existing behaviour.

Another solution would be to add another layer of abstraction, for example a
script named ``agent.py`` that could call either ``_analyse_by_id`` or the
provided script. In this scenario ``_analyse_by_id`` and user provided scripts
would become alternative backends to the ``agent.py`` script. As such it would
make sense to rename ``_analyse_by_id`` to ``_cwl_backend``.

We prefer, the latter of these options. The job written out by ``sketchjob``
would then take the form of:

.. code-block:: none

    sketchjob --cwl-backend shasum.cwl exmaple_dataset output/
    #!/bin/bash

    _jobarchitect_agent \
      --cwl-backend
      --tool_path=shasum.cwl \
      --input_dataset_path=example_dataset/ \
      --output_root=output/ \
      290d3f1a902c452ce1c184ed793b1d6b83b59164

Or in the case of a custom script:

.. code-block:: none

    sketchjob scripts/analysis.py exmaple_dataset output/
    #!/bin/bash

    _jobarchitect_agent \
      --tool_path=scripts/analysis.py
      --input_dataset_path=example_dataset/ \
      --output_root=output/ \
      290d3f1a902c452ce1c184ed793b1d6b83b59164
