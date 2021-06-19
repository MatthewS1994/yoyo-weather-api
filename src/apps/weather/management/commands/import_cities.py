import gzip
import json
import logging
import os
import shutil

import wget
from django.core.management import BaseCommand

from apps.weather.models import City

DOWNLOAD_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../fixtures/.")

logger = logging.getLogger("weather")


class Command(BaseCommand):
    help = (
        "The imported city data is used for searching purposes. i.e: A user is looking for the"
        " weather data for a specific city e.g. Cape Town or London.This data will allow better"
        " accuracy for finding a city. It will alleviate the user from getting NO data back from"
        " the weather API from problems as simple as a spelling mistake"
    )

    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument(
            "--remove",
            dest="remove",
            action="store_true",
            help="Option to DELETE the files before and after it has been imported",
        )
        parser.add_argument(
            "--no-remove",
            dest="remove",
            action="store_false",
            help="Option to KEEP the files from before and after it has been imported",
        )
        parser.set_defaults(remove=True)

    def handle(self, *args, **options):

        file_name = "city.list.json.gz"
        file_names = []
        url = f"http://bulk.openweathermap.org/sample/{file_name}"

        if options["remove"]:
            logger.info("\nRemove any Old Files that are laying around")
            files_to_remove = list(
                filter(lambda x: x.endswith(".gz") or x.endswith(".json"), os.listdir(DOWNLOAD_DIR))
            )
            for remove in files_to_remove:
                logger.info(f"\t- Removing: {remove}")
                os.remove(os.path.join(DOWNLOAD_DIR, remove))

        # WGET to download the file
        logger.info(f"\nDownloading file from source: {url} \n")
        _ = wget.download(str(url), out=os.path.join(DOWNLOAD_DIR, file_name))

        files = list(
            filter(lambda x: x.startswith(file_name.replace(".gz", "")), os.listdir(DOWNLOAD_DIR))
        )

        # Method used to unzip the .gz file and extract to JSON
        logger.info("\n\nExtraction of Files ... ")
        for index, file in enumerate(files):
            logger.info(f"\tExtracting file: {index} - {file}")
            with gzip.open(os.path.join(DOWNLOAD_DIR, file), "rb") as f_in:
                file_name = f"city.list.{index}.json"
                with open(os.path.join(DOWNLOAD_DIR, file_name), "wb") as f_out:
                    shutil.copyfileobj(f_in, f_out)
                    file_names.append(file_name)
                    logger.info(f"\t\t{file} - complete!")

        logger.info("\nPrepare files for database inserts")
        for file in file_names:
            logger.info(f"Storing The City Data from {file} into the database")

            logger.debug("\t\t - Opening file: {file}")
            with open(os.path.join(DOWNLOAD_DIR, file)) as json_file:
                cities = json.load(json_file)
                logger.debug("\t\t - Convert to readable dict")
                city_objs = []

                logger.debug("\t\t - Create tuple of City Model objects")
                # Create a tuple/list of City objects to be bulk inserted
                for city in cities:
                    city_objs.append(
                        City(
                            title=city["name"],
                            related_id=city["id"],
                            country_code=city["country"],
                            lat=city["coord"]["lat"],
                            lon=city["coord"]["lon"],
                        )
                    )

                if len(city_objs) >= 1:
                    logger.debug(f"\t\t - Storing total number of Cities: {len(city_objs)}")

                    # Bulk insert the objects
                    bulk_insert = City.objects.bulk_create(
                        city_objs,
                        batch_size=100,
                    )

                    logger.debug(f"\t\t - Inserted total number of Cities: {len(bulk_insert)}")
                else:
                    logger.debug("\t\t - Storing nothing as the total number of Cities is 0")

                logger.debug(f"\t\t - Closing {file}")
                json_file.close()
            logger.info(f"Stored The City Data from {file} into the database")
        logger.info("Done!")

        if options["remove"]:
            files_to_remove = list(
                filter(lambda x: x.endswith(".gz") or x.endswith(".json"), os.listdir(DOWNLOAD_DIR))
            )
            for remove in files_to_remove:
                logger.info(f"\t- Removing: {remove}")
                os.remove(os.path.join(DOWNLOAD_DIR, remove))
