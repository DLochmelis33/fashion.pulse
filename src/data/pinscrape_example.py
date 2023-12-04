from pinscrape import pinscrape
details = pinscrape.scraper.scrape("grunge", "output", {}, 10, 20)

if details["isDownloaded"]:
    print("\nDownloading completed !!")
    print(f"\nTotal urls found: {len(details['extracted_urls'])}")
    print(f"\nTotal images downloaded (including duplicate images): {len(details['url_list'])}")
    print(details)
else:
    print("\nNothing to download !!")

