import os
import sys
import argparse
import getpass
from twitter_scraper import Twitter_Scraper

try:
    from dotenv import load_dotenv

    print("Loading .env file")
    load_dotenv()
    print("Loaded .env file\n")
except Exception as e:
    print(f"Error loading .env file: {e}")
    sys.exit(1)


def main():
    try:
        TWITTER_SCRAPER_DESCRIPTION = "Twitter Scraper is a tool that allows you to scrape tweets from twitter without using Twitter's API."
        parser = argparse.ArgumentParser(add_help=True, usage="python scraper [option] ... [arg] ...", description=TWITTER_SCRAPER_DESCRIPTION,)

        try:
            parser.add_argument("--user", type=str, default=os.getenv("TWITTER_USERNAME"), help="Your Twitter username.",)
            parser.add_argument("--password", type=str, default=os.getenv("TWITTER_PASSWORD"), help="Your Twitter password.",)

        except Exception as e:
            print(f"Error retrieving environment variables: {e}")
            sys.exit(1)

        parser.add_argument("-t", "--tweets", type=int, default=50, help="Number of tweets to scrape (default: 50)",)
        parser.add_argument("-u", "--username", type=str, default=None, help="Twitter username. Scrape tweets from a user's profile.",)
        parser.add_argument("-ht", "--hashtag", type=str, default=None, help="Twitter hashtag. Scrape tweets from a hashtag.",)
        parser.add_argument("-q", "--query", type=str, default=None, help="Twitter query or search. Scrape tweets from a query or search.",)
        parser.add_argument("-a", "--add", type=str, default="", help="Additional data to scrape and save in the .csv file.",)
        parser.add_argument("--latest", action="store_true", help="Scrape latest tweets",)
        parser.add_argument("--top", action="store_true", help="Scrape top tweets",)

        args = parser.parse_args()

        USER_UNAME = args.user
        USER_PASSWORD = args.password

        # if there is no declaration in file or in the command of the login
        if USER_UNAME is None:
            USER_UNAME = input("Twitter Username: ")

        if USER_PASSWORD is None:
            USER_PASSWORD = getpass.getpass("Enter Password: ")

        # blank line space
        print()

        tweet_type_args = []

        if args.username is not None:
            tweet_type_args.append(args.username)
        if args.hashtag is not None:
            tweet_type_args.append(args.hashtag)
        if args.query is not None:
            tweet_type_args.append(args.query)

        additional_data: list = args.add.split(",")

        # to search only by one of those
        if len(tweet_type_args) > 1:
            print("Please specify only one of --username, --hashtag, or --query.")
            sys.exit(1)

        # to search only by the top or the latest
        if args.latest and args.top:
            print("Please specify either --latest or --top. Not both.")
            sys.exit(1)

        # the scraping
        if USER_UNAME is not None and USER_PASSWORD is not None:
            scraper = Twitter_Scraper(username=USER_UNAME, password=USER_PASSWORD,)

            scraper.login()

            scraper.scrape_tweets(
                max_tweets=args.tweets,
                scrape_username=args.username,
                scrape_hashtag=args.hashtag,
                scrape_query=args.query,
                scrape_latest=args.latest,
                scrape_top=args.top,
                scrape_poster_details="pd" in additional_data,
            )
            scraper.save_to_csv() #saving to csv by function in twitter_scraper.py
            if not scraper.interrupted:
                scraper.driver.close()
        else:
            print("Missing Twitter username or password environment variables. Please check your .env file.")
            sys.exit(1)
    # there was an error in the commands
    except KeyboardInterrupt:
        print("\nScript Interrupted by user. Exiting...")
        sys.exit(1)
    # other errors
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

    sys.exit(1)


if __name__ == "__main__":
    main()
