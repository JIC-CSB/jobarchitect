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
