# Tweetstorm

## The mission

-----

Tweetsorm receives a text of arbitrary length and creates a Twitter thread from it, using as much space in each tweet as possible, and avoiding to break words between tweets.

### Specs:

1. Each tweet can't be over **280** characters (current tweet character limit).
2. Each tweet is prefixed with the *current tweet index / total count of tweets*.


### Steps

- Define constants for character limit, prefix buffer, text phrase limit.
- Breakdown the text by paragraphs
- For each paragraph, parse word and concatenate to for tweet (phrases within text phrase limit and <= 280 chars)
- Append phrases to thread bucket (an array of tweets)
- Paginate array of tweets
- Finally, on `main()`, using `argparse` accept corpus from CLI and pass to `make_tweetstorm()`

### Testing

The test suit uses corpus upto 9.8 million characters. These files are in `test_data/`. To execute the test suite, run:

```shell
python test_tweetstorm_generator.py
```
