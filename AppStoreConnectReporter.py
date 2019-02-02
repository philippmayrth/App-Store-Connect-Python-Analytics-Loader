from typing import *
from AppStoreConnectReporterErrors import RaiseExceptionForCode
import os
import subprocess
import datetime
import calendar
import enum
import logging
import xml.etree.ElementTree


class SalesReportType(enum.Enum):
    sales = "Sales"


class SalesReportSubType(enum.Enum):
    """
    Note the detail report type wont work with Apps.
    It appers that only works with Music, Videos and TV content.
    This is the reason why its not used here.
    """
    summary = "Summary"


class DateType(enum.Enum):
    daily = "Daily"
    weekly = "Weekly"
    monthly = "Monthly"
    yearly = "Yearly"


class AppStoreConnectReporter:
    """
    Do not use this class direclty. Use a subclass instead.
    """
    def __init__(self):
        directoryContainingScriptPath = os.path.dirname(os.path.abspath(__file__))
        reporterFilePath = os.path.join(
            directoryContainingScriptPath,
            "Reporter.jar"
        )
        self.baseCommand = f'/usr/bin/java -jar {reporterFilePath} p=Reporter.properties m=Robot.XML '

    def buildFormatedDateFromDate(self, date: datetime.datetime, format: DateType) -> str:
        DATE_YYYYMMDD = date.strftime("%Y%m%d")
        DATE_YYYYMM = date.strftime("%Y%m")
        DATE_YYYY = date.strftime("%Y")

        if format == DateType.daily:
            return DATE_YYYYMMDD
        if format == DateType.weekly:
            return DATE_YYYYMMDD
        if format == DateType.monthly:
            return DATE_YYYYMM
        if format == DateType.yearly:
            return DATE_YYYY

        raise NotImplementedError("Unknown date format")

    def buildCommand(self, name: str, *, parameters: List[str], baseCommand: str) -> str:
        """
        This method require the self.baseCommand to be overwritten by its subcalss.
        """
        buildParameters = str.join(", ", parameters)
        build = f"{baseCommand}{name} {buildParameters}"
        return build

    def executeCommand(self, command: str) -> xml.etree.ElementTree:
        """This command can raise the exception AppStoreConnectReporterError or a child exception."""
        result = subprocess.run(command.split(" "), stdout=subprocess.PIPE)
        xmlString = result.stdout
        xmlString = xmlString.decode("utf-8")
        xmldoc = xml.etree.ElementTree.fromstring(xmlString)
        try:
            result.check_returncode()
        except subprocess.CalledProcessError as ex:
            errorCode = int(xmldoc[0].text)
            errorMessage = xmldoc[1].text
            logging.exception(ex)
            logging.debug("XML Returned by subprocess is: ")
            logging.debug(xmlString)
            raise RaiseExceptionForCode(errorCode, withMessage=errorMessage)


class AppStoreConnectSalesReporter(AppStoreConnectReporter):
    def __init__(self):
        super().__init__()
        self.baseCommand = f"{self.baseCommand}Sales."

    def getCommandForGetReport(self, vendorId: str, *, type: SalesReportType, subType: SalesReportSubType, dateType: DateType, date: datetime.datetime) -> str:
        command = "getReport"
        parameterReportVersion = "1_0"  # just make sure we get the XML we can work with
        commandParameters = [
            vendorId,
            type.value,
            subType.value,
            dateType.value,
            self.buildFormatedDateFromDate(date, format=dateType),
            parameterReportVersion
        ]
        buildCommand = self.buildCommand(command, parameters=commandParameters, baseCommand=self.baseCommand)
        return buildCommand

    def getReport(self, vendorId: str, *, type: SalesReportType, subType: SalesReportSubType, dateType: DateType, date: datetime.datetime):
        buildCommand = self.getCommandForGetReport(
            vendorId=vendorId,
            type=type,
            subType=subType,
            dateType=dateType,
            date=date
        )
        self.executeCommand(buildCommand)


class AppStoreConnectFinancialReporter(AppStoreConnectReporter):
    def __init__(self):
        raise NotImplementedError()
