
def write_shasum(output_path, shasum, fpath):
    with open(output_path, "w") as fh:
        shasum_string = "{} {}\n".format(shasum, fpath)
        fh.write(shasum_string)
