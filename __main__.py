from __future__ import division
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
import sys
import PositionRank
import evaluation
import process_data
import os
from os.path import isfile, join
from nltk.stem.porter import PorterStemmer
porter_stemmer = PorterStemmer()

def process(args):


    # initialize the evaluation metrics vectors
    P, R, F1 = [0] * args.topK, [0] * args.topK, [0] * args.topK
    Rprec = 0.0
    bpref = 0.0

    docs = 0

    files = [f for f in os.listdir(args.input_data) if isfile(join(args.input_data, f))]

    for filename in files:

        print filename
        # if doc has passed the criteria then we save its text and gold
        text = process_data.read_input_file(args.input_data + filename)
        gold = process_data.read_gold_file(args.input_gold + filename)

        if text and gold:
            gold_stemmed = []
            for keyphrase in gold:
                keyphrase = [porter_stemmer.stem(w) for w in keyphrase.lower().split()]
                gold_stemmed.append(' '.join(keyphrase))
            # count the document
            docs += 1

            system = PositionRank.PositionRank(text, args.window, args.phrase_type)

            system.get_doc_words()

            system.candidate_selection()

            system.candidate_scoring(update_scoring_method=False)

            currentP, currentR, currentF1 =\
                evaluation.PRF_range(system.get_best_k(args.topK), gold_stemmed, k=args.topK)

            Rprec += evaluation.Rprecision(system.get_best_k(args.topK), gold_stemmed,
                                           k=len(gold_stemmed))

            bpref += evaluation.Bpref(system.get_best_k(args.topK), gold_stemmed)

            P = map(sum, zip(P, currentP))
            R = map(sum, zip(R, currentR))
            F1 = map(sum, zip(F1, currentF1))
            print 'docs', docs

    print 'docs', docs

    P = [p / docs for p in P]
    R = [r / docs for r in R]
    F1 = [f / docs for f in F1]

    # print 'Rprecision =', Rprec / docs
    # print 'Bpref', bpref / docs
    print 'Evaluation metrics:'.ljust(20, ' '), 'Precision @k'.ljust(20, ' '), 'Recall @k'.ljust(20, ' '), 'F1-score @k'

    for i in range(0, args.topK):
        print ''.ljust(20, ' '), \
            'Pr@{}'.format(i + 1).ljust(6, ' '), '{0:.3f}'.format(P[i]).ljust(13, ' '), \
            'Re@{}'.format(i + 1).ljust(6, ' '), '{0:.3f}'.format(R[i]).ljust(13, ' '), \
            'F1@{}'.format(i + 1).ljust(6, ' '), '{0:.3f}'.format(F1[i])


def main():
  parser = ArgumentParser("PositionRank",
                          formatter_class=ArgumentDefaultsHelpFormatter,
                          conflict_handler='resolve')

  parser.add_argument('--input_data', nargs='?', required=True,
                      help='Directory with text documents')

  parser.add_argument('--input_gold', nargs='?', required=True,
                      help='Directory with documents containing the gold')

  parser.add_argument('--topK', default=10, type=int,
                      help='Top k predicted')

  parser.add_argument('--window', default=10, type=int,
                      help='Window used to add edges in the graph')

  parser.add_argument('--phrase_type', default='n_grams',
                      help='If you want n-grams or noun phrases')

  args = parser.parse_args()


  process(args)


if __name__ == "__main__":
  sys.exit(main())