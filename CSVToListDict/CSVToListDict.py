import csv
from logging import Logger


class FieldnamesMismatch(Exception):
    ...


def GetListDict(csv_file, fieldnames, logger: Logger) -> list:
    """Opens the CSV and reads it into a DictReader() then creates a list_dict and returns that."""
    list_dict = []
    logger.debug(f"csv file: {csv_file} with fieldnames: {fieldnames} entered to GetListDict")
    logger.info(f"getting list_dict from {csv_file}")
    # added encoding to deal with bug on 4/5/23
    with open(csv_file, encoding='utf-8') as csv_f:
        # YOU CANNOT USE CSV_F.READLINE BEFORE THE CHECK
        # OR THE COMPARISON WILL CHECK AGAINST LINE 2 AND WILL ALWAYS FAIL
        if [f.strip() for f in fieldnames] == [x.strip() for x in csv_f.readline().split(",")]:
            dictr = csv.DictReader(csv_f, fieldnames=fieldnames)
            logger.debug("DictReader Created")
            for row in dictr:
                list_dict.append(row)
                logger.debug(f"The following row was appended to list_dict {row}")
            logger.info(f"Returning list_dict with {len(list_dict)} entries")
            return list_dict
        else:
            try:
                raise FieldnamesMismatch("Make sure the CSV field names list chosen, matches the CSV chosen")
            except FieldnamesMismatch as e:
                logger.error(e, exc_info=True)
                raise e
