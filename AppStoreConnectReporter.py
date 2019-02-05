from typing import *
from collections import namedtuple
from AppStoreConnectReporterErrors import RaiseExceptionForCode
import os
import subprocess
import datetime
import calendar
import enum
import logging
import xml.etree.ElementTree
import gzip
import csv


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


class AppSalesReportItem(NamedTuple):
    Provider: str
    ProviderCountry: str
    SKU: str
    Developer: str
    Title: str
    Version: str
    ProductTypeIdentifier: str
    Units: int
    DeveloperProceeds: str
    BeginDate: datetime.datetime
    EndDate: datetime.datetime
    CustomerCurrency: str
    CountryCode: str
    CurrencyOfProceeds: str
    AppleIdentifier: str
    CustomerPrice: float
    PromoCode: str
    ParentIdentifier: str
    Subscription: str
    Period: str
    Category: str
    CMB: str
    Device: str
    SupportedPlatforms: str
    ProceedsReason: str
    PreservedPricing: str
    Client: str
    OrderType: str



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

    def executeCommand(self, command: str): # Returnes ElementTree or None
        """This command can raise the exception AppStoreConnectReporterError or a child exception.
        Returns xml.etree.ElementTree or
        Returns None type for ERROR_CODE_FOR_NoSalesOnSpesifiedDate
        """
        result = subprocess.run(command.split(" "), stdout=subprocess.PIPE)
        xmlString = result.stdout
        xmlString = xmlString.decode("utf-8")
        xmldoc = xml.etree.ElementTree.fromstring(xmlString)

        if result.returncode != 0:
            errorCode = int(xmldoc[0].text)
            errorMessage = xmldoc[1].text
            ERROR_CODE_FOR_NoSalesOnSpesifiedDate = 213
            if errorCode == ERROR_CODE_FOR_NoSalesOnSpesifiedDate:
                return None
            raise RaiseExceptionForCode(errorCode, withMessage=errorMessage)
        return xmldoc

class AppStoreConnectSalesReporter(AppStoreConnectReporter):
    def __init__(self):
        super().__init__()
        self.baseCommand = f"{self.baseCommand}Sales."
        self.keepDownloadedFilesAfterProcessing = False

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

    def getReportFileNameFromCommandOutput(self, xmlTag: xml.etree.ElementTree) -> List[str]:
        """Returns the file name to the tar file as first item of the list and the name of the text file inside of the tar.gz file as second item."""
        message = xmlTag[0].text
        gzFileName = message.replace("Successfully downloaded ", "")
        txtFileName = gzFileName[:-3]  # -3 to remove '.gz'
        logging.debug("tarfilename: "+str(gzFileName))
        return [gzFileName, txtFileName]

    def getReportContentFromGZFile(self, path: str) -> str:
        logging.debug("opening gzfile with path: "+str(path))
        with gzip.open(path) as f:
            return f.read().decode("utf-8")

    def csvRowToAppSalesReportItem(self, csvRowItem: List[Any]) -> AppSalesReportItem:
        item = csvRowItem
        datetimeParseFormatString = "%m/%d/%Y"
        beginDate = datetime.datetime.strptime(item[9], datetimeParseFormatString)
        endDate = datetime.datetime.strptime(item[10], datetimeParseFormatString)

        return AppSalesReportItem(
            Provider=item[0],
            ProviderCountry=item[1],
            SKU=item[2],
            Developer=item[3],
            Title=item[4],
            Version=item[5],
            ProductTypeIdentifier=item[6],
            Units=item[7],
            DeveloperProceeds=item[8],
            BeginDate=beginDate,
            EndDate=endDate,
            CustomerCurrency=item[11],
            CountryCode=item[12],
            CurrencyOfProceeds=item[13],
            AppleIdentifier=item[14],
            CustomerPrice=item[15],
            PromoCode=item[16],
            ParentIdentifier=item[17],
            Subscription=item[18],
            Period=item[19],
            Category=item[20],
            CMB=item[21],
            Device=item[22],
            SupportedPlatforms=item[23],
            ProceedsReason=item[24],
            PreservedPricing=item[25],
            Client=item[26],
            OrderType=item[27]
        )

    def getReportNamedTupelFromCSV(self, content: str, removeHeader: bool = False) -> List[AppSalesReportItem]:
        csvLinesArray = content.splitlines()
        if removeHeader is True:
            del csvLinesArray[0]  # Remove the CSV Header
        csvReader = csv.reader(
            csvLinesArray,
            delimiter="\t"
        )
        salesReport = []
        for item in csvReader:
            salesReport.append(
                self.csvRowToAppSalesReportItem(item)
            )
        return salesReport

    def getReport(self, vendorId: str, *, type: SalesReportType, subType: SalesReportSubType, dateType: DateType, date: datetime.datetime) -> List[AppSalesReportItem]:
        """
        Returnes an empty list if there were no sales for the spesified criteria.
        """
        buildCommand = self.getCommandForGetReport(
            vendorId=vendorId,
            type=type,
            subType=subType,
            dateType=dateType,
            date=date
        )
        output = self.executeCommand(buildCommand)
        if output is None:
            return []
        gzFileName, _ = self.getReportFileNameFromCommandOutput(output)
        gzFilePath = gzFileName
        logging.debug("Using gzFilePath: "+str(gzFilePath))
        reportCSV = self.getReportContentFromGZFile(gzFilePath)
        logging.debug("The report CSV:")
        logging.debug(reportCSV)
        if self.keepDownloadedFilesAfterProcessing is False:
            os.remove(gzFilePath)
        return self.getReportNamedTupelFromCSV(reportCSV, removeHeader=True)


class AppStoreConnectFinancialReporter(AppStoreConnectReporter):
    def __init__(self):
        raise NotImplementedError()
