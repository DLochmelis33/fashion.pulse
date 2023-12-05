from pinscrape import pinscrape

if __name__ == '__main__':
    details = pinscrape.scraper.scrape("grunge", "test-grunge", {}, 10, 20)

    if details["isDownloaded"]:
        print("\nDownloading completed !!")
        print(f"\nTotal urls found: {len(details['extracted_urls'])}")
        print(
            f"\nTotal images downloaded (including duplicate images): {len(details['url_list'])}"
        )
        print(details)
    else:
        print("\nNothing to download !!")
