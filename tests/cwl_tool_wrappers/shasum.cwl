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
