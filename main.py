from AppStoreConnectReporter import *

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    report = AppStoreConnectSalesReporter().getReport(
        vendorId="000000",
        type=SalesReportType.sales,
        subType=SalesReportSubType.summary,
        dateType=DateType.monthly,
        date=datetime.datetime(year=2018, month=6, day=1)
    )
    print(report)
