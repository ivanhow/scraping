import json
import scrapy
from ..items import SiteScrapingItem
from datetime import datetime, timedelta


now = datetime.now()
today = now.strftime("%Y-%m-%dT21:00:00.000Z")
yesterday = now - timedelta(days=1)


class MySpider(scrapy.Spider):
    name = 'bids'
    allowed_domains = ['http://www.e-licitatie.ro/pub/notices/contract-notices/list/2/1']
    start_urls = ['http://www.e-licitatie.ro/api-pub/NoticeCommon/GetCNoticeList/']

    def start_requests(self):
        header = {'Accept': 'application/json, text/plain, */*',
                   'Accept-Language': 'en-US,en;q=0.9,bg;q=0.8,la;q=0.7',
                   'Authorization': 'Bearer null',
                   'Connection': 'keep-alive',
                   'Content-Type': 'application/json;charset=UTF-8',
                   'Culture': 'en-US',
                   'DNT': '1',
                   'HttpSessionID': 'null',
                   'Origin': 'http://www.e-licitatie.ro',
                   'Referer': 'http://www.e-licitatie.ro/pub/notices/contract-notices/list/2/1', }

        params = {
            "sysNoticeTypeIds": ['2'],
            "sortProperties": [],
            "pageSize": '100',
            "hasUnansweredQuestions": 'false',
            "startPublicationDate": f'{yesterday.strftime("%Y-%m-%dT21:00:00.000Z")}',
            "sysProcedureStateId": '2',
            "pageIndex": '0',
            "endPublicationDate": f'{yesterday.strftime("%Y-%m-%dT21:00:00.000Z")}',
        }
        yield scrapy.FormRequest(url='http://www.e-licitatie.ro/api-pub/NoticeCommon/GetCNoticeList/', callback=self.parse,
                                 method='POST', body=json.dumps(params), headers=header)

    def parse(self, response, **kwargs):
        items = SiteScrapingItem()
        scraped_data = json.loads(response.body)
        for i in range(len(scraped_data['items'])):
            date = now.strftime("%d.%m.%Y")
            notice_number = scraped_data['items'][i]['noticeNo']
            tender_name = scraped_data['items'][i]['contractTitle']
            procedure_state = scraped_data['items'][i]['sysProcedureState']["text"]
            contract_type = scraped_data['items'][i]['sysAcquisitionContractType']["text"]
            if scraped_data['items'][i]['isOnline']:
                type_of_procurement = 'ONLINE'
            else:
                type_of_procurement = 'OFFLINE'
            estimated_value = str(scraped_data['items'][i]['estimatedValueRon'])

            items['date'] = date
            items['notice_number'] = notice_number
            items['tender_name'] = tender_name
            items['procedure_state'] = procedure_state
            items['contract_type'] = contract_type
            items['type_of_procurement'] = type_of_procurement
            items['estimated_value'] = estimated_value
            yield items
