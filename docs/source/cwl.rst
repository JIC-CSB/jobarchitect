Defining jobs using CWL
=======================

CWL tools are defined using a YAML syntax. They specify the way in which a command is run. 

When Jobarchitect uses CWL to run its jobs, it makes use of two hardcoded parameters, 
input_file and output_file. These are then dynamically generated from items in the
dataset.

An example wrapping the ``cp`` command looks like this:

.. code-block:: yaml

    cwlVersion: v1.0
    class: CommandLineTool
    baseCommand: cp
    inputs:
      input_file:
        type: File
        inputBinding:
          position: 1
      output_file:
        type: string
        inputBinding:
          position: 2
    outputs:
       an_output_file:
         type: File
         outputBinding:
           glob: $(inputs.output_file)

This can then be combined with the job description file below.

.. code-block:: yaml

    input_file:
      class: File
      path: /Users/olssont/sandbox/cwl_v1/dummy.txt 
    output_file: dummycopy.txt

The job description files are generated dynamically by Jobarchitect's agent
(``_analyse_by_ids``) at runtime.

A different example using redirection (such that output is captured from stdout) is
illustrated below:

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
