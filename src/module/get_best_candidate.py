import csv
import numpy as np
import sys

from itertools import permutations

def get_candidates(filename):
  dict_reader = csv.DictReader(open(filename, 'rU'), delimiter=',')
  #dict_reader.next()
  master_list = [{'defense spending position': 3, 'uuid': 0, 'Party affiliation': 'Other', 
  'Govt and jobs position': 4, 'healthcare position': 4, 'Gun control position': 4, 'ideology': 
  'Slightly liberal'}, {'defense spending position': 2, 'uuid': 1, 'Party affiliation': 'Democrat',
   'Govt and jobs position': 3, 'healthcare position': 2, 'Gun control position': 1, 'ideology': 'Liberal'}
, {'defense spending position': 4, 'uuid': 2, 'Party affiliation': 'Republican', 'Govt and jobs position': 5, 'healthcare position': 6, 'Gun control position': 4, 'ideology': 'Slightly conservative'}, 
   {'defense spending position': 4, 'uuid': 3, 'Party affiliation': 'Other', 'Govt and jobs position': 4, 'healthcare position': 3, 'Gun control position': 4, 'ideology': 'Slightly liberal'}, 
   {'defense spending position': 4, 'uuid': 4, 'Party affiliation': 'Republican', 'Govt and jobs position': 6, 'healthcare position': 6, 'Gun control position': 4, 'ideology': 'Slightly conservative'}, 
   {'defense spending position': 2, 'uuid': 5, 'Party affiliation': 'Democrat', 'Govt and jobs position': 2, 'healthcare position': 2, 'Gun control position': 1, 'ideology': 'Liberal'}]
  candidate_dict = {}
  pairwise_matrix = np.zeros(shape=(6, ))

  for row in dict_reader:
    # quality control
    golden_question = row['what_sound_does_a_kitty_cat_make']
    health_a = row['which_statement_would_candidate_a_agree_with_more']
    A_health_preference = int(row['healthcare_a'])

    if golden_question != 'meow':
      continue
    if A_health_preference == 4 and health_a != 'Candidate A would be indifferent between the two statements above.':
      continue
    if A_health_preference <= 3  and health_a != 'The government should provide health care for all citizens.':
      continue
    if A_health_preference > 4 and health_a != 'All citizens should purchase private health insurance.':
      continue

    # aggregation
    a = int(row['uuid_a'])
    b = int(row['uuid_b'])
    print '----'
    fav_candidate = row['vote_for_your_preferred_candidate'][-1].lower()
    fav_candidate = row['uuid_' + fav_candidate]

    print a
    print b
    if int(fav_candidate) == a:
      pairwise_matrix[a][b] += 1
    else:
      pairwise_matrix[b][a] += 1

    if fav_candidate not in candidate_dict:
      candidate_dict[fav_candidate] = 0
    candidate_dict[fav_candidate] += 1

  print pairwise_matrix
  return candidate_dict


if __name__ == '__main__':
  candidates = get_candidates(sys.argv[1])
  print (candidates)

