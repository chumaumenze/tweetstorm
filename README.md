# LL Tweetstorm

## The mission

-----

Create a program that receives a text of arbitrary length and creates a tweetstorm with it, using as much space in each tweet as possible, and avoinding to break words between tweets.

### Constraints:

1. Each tweet can't be over **280** characters;
2. Each tweet must be prefixed with the *current tweet index / total count of tweets*;
3. We'll call your program from a Unix shell, like `/opt/hiring/yourname/tweetstorm-generator`, with the text corpus passed as a parameter;
4. You can choose any language, but stick to its built-in library (if you think you need a third-party lib to achieve this, we're curious to know what that would be).

## Solution

This program requires `>=python3.6`.

### Steps

- Define constants for character limit, prefix buffer, text phrase limit.
- Breakdown the text by paragraphs
- For each paragraph, parse word and concatenate to for tweet (phrases within text phrase limit and <= 280 chars)
- Append phrases to thread bucket (an array of tweets)
- Paginate array of tweets
- Finally, on `main()`, using `argparse` accept corpus from CLI and pass to `make_tweetstorm()`

### Assumptions

1. Due to constraint (2), as defined above, even empty string outputs with pagination. This can be disable by passing `page_all=False`. 
1. Text corpus has a defined limit. Tested with upto 9.8 million characters.
1. Each tweet can't be over **280** characters but can be **less than** 280 characters.
1. Extremely long word will cause an `Overflow("Word too long to be presented")` exception.


### Testing

The test suit uses corpus upto 9.8 million characters. These files are in `test_data/`. To execute the test suite, run:

```shell
python test_tweetstorm_generator.py
```