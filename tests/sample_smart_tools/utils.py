import os


def write_shasum(output_directory, shasum, fpath):
    output_fpath = os.path.join(output_directory, os.path.basename(fpath))
    with open(output_fpath, "w") as fh:
        shasum_string = "{} {}\n".format(shasum, fpath)
        fh.write(shasum_string)
