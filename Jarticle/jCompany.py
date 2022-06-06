from FDate import DATE
from FList import LIST
from FSON import DICT
from FLog.LOGGER import Log
from Jarticle.jHelper import JQ, F
from Jarticle.jQuery import jSearch
from M.MQuery import Q

Log = Log("jCompany")

COMPANIES_COLLECTION = "companies"

""" Master Class to work with Companies Collection """
class jCompany(jSearch):

    @classmethod
    def constructor_jcompany(cls):
        nc = cls()
        nc.construct_mcollection(COMPANIES_COLLECTION)
        return nc

    def add_companies(self, list_of_companies):
        for item in list_of_companies:
            print(item)
            self.insert_record(item)

    def find_company_by_ticker(self, ticker):
        company_record = self.base_query({'ticker': ticker})
        if company_record:
            single_record = LIST.get(0, company_record, False)
            return single_record
        return False

    def find_ticker_by_company(self, companyName, tickerOnly=False):
        company_record = self.base_query({'name': companyName})
        if company_record:
            single_record = LIST.get(0, company_record, False)
            if tickerOnly:
                ticker = DICT.get("ticker", single_record)
                return ticker
            return single_record
        return False

    def get_company_id_for_ticker(self, ticker):
        company = self.find_company_by_ticker(ticker)
        if company:
            id = DICT.get("_id", company)
            return id
        return False

    def get_list_of_all_companies(self):
        all_ = self.base_query({}, page=False, limit=False)
        return all_


if __name__ == '__main__':
    jc = jCompany.constructor_jcompany()
    record = jc.find_company_by_ticker("AMD")
    print(record)