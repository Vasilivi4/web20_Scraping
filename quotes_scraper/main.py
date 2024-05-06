from scrapy.cmdline import execute

# Запускаємо краулер для проекту Scrapy
execute(["scrapy", "crawl", "quotes", "-o", "quotes.json"])
