import unittest
import xml.etree.ElementTree
from AppStoreConnectReporter import *


class AppStoreConnectReporterTestCase(unittest.TestCase):
    def test_buildFormatedDateFromDate_Daily(self):
        day = 10
        month = 10
        year = 2019
        date = datetime.datetime(year=year, month=month, day=day)
        buildDate = AppStoreConnectReporter().buildFormatedDateFromDate(date, format=DateType.daily)
        buildDateSholdBe = str(year)+str(month)+str(day)
        self.assertEqual(buildDate, buildDateSholdBe)

    def test_buildFormatedDateFromDate_Weekly(self):
        day = 10
        month = 10
        year = 2019
        date = datetime.datetime(year=year, month=month, day=day)
        buildDate = AppStoreConnectReporter().buildFormatedDateFromDate(date, format=DateType.weekly)
        buildDateSholdBe = str(year)+str(month)+str(day)
        self.assertEqual(buildDate, buildDateSholdBe)

    def test_buildFormatedDateFromDate_Monthly(self):
        day = 10
        month = 10
        year = 2019
        date = datetime.datetime(year=year, month=month, day=day)
        buildDate = AppStoreConnectReporter().buildFormatedDateFromDate(date, format=DateType.monthly)
        buildDateSholdBe = str(year)+str(month)
        self.assertEqual(buildDate, buildDateSholdBe)

    def test_buildFormatedDateFromDate_Yearly(self):
        day = 10
        month = 10
        year = 2019
        date = datetime.datetime(year=year, month=month, day=day)
        buildDate = AppStoreConnectReporter().buildFormatedDateFromDate(date, format=DateType.yearly)
        buildDateSholdBe = str(year)
        self.assertEqual(buildDate, buildDateSholdBe)

    def test_buildCommand(self):
        testCommand = "testCommand"
        testParamters = ["one", "two", "three"]
        testBaseCommand = "testBaseCommandString"
        buildCommand = AppStoreConnectReporter().buildCommand(testCommand, parameters=testParamters, baseCommand=testBaseCommand)
        buildCommandParameterStringShouldBe = str.join(", ", testParamters)
        buildCommandShouldBe = f"{testBaseCommand}{testCommand} {buildCommandParameterStringShouldBe}"
        self.assertEqual(buildCommand, buildCommandShouldBe)


class AppStoreConnectSalesReporterTestCase(unittest.TestCase):
    def test_getCommandForGetReport(self):
        testVendorId = "000000"
        testType = SalesReportType.sales
        testSubType = SalesReportSubType.summary
        testDateType = DateType.yearly
        testYear = 2019

        salesReporter = AppStoreConnectSalesReporter()
        buildCommandString = salesReporter.getCommandForGetReport(
            vendorId=testVendorId,
            type=testType,
            subType=testSubType,
            dateType=testDateType,
            date=datetime.datetime(year=testYear, month=1, day=1)
        )
        buildCommandStringShouldBe = f"{salesReporter.baseCommand}getReport {testVendorId}, {testType.value}, {testSubType.value}, {testDateType.value}, {str(testYear)}, 1_0"
        self.assertEqual(buildCommandString, buildCommandStringShouldBe)

    def test_getReportFileNameFromCommandOutput(self):
        testNameBase = "P_S_W_000000_20150208"
        testFileNameGZ = f"{testNameBase}.txt.gz"
        testFileNameTxt = f"{testNameBase}.txt"

        testXMLString = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
            <Output>
                <Message>Successfully downloaded {testFileNameGZ}</Message>
            </Output>
            """
        testXMLTree = xml.etree.ElementTree.fromstring(testXMLString)
        salesReporter = AppStoreConnectSalesReporter()
        resultingGZFileName, resultTxtFileName = salesReporter.getReportFileNameFromCommandOutput(testXMLTree)
        resultShouldIs = [resultingGZFileName, resultTxtFileName]
        resultShouldBe = [testFileNameGZ, testFileNameTxt]
        self.assertEqual(resultShouldBe, resultShouldIs)


class ExtrapolateDetailReportFromAppleSummaryFormatTestCase(unittest.TestCase):
    def test_createsOneItemForEeachUnit(self):
        testAmountOfUnits = 2
        mockAppleSalesSummaryFormat = [
            AppSalesReportItem(
                Title = "TestApp#1",
                Units = testAmountOfUnits
            )
        ]
        result = AppStoreConnectSalesReporter.extrapolateDetailReportFromAppleSummaryFormat(mockAppleSalesSummaryFormat)
        self.assertEqual(testAmountOfUnits, len(result))

    def test_retunsSameAsInputIfNotMultipleUnitsInItem(self):
        mockAppleSalesSummaryFormat = [
            AppSalesReportItem(
                Title = "TestApp#1",
                Units = 1
            )
        ]
        result = AppStoreConnectSalesReporter.extrapolateDetailReportFromAppleSummaryFormat(mockAppleSalesSummaryFormat)
        self.assertEqual(len(mockAppleSalesSummaryFormat), len(result))

if __name__ == '__main__':
    unittest.main()
