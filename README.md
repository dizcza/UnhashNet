# Unhash MD5

MD5 cryptographic hash function is known to be insecure. Is it possible to predict (with non-negligible certainty) whether the hash starts with _'a'_ or _'b'_? If so, an attacker may train, for example, `N` classifiers to infer the most probable word candidates each of length `N-1` (or less) from a given wordlist, using the chain rule probability:

```P('qwerty') = P(x1='q') * P(x2='w') * P(x3='e') * P(x4='r') * P(x5='t') * P(x6='y') * P(x7='\0')```,

where each classifier is trained _independently_ to predict a positional character, thus making the most probable candidate composed of argmax of likelihoods for each letter.

Cryptographically insecure hash functions suffer from exploitation that people tend to use passwords from a vocabulary of (English) language. A classifier hardly converges if you train it on hashes of all `26^N` combinations of `N`-length English words, apart from waiting the age of Universe to complete the training. A much better approach is to test your idea against a preset of commonly used passwords. For our experiments, we will use the famous [rockyou](http://skullsecurity.org/wiki/index.php/passwords) list.

## Prerequisite

* Python 3.5+
* run `./download_rockyou.sh` in a terminal to prepare a dataset
* `pip install -r requirements.txt`

## Model definition

MD5 hash has a fixed length of 16 bytes. A naive approach is to treat the MD5 hash as a vector of 16 elements, ranging from 0x0 to 0xf, though you're not limited to expand your input vector with interesting combinations of byte pairs, since, of course, each byte depends on all other ones.

For a quick start, I used MLP `16 --> 100 --> 20 --> 2` to predict whether a hashed word starts with 'a' or 'b'. Train and test data come from 'rockyou.txt' list. Assuming, for simplicity, that each hash byte is taken from a uniform\[0, 15] distribution, each vector element is normalized to have a zero mean and unit variance.

## Results

Train and test accuracy of `0.6677` and `0.4983` respectively suggests that classifier is overfit and there is no statistical dependency between the MD5 hash and its first letter.