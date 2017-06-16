import os
import argparse

from dtoolcore import DataSet


def main(dataset_path, identifier, output_directory):
    dataset = DataSet.from_path(dataset_path)
    fpath = dataset.abspath_from_identifier(identifier)
    output_fpath = os.path.join(output_directory, os.path.basename(fpath))
    with open(output_fpath, "w") as fh:
        shasum_string = "{} {}\n".format(identifier, fpath)
        fh.write(shasum_string)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset-path", required=True)
    parser.add_argument("--identifier", required=True)
    parser.add_argument("--output-directory", required=True)
    args = parser.parse_args()

    main(args.dataset_path, args.identifier, args.output_directory)
