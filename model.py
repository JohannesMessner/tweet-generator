import pandas as pd
import numpy as np
import json


def map_tokens_to_id(tokens):
    i = 0
    token_id_map = {}
    id_token_map = {}
    for token in tokens:
        if token not in token_id_map:
            token_id_map[token] = i
            id_token_map[i] = token
            i += 1
    return token_id_map, id_token_map


def calculate_probabilities(pre_model):
    model = {}
    for key in pre_model:
        # all the successors (=next tokens in the text) with associated counts, as a dict
        successors_and_counts = pre_model[key]
        successors = list(successors_and_counts.keys())  # only the successors without counts as a list
        # calculate how many successors a key has (= number of occurrences of the key in the corpus)
        tot_successor_count = np.sum([successors_and_counts[successor] for successor in successors_and_counts])
        # calculate the probability of occurring for each unique successor
        successor_probs = [successors_and_counts[successor] / tot_successor_count for successor in
                           successors_and_counts]
        # TODO: these probs need to sum up to 1. Does the np.rando.choice accept them if calculated like this?
        # for each key store which successors occur how frequently/likely
        model[key] = (successors, successor_probs)
    return model


class Model():
    degree = 0
    data_filename = ''
    padding_token = '§'
    model = None
    token_id_map = None
    id_token_map = None

    def __init__(self, degree, data_filename, padding_token='§'):
        self.degree = degree
        self.data_filename = data_filename
        self.padding_token = padding_token

    def initialize(self):
        # get tweets from disk
        df_tweets = pd.read_csv(self.data_filename)
        tweets = [tweet for tweet in df_tweets.iloc[:, 1]]
        df_tweets = None

        # split tweets into individual tokens (=words)
        padding = [self.padding_token for _ in range(self.degree)]  # for degree-gram-model
        tokenized_tweets = [padding + tweet.split() + padding for tweet in tweets]
        tokens = [token for tweet in tokenized_tweets for token in tweet]

        # assign an integer to each token for more efficient storing
        token_id_map, id_token_map = map_tokens_to_id(tokens)
        tokenized_tweets = [[token_id_map[token] for token in tweet] for tweet in tokenized_tweets]

        # build the actual model
        pre_model = {}  # model that count occurrences of tokens
        for tweet in tokenized_tweets:
            for i_token, token in enumerate(tweet):
                if i_token > len(tweet) - self.degree - 1:
                    break
                key = str(token)  # TODO: negates the savings from transforming string to ints...
                for i_deg in range(1, self.degree):
                    key += ' ' + str(tweet[i_token + i_deg])
                successor = tweet[i_token + self.degree]  # the token that follows after the token-tuple of length degree
                if key not in pre_model:
                    pre_model[key] = {}
                known_successors = pre_model[key]
                # count how often the successor occurs in the corpus
                known_successors[successor] = known_successors[successor] + 1 if successor in known_successors else 1
        self.model = calculate_probabilities(pre_model)
        self.token_id_map = token_id_map
        self.id_token_map = id_token_map

    def generate_tweet(self, maxlen=280):
        if self.model is None or self.token_id_map is None or self.id_token_map is None:
            return "Can't generate tweet. Model must be initialized first"

        tweet = ''
        padding = ((str(self.token_id_map[self.padding_token]) + ' ') * self.degree)[:-1]
        memory = padding  # how far back the model looks in time to generate words
        start_successors, start_probs = self.model[memory]  # beginning of the tweet
        next_id = np.random.choice(start_successors, p=start_probs)  # id of the next word, sampled from the model
        next_token = self.id_token_map[next_id]
        tweet += next_token
        while next_token != self.padding_token and len(tweet) <= maxlen:
            memory_list = memory.split()[1:] + [next_id]  # shift memory one token (word) forward
            memory = ''
            for id in memory_list:
                memory += str(id) + ' '
            memory = memory[:-1]
            successors, probs = self.model[memory]
            next_id = np.random.choice(successors, p=probs)
            next_token = self.id_token_map[next_id]
            tweet += ' ' + next_token
        return tweet[:-1]  # cut off padding token at the end


def main():
    m = Model(2, 'trump.csv')
    m.initialize()
    for _ in range(10):
        print(m.generate_tweet())


if __name__ == '__main__':
    main()