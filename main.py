import json
import argparse
import pymongo
from AppStoreConnectReporter import *
from AppStoreConnectReporterErrors import *


def AppSalesReportItemToDictAsPreparationForDocumentConvertion(item: Union[AppSalesReportItem, AppSalesReportExtrapolatedDetailItem]) -> Dict[str, Any]:
    logging.debug("Type of item: "+str(type(item)))
    logging.debug("item is: "+str(item))
    formatTimeString = "%Y-%m-%d"
    newItem = {
        "Provider": item.Provider,
        "ProviderCountry": item.ProviderCountry,
        "SKU": item.SKU,
        "Developer": item.Developer,
        "Title": item.Title,
        "Version": item.Version,
        "ProductTypeIdentifier": item.ProductTypeIdentifier,
        "BeginDate": item.BeginDate.strftime(formatTimeString),
        "EndDate": item.EndDate.strftime(formatTimeString),
        "CustomerCurrency": item.CustomerCurrency,
        "CountryCode": item.CountryCode,
        "CurrencyOfProceeds": item.CurrencyOfProceeds,
        "AppleIdentifier": item.AppleIdentifier,
        "PromoCode": item.PromoCode,
        "ParentIdentifier": item.ParentIdentifier,
        "Subscription": item.Subscription,
        "Period": item.Period,
        "Category": item.Category,
        "CMB": item.CMB,
        "Device": item.Device,
        "SupportedPlatforms": item.SupportedPlatforms,
        "Client": item.Client,
        "OrderType": item.OrderType
    }
    if type(item) == AppSalesReportItem:
        newItem["Units"] = item.Units
        newItem["ProceedsReason"] = item.ProceedsReason
        newItem["PreservedPricing"] = item.PreservedPricing
        newItem["CustomerPrice"] = item.CustomerPrice
        newItem["DeveloperProceeds"] = item.DeveloperProceeds

    return newItem


def getReport(date: datetime.datetime, *, period: DateType, forVendorId: str) -> List[AppSalesReportItem]:
    try:
        report = AppStoreConnectSalesReporter().getReport(
            vendorId=forVendorId,
            type=SalesReportType.sales,
            subType=SalesReportSubType.summary,
            dateType=period,
            date=date
        )
        return report

    except InvalidVendor as ex:
        logging.exception(ex)

    except ReportsDelayed as ex:
        logging.exception(ex)

    except ReportNoLongerAvailable as ex:
        logging.exception(ex)

    except ReportNotAvailableYet as ex:
        logging.exception(ex)

    except ReportNotAvailableYetUnexpected as ex:
        logging.exception(ex)

    except Exception as ex:
        logging.exception(ex)
        raise ex
    finally:
        return []


def getReportAsDocumentForMongo(report: List[AppSalesReportItem]) -> List[Dict[str, Any]]:
    reportDictList = []
    for item in report:
        reportDict = AppSalesReportItemToDictAsPreparationForDocumentConvertion(item)
        reportDictList.append(reportDict)
    return reportDictList


def insertToMongoDBOverwritingEntireCollection(mongoconnection: str, database: str, collection: str, document: List):
    mongoClient = pymongo.MongoClient(mongoconnection)
    mongoDatabase = mongoClient[database]
    mongoCollection = mongoDatabase[collection]

    if document is not None and len(document) >= 1:  # dont insert an empty list as that would fail
        mongoCollection.insert_many(document)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Load data from App Store Connect to a database.')
    parser.add_argument('--yesterday-daily', help='Import daily data from yesterday.', action='store_true')
    parser.add_argument('--year', help='The year for the report.', type=int, default=datetime.datetime.now().year)
    parser.add_argument('--month', help='The month for the report.', type=int, default=1)
    parser.add_argument('--day', help='The day for the report.', type=int, default=1)
    parser.add_argument(
        '--period',
        help='The period for the report.',
        type=str, choices=["yearly", "monthly", "weekly", "daily"],
        default="daily"
    )
    parser.add_argument('--log-level', help='The log level to use.', type=int, choices=["DEBUG"])
    parser.add_argument('--print', help='Display the report data on screen.', action='store_true')
    parser.add_argument('--dry-run', help='Dont load data into a database.', action='store_true')
    shellParameters = parser.parse_args()

    if shellParameters.log_level is not None:
        logging.basicConfig(level=logging.DEBUG)

    with open("config.json", "r") as f:
        configObject = json.JSONDecoder().decode(f.read())

    date = None
    if shellParameters.yesterday_daily is True:
        today = datetime.datetime.now()
        yesterday = today - datetime.timedelta(days=1)
        date = yesterday
    else:
        date = datetime.datetime(
            year=shellParameters.year,
            month=shellParameters.month,
            day=shellParameters.day
        )
    logging.debug("Using date: "+str(date))

    report = getReport(
        date,
        period=DateType[shellParameters.period],
        forVendorId=configObject["vendorId"]
    )

    reportSummaryAsMongoDocument = getReportAsDocumentForMongo(report)

    also_extrapolate_detail = configObject["also_extrapolate_detail"]
    if also_extrapolate_detail == True:
        reportExtapolatedDetail = AppStoreConnectSalesReporter.extrapolateDetailReportFromAppleSummaryFormat(report)
        reportDetailAsMongoDocument = getReportAsDocumentForMongo(reportExtapolatedDetail)

    if shellParameters.print is True:
        print("Summary:")
        print(reportSummaryAsMongoDocument)
    if shellParameters.print is True and also_extrapolate_detail:
        print("Detail:")
        print(reportDetailAsMongoDocument)

    if shellParameters.dry_run is False:
        logging.debug("Writing to Database.")
        configDB = configObject["db"]
        insertToMongoDBOverwritingEntireCollection(
            mongoconnection=configDB["connectionString"],
            database=configDB["database"],
            collection=configDB["collection_summary"],
            document=reportSummaryAsMongoDocument
        )
        if also_extrapolate_detail:
            insertToMongoDBOverwritingEntireCollection(
            mongoconnection=configDB["connectionString"],
            database=configDB["database"],
            collection=configDB["collection_detail_extrapolated"],
            document=reportDetailAsMongoDocument
        )