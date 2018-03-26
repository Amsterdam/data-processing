from src.datapunt_processing.helpers.getaccesstoken import GetAccessToken


def test_employee_plus_login(caplog):
    """Add DATAPUNT_EMAIL and DATAPUNT_PASSWORD test credtials to environment variables to test."""
    access_token = GetAccessToken().getAccessToken(usertype='employee_plus', scopes='BRK/RO,BRK/RS,BRK/RSN', acc=True)
    assert(isinstance(access_token, dict))


def test_employee_login():
    """Only testable in internal network"""
    access_token = GetAccessToken().getAccessToken(usertype='employee_plus', scopes='TLLS/R', acc=True)
    assert(isinstance(access_token,dict))
