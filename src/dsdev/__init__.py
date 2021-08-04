import datetime
import logging

# Add NullHandler for logging as library mode
# refs: https://realpython.com/python-logging-source-code/#library-vs-application-logging-what-is-nullhandler # noqa: E501
logging.getLogger(__name__).addHandler(logging.NullHandler())

__version__ = "0.0.2"

__maintainer__ = "An Truong"

__maintainer_email__ = "bian.tquang@gmail.com"

__copyright__ = f"Copyright 2020-{datetime.date.today()} An Truong"
