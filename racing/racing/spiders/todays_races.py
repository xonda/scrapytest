import scrapy


class TodaysRacesSpider(scrapy.Spider):
    name = 'todays'

    start_urls = ['https://www.betbright.com/horse-racing/today']

    def parse(self, response):
        for href in response.css('.event_time::attr(href)').extract():
            yield scrapy.Request(response.urljoin(href),
                                 callback=self.parse_race)

    def parse_race(self, response):
        def extract_with_css(query):
            return response.css(query).extract()

        yield {
            'track': extract_with_css('div.event-name::text')[6:],
            'start': extract_with_css('div.event-countdown::attr(data-start-date-time)'),
            'uid': extract_with_css('ul.racecard::attr(data-event-id)'),
            # 'participants': extract_with_css('div.horse-information-name::text'),
            'participants': {
                extract_with_css('div.horse-information-name::text'),
                extract_with_css('span.recent_form::text'),

            },
        }
