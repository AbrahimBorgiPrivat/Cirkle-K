import logging

from libraries.scripts.upserts import (
    interview_item_images,
    interview_item_master,
    interview_site_master,
    interview_transactions,
)

logger = logging.getLogger(__name__)

RUN_MODULES = [
    ("Upsert Interview Item Master", interview_item_master),
    ("Upsert Interview Item Images", interview_item_images),
    ("Upsert Interview Site Master", interview_site_master),
    ("Upsert Interview Transactions", interview_transactions),
]


def main(create_table_if_not_exist: bool = True):
    for name, module in RUN_MODULES:
        logger.info("Running: %s", name)
        module.main(create_table_if_not_exist=create_table_if_not_exist)
        logger.info("Completed: %s", name)


if __name__ == "__main__":
    main()
