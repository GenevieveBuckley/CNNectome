import argparse
import os
from CNNectome.utils.hierarchy import hierarchy
from CNNectome.utils.cosem_db import MongoCosemDB, CosemCSV
from CNNectome.utils import config_loader


def transfer(training_version="v0003.2"):
    db = MongoCosemDB(training_version=training_version)
    eval_col = db.access("evaluation", db.training_version)
    eval_results_csv_folder = os.path.join(config_loader.get_config()["organelles"]["evaluation_path"],
                                           training_version,
                                           "evaluation_results")

    csv_d = CosemCSV(eval_results_csv_folder)
    for l in hierarchy.keys():
        csv_d.erase(l)
    for db_entry in eval_col.find():
        csv_d.write_evaluation_result(db_entry)


def main():
    parser = argparse.ArgumentParser("Transfer contents of evaluation database to csv file")
    parser.add_argument("--training_version", type=str, default="v0003.2", help="Version of training for which to"
                                                                                "transfer evaluation results.")
    args = parser.parse_args()
    transfer(training_version=args.training_version)


if __name__ == "__main__":
    main()
