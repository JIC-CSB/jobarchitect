cwlVersion: v1.0
class: CommandLineTool
inputs:
  input_file:
    type: File
    inputBinding: { position: 1 }
baseCommand: sha1sum
outputs:
  sha1sum: stdout
stdout: $(inputs.output_file)
