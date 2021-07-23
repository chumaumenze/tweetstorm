#!/usr/bin/env python

import math
import sys


MAX_MESSAGE_LENGTH = 280


def count_tweets(message):
    # how many tweets without prefix for a given message
    tweets_count = math.ceil(1.0 * len(message) / MAX_MESSAGE_LENGTH)
    # sum all prefixes chars
    total_prefix_length = sum(
        [len('%s/%s ' % (i + 1, int(tweets_count))) for i in range(int(tweets_count))]
    )

    total_length = total_prefix_length + len(message)

    return int(math.ceil(total_length * 1.0 / MAX_MESSAGE_LENGTH))


def tweets_generator(message):
    if len(message) <= MAX_MESSAGE_LENGTH:
        yield message
    else:
        # how many tweets?
        total_tweets = count_tweets(message)

        words = message.split(' ')
        idx = 1
        tweet = '{}/{}'.format(idx, total_tweets)
        while True:
            # using words as a stack
            tweet += ' ' + words.pop(0)

            # no more words left
            if len(words) == 0:
                break

            # tweet length + 1 space + next word length > MAX_MESSAGE_LENGTH
            if (len(tweet) + 1 + len(words[0])) > MAX_MESSAGE_LENGTH:
                yield tweet
                idx += 1
                tweet = '{}/{}'.format(idx, total_tweets)

        yield tweet


def main(*args):
    if len(args) > 1:
        message = ' '.join(args)
    else:
        message = args[0]

    for tweet in tweets_generator(message.strip()):
        print(tweet)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('''Usage:
            python tweetstorm-generator.py "<long message I want to tweet>"

            Ex:
            $ python tweetstorm-generator.py "You take the blue pill (...)"
        ''')
        sys.exit(1)
    print(sys.argv[1:])
    main(*sys.argv[1:])
