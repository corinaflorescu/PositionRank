#! /usr/bin/env python
# -*- coding: utf-8 -*-

from doc_candidates import LoadFile
import networkx as nx


class PositionRank(LoadFile):

    def __init__(self, input_text, window, phrase_type):
        """ Redefining initializer for PositionRank. """

        super(PositionRank, self).__init__(input_text=input_text)

        self.graph = nx.Graph()
        """ The word graph. """
        self.window = window

        self.phrase_type = phrase_type

    def build_graph(self, window, pos=None):
        """
        build the word graph

        :param window: the size of window to add edges in the graph
        :param pos: he part of speech tags used to select the graph's nodes
        :return:
        """

        if pos is None:
            pos = ['NN', 'NNS', 'NNP', 'NNPS', 'JJ']

        # container for the nodes
        seq = []

        # select nodes to be added in the graph
        for el in self.words:
            if el.pos_pattern in pos:
                seq.append((el.stemmed_form, el.position, el.sentence_id))
                self.graph.add_node(el.stemmed_form)

        # add edges
        for i in range(0, len(seq)):
            for j in range(i+1, len(seq)):
                if seq[i][1] != seq[j][1] and abs(j-i) < window:
                    if not self.graph.has_edge(seq[i][0], seq[j][0]):
                        self.graph.add_edge(seq[i][0], seq[j][0], weight=1)
                    else:
                        self.graph[seq[i][0]][seq[j][0]]['weight'] += 1

    def candidate_selection(self, pos=None, phrase_type='n_grams'):
        """
        the candidates selection for PositionRank
        :param pos: pos: the part of speech tags used to select candidates
        :return:
        """

        if pos is None:
            pos = ['NN', 'NNS', 'NNP', 'NNPS', 'JJ']

        # uncomment the line below if you wish to extract ngrams instead of the longest phrase
        if phrase_type=='n_grams':
            self.get_ngrams(n=4, good_pos=pos)
        else:
            # select the longest phrase as candidate keyphrases
            self.get_phrases(self, good_pos=pos)

    def candidate_scoring(self, pos=None, window=10, update_scoring_method=False):
        """
        compute a score for each candidate based on PageRank algorithm
        :param pos: the part of speech tags
        :param window: window size
        :param update_scoring_method: if you want to update the scoring method based on my paper cited below:
        Florescu, Corina, and Cornelia Caragea. "A New Scheme for Scoring Phrases in Unsupervised Keyphrase Extraction."
         European Conference on Information Retrieval. Springer, Cham, 2017.

        :return:
        """

        if pos is None:
            pos = ['NN', 'NNS', 'NNP', 'NNPS', 'JJ']

        # build the word graph
        self.build_graph(window=window, pos=pos)

        # filter out canditates that unlikely to be keyphrases
        self.filter_candidates(max_phrase_length=4, min_word_length=3, valid_punctuation='-.')

        # compute the personalization values
        # each word is weighted with 1/position_in_the_doc
        # the weights are normalized before being used in the algorithm
        personalization = {}
        for w in self.words:
            stem = w.stemmed_form
            poz = w.position
            pos = w.pos_pattern

            if pos in pos:
                if stem not in personalization.keys():
                    personalization[stem] = 1.0/poz
                else:
                    personalization[stem] = personalization.get(stem)+1.0/poz

        factor = 1.0 / sum(personalization.itervalues())

        normalized_personalization = {k: v * factor for k, v in personalization.iteritems()}

        # compute the word scores using personalized random walk
        pagerank_weights = nx.pagerank_scipy(self.graph, personalization=normalized_personalization, weight='weight')


        # loop through the candidates
        if update_scoring_method:
            for c in self.candidates:
                if len(c.stemmed_form.split()) > 1:
                    # for arithmetic mean
                    #self.weights[c.stemmed_form] = [stem.stemmed_form for stem in self.candidates].count(c.stemmed_form) * \
                                                   #sum([pagerank_weights[t] for t in c.stemmed_form.split()]) \
                                                   #/ len(c.stemmed_form.split())
                    # for harmonic mean
                    self.weights[c.stemmed_form] = [stem.stemmed_form for stem in self.candidates].count(c.stemmed_form) * \
                                                   len(c.stemmed_form.split()) / sum([1.0 / pagerank_weights[t] for t in c.stemmed_form.split()])
                else:
                    self.weights[c.stemmed_form] = pagerank_weights[c.stemmed_form]
        else:
            for c in self.candidates:
                self.weights[c.stemmed_form] = sum([pagerank_weights[t] for t in c.stemmed_form.split()])



