from AppStoreConnectReporter import *

if __name__ == "__main__":
    #     def getReport(vendorId: str, *, type: SalesReportType, subType: dateType: DateType, date: datetime.datetime):
    AppStoreConnectSalesReporter().getReport(vendorId="",
        type=SalesReportType.sales,
        subType=SalesReportSubType.summary,
        dateType=DateType.daily,
        date=datetime.datetime.now()
    )
