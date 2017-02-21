import scrapy


class TodaysRacesSpider(scrapy.Spider):
    name = 'todays'

    start_urls = ['https://www.betbright.com/horse-racing/today']

    def parse(self, response):
        for href in response.css('.event_time::attr(href)').extract():
            yield scrapy.Request(response.urljoin(href),
                                 callback=self.parse_race)

    def parse_race(self, response):
        horses = {}
        for horse in response.css('.horse-datafields'):
            name = horse.css('div.horse-information-name::text').extract_first()
            uid = horse.css('a.bet_now_btn::attr(data-selection-id)').extract()[-1]
            odds = horse.css('a.bet_now_btn::text').extract()[-1]
            horses[name] = {'uid': uid, 'odds': odds}

        yield {
            'track': response.css('div.event-name::text').extract_first()[6:],
            'start': response.css('div.event-countdown::attr(data-start-date-time)').extract_first(),
            'uid': response.css('ul.racecard::attr(data-event-id)').extract_first(),
            'horses': horses
        }
