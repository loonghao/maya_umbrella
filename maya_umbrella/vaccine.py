class AbstractVaccine(object):
    """Abstract base class for Vaccine classes.

    Attributes:
        virus_name (str): The name of the virus.
        api (MayaVirusCleaner): The VaccineAPI instance.
        logger (Logger): The logger instance.
    """

    virus_name = None

    def __init__(self, api, logger):
        """Abstract class for Vaccine.

        Args:
            api (MayaVirusCleaner): The VaccineAPI instance.
            logger (Logger): The logger instance.

        """
        self.api = api
        self.logger = logger

    def collect_issues(self):
        """Collect issues related to the virus.

        Raises:
            NotImplementedError: This method must be implemented in the derived classes.
        """
        raise NotImplementedError

    def report_issue(self, name):
        """Report an issue related to the virus.

        Args:
            name (str): The name of the issue.
        """
        self.logger.warning(self.api.translator.translate("report_issue", name=name))
