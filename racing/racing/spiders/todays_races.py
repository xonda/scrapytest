import scrapy


class TodaysRacesSpider(scrapy.Spider):
    name = 'todays'

    start_urls = ['https://www.betbright.com/horse-racing/today']

    def parse(self, response):
        for href in response.css('.event_time::attr(href)').extract():
            yield scrapy.Request(response.urljoin(href),
                                 callback=self.parse_race)

    def parse_race(self, response):
        def get(query):
            return response.css(query).extract_first()

        horses = {}
        for horse in response.css('.horse-datafields'):
            name = horse.css('div.horse-information-name::text').extract_first(),
            uid = horse.css('a.bet_now_btn::attr(data-selection-id)').extract_first(),
            odds = horse.css('a.bet_now_btn::text').extract_first()
            horses[name] = {'uid': uid, 'odds': odds}

        yield {
            'track': get('div.event-name::text')[6:],
            'start': get('div.event-countdown::attr(data-start-date-time)'),
            'uid': get('ul.racecard::attr(data-event-id)'),
            'horses': horses
        }
