import csv
import numpy as np
import sys

def get_candidates(filename):
  dict_reader = csv.DictReader(open(filename, 'rU'), delimiter=',')
  #dict_reader.next()
  candidate_dict = {}

  for row in dict_reader:
    # quality control
    # golden_question = row['golden_question']
    # health_a = row['health_a']

    # if health_a == '1' and golden_question != 'TRUE':
    #   continue
    # if health_a != '1' and golden_question == 'TRUE':
    #   continue

    # aggregation

    fav_candidate = row['favorite_candidate'].lower()
    political_ideology = row['ideology_' + fav_candidate]
    if political_ideology not in candidate_dict:
      candidate_dict[political_ideology] = 0
    candidate_dict[political_ideology] += 1

  return candidate_dict


if __name__ == '__main__':
  candidates = get_candidates(sys.argv[1])
  print candidates

