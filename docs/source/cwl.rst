Defining jobs using CWL
=======================

CWL tools are defined using a YAML syntax. They specify the way in which a command is run. 

When Jobarchitect uses CWL to run its jobs, it makes use of two hardcoded parameters, 
input_file and output_file. These are then dynamically generated from items in the
dataset.

A simple example wrapping the ``cp`` command looks like this:

.. code-block:: yaml

    cwlVersion: cwl:draft-3
    class: CommandLineTool
    baseCommand: cp
    inputs:
      - id: input_file
        type: string
        inputBinding:
          position: 1
      - id: output_file
        type: string
        inputBinding:
          position: 2
    outputs: []

A more complicated example using redirection (such that output is captured from stdout):

.. code-block:: yaml

    cwlVersion: cwl:draft-3
    class: CommandLineTool
    baseCommand: shasum
    stdout: $(inputs['output_file'])
    inputs:
      - id: input_file
        type: string
        inputBinding:
          position: 1
      - id: output_file
        type: string
    outputs:
      - id: output_file
        type: File
        outputBinding:
          glob: $(inputs['output_file'])

To actually run tools, CWL requires a job description YAML (or JSON) file. Using the command line runner, an example would be:

.. code-block:: yaml

    input_file: /Users/hartleym/projects/exploration/cwl/dummy.txt
    output_file: dummycopy.txt
    
These files are generated dynamically by Jobarchitect's agent (``_analyse_by_ids``) at runtime.
