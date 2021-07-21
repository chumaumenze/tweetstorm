#!/usr/bin/env python3

import importlib
import unittest

try:
    import tweetstorm_generator as tweetstorm
except ImportError:
    loader = importlib.machinery.SourceFileLoader('tweetstorm', './tweetstorm-generator')
    spec = importlib.util.spec_from_loader('tweetstorm', loader)
    tweetstorm = importlib.util.module_from_spec(spec)
    loader.exec_module(tweetstorm)


class TestTweetstormGenerator(unittest.TestCase):

    def setUp(self) -> None:
        self.files = [
            "test_data/softu-vsmall.txt",
            "test_data/softu-small.txt",
            "test_data/softu-medium.txt",
            "test_data/hippocratic-large.txt",
            "test_data/softu-vlarge.txt",
            "test_data/softu-xxxlarge.txt"
        ]

    @staticmethod
    def reassemble_tweets_to_corpus(tweets: list[str]):
        corpus = ""
        for i, tweet in enumerate(tweets):
            prefix = f"{i+1}/{len(tweets)}"
            corpus += tweet.replace(prefix, "", 1)
        return corpus.strip()

    def test_tweetstorm_with_empty_string(self):
        expected_tweets = [""]
        corpus = ""
        tweets = tweetstorm.make_tweetstorm(corpus, page_all=False)
        self.assertEqual(tweets, expected_tweets)

    def test_tweetstorm_with_long_words(self):
        corpus = (
            "The longest words in the dictionary are: "
            "antidisestablishmentarianism - opposition to the disestablishment "
            "of the Church of England - 28 letters. "
            "floccinaucinihilipilification - the estimation of something as "
            "worthless - 29 letters. pneumonoultramicroscopicsilicovolcanoconiosis "
            "- a supposed lung disease - 45 letters."
        )
        tweets = tweetstorm.make_tweetstorm(corpus, page_all=False)
        for tweet in tweets:
            err_msg = f'\nCharLimitExceeded:\n"{tweet}"'
            self.assertLessEqual(
                len(tweet), tweetstorm.TWITTER_CHAR_LIMIT, msg=err_msg)

        re_corpus = self.reassemble_tweets_to_corpus(tweets)
        self.assertEqual(re_corpus, corpus)

    def test_tweetstorm_with_xxx_long_words(self):
        xxlong_word = (
            "methionylthreonylthreonylglutaminylalanylprolylthreonyl"
            "phenylalanylthreonylglutaminylprolylleucylglutaminylserylvalyl"
            "valylvalylleucylglutamylglycylserylthreonylalanylthreonyl"
            "phenylalanylglutamylalanylhistidylisoleucylserylglycyl"
            "phenylalanylprolylvalylprolylglutamylvalylseryltryptophyl"
            "phenylalanylarginylaspartylglycylglutaminylvalylisoleucyl"
            "serylthreonylserylthreonylleucylprolylglycylvalylglutaminyl"
            "isoleucylserylphenylalanylserylaspartylgl"
        )
        corpus = f"The chemical composition of titin, the largest known protein is {xxlong_word}"
        err_msg = f'Word too long to be presented: "{xxlong_word}"'
        with self.assertRaises(OverflowError) as e:
            tweetstorm.make_tweetstorm(corpus, page_all=False)
            self.assertEqual(e.exception, err_msg)

    def test_tweetstorm_with_compund_sentence(self):
        corpus = (
            "This is your last chance. After this, there is no turning back. "
            "You take the blue pill—the story ends, you wake up in your bed "
            "and believe whatever you want to believe. You take the red "
            "pill—you stay in Wonderland, and I show you how deep the rabbit "
            "hole goes. Remember: all I'm offering is the truth. Nothing more."
        )
        tweets = tweetstorm.make_tweetstorm(corpus, page_all=False)
        for tweet in tweets:
            err_msg = f'\nCharLimitExceeded:\n"{tweet}"'
            self.assertLessEqual(
                len(tweet), tweetstorm.TWITTER_CHAR_LIMIT, msg=err_msg)

        re_corpus = self.reassemble_tweets_to_corpus(tweets)
        self.assertEqual(re_corpus, corpus)

    def test_tweetstorm_with_corpus(self):
        for file in self.files:
            with open(file) as f:
                corpus = f.read()

            tweets = tweetstorm.make_tweetstorm(corpus, page_all=False)
            for tweet in tweets:
                err_msg = f'\nCharLimitExceeded: {file}\n"{tweet}"'
                self.assertLessEqual(
                    len(tweet), tweetstorm.TWITTER_CHAR_LIMIT, msg=err_msg)


if __name__ == '__main__':
    unittest.main()
