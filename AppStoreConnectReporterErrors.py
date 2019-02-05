class AppStoreConnectReporterError(Exception):
    pass


class InvalidApplicationOrMethodName(AppStoreConnectReporterError):
    pass


class InvalidMethod(AppStoreConnectReporterError):
    pass


class InvalidParameterCount(AppStoreConnectReporterError):
    pass


class PropertiesFileNotFound(AppStoreConnectReporterError):
    pass


class InvalidPropertiesFile(AppStoreConnectReporterError):
    pass


class InvalidCredentials(AppStoreConnectReporterError):
    pass


class EndpointMissing(AppStoreConnectReporterError):
    pass


class NetworkOffline(AppStoreConnectReporterError):
    pass


class NetworkApplicationError(AppStoreConnectReporterError):
    pass


class FileNotSaved(AppStoreConnectReporterError):
    pass


class InvalidOutputStyle(AppStoreConnectReporterError):
    pass


class InvalidAPIVersion(AppStoreConnectReporterError):
    pass


class InvalidAPIService(AppStoreConnectReporterError):
    pass


class ReportsDelayed(AppStoreConnectReporterError):
    pass


class ReportDownloadError(AppStoreConnectReporterError):
    pass


class InvalidParameterVersion(AppStoreConnectReporterError):
    pass


class ParameterVersionMissing(AppStoreConnectReporterError):
    pass


class AccessTokenExpired(AppStoreConnectReporterError):
    pass


class InvalidAccessToken(AppStoreConnectReporterError):
    pass


class InvalidVendor(AppStoreConnectReporterError):
    pass


class InvalidReportType(AppStoreConnectReporterError):
    pass


class InvalidReportSubType(AppStoreConnectReporterError):
    pass


class InvalidReportCombination(AppStoreConnectReporterError):
    pass


class InvalidDate(AppStoreConnectReporterError):
    pass


class InvalidReportTypeAndDateCombination(AppStoreConnectReporterError):
    pass


class InvalidReportSubTypeAndDateCombination(AppStoreConnectReporterError):
    pass


class ReportNoLongerAvailable(AppStoreConnectReporterError):
    pass


class ReportNotAvailableYet(AppStoreConnectReporterError):
    pass


class ReportNotAvailableYetUnexpected(AppStoreConnectReporterError):
    pass


class UnexpectedError(AppStoreConnectReporterError):
    pass


class AmbiguousAccountNumber(AppStoreConnectReporterError):
    pass


class InvalidAccountNumber(AppStoreConnectReporterError):
    pass


class InvalidRegioinCode(AppStoreConnectReporterError):
    pass


class InvalidFiscalYear(AppStoreConnectReporterError):
    pass


class InvalidFiscalPeriod(AppStoreConnectReporterError):
    pass


EXCEPTION_FOR_CODE = {
    100: InvalidApplicationOrMethodName,
    101: InvalidMethod,
    102: InvalidParameterCount,
    103: PropertiesFileNotFound,
    104: PropertiesFileNotFound,
    105: InvalidPropertiesFile,
    108: InvalidCredentials,
    109: EndpointMissing,
    110: NetworkOffline,
    111: NetworkApplicationError,
    112: FileNotSaved,
    113: InvalidOutputStyle,
    114: InvalidAPIVersion,
    115: InvalidAPIService,
    117: ReportsDelayed,
    119: ReportDownloadError,
    120: InvalidParameterVersion,
    121: ParameterVersionMissing,
    123: AccessTokenExpired,
    124: InvalidAccessToken,
    125: InvalidAccessToken,
    131: InvalidCredentials,
    132: InvalidCredentials,
    200: InvalidVendor,
    201: InvalidReportType,
    202: InvalidReportSubType,
    203: InvalidReportCombination,
    204: InvalidDate,
    205: InvalidDate,
    206: InvalidReportSubTypeAndDateCombination,
    207: InvalidDate,
    208: InvalidReportTypeAndDateCombination,
    209: ReportNoLongerAvailable,
    210: ReportNotAvailableYet,
    211: ReportNotAvailableYetUnexpected,
    212: UnexpectedError,
    214: AmbiguousAccountNumber,
    215: InvalidAccountNumber,
    216: InvalidAccountNumber,
    300: InvalidVendor,
    301: InvalidReportType,
    316: InvalidRegioinCode,
    314: InvalidFiscalYear,
    315: InvalidFiscalPeriod,
}


def RaiseExceptionForCode(code: int, withMessage: str):
    ex = EXCEPTION_FOR_CODE[code]
    raise ex(withMessage)
