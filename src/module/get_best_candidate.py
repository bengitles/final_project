import csv
import numpy as np
import sys
import pandas as pd
from itertools import permutations
import matplotlib.pyplot as plt

pairwise_matrix = np.zeros(shape=(3, 3))

master_list = [{'defense spending position': 3, 'uuid': 0, 'Party affiliation': 'Other', 
  'Govt and jobs position': 4, 'healthcare position': 4, 'Gun control position': 4, 'ideology': 
  'Slightly liberal'}, {'defense spending position': 2, 'uuid': 1, 'Party affiliation': 'Democrat',
   'Govt and jobs position': 3, 'healthcare position': 2, 'Gun control position': 1, 'ideology': 'Liberal'}
  ,{'defense spending position': 4, 'uuid': 2, 'Party affiliation': 'Republican', 'Govt and jobs position': 5, 'healthcare position': 6, 'Gun control position': 4, 'ideology': 'Slightly conservative'}, 
   {'defense spending position': 4, 'uuid': 3, 'Party affiliation': 'Other', 'Govt and jobs position': 4, 'healthcare position': 3, 'Gun control position': 4, 'ideology': 'Slightly liberal'}, 
   {'defense spending position': 4, 'uuid': 4, 'Party affiliation': 'Republican', 'Govt and jobs position': 6, 'healthcare position': 6, 'Gun control position': 4, 'ideology': 'Slightly conservative'}, 
   {'defense spending position': 2, 'uuid': 5, 'Party affiliation': 'Democrat', 'Govt and jobs position': 2, 'healthcare position': 2, 'Gun control position': 1, 'ideology': 'Liberal'}]

def get_candidates(filename):
  dict_reader = csv.DictReader(open(filename, 'rU'), delimiter=',')
  #dict_reader.next()
  comment_list = []
  candidate_dict = {}
  state_count_dict = {}
  a_votes = 0
  b_votes = 0

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

    # store comment
    if row['explain_your_choice_optional']: 
      comment_list.append(row['explain_your_choice_optional'].lower()) 

    

    # aggregation
    a = int(row['uuid_a']) - 3
    b = int(row['uuid_b']) - 3
    fav_candidate = row['vote_for_your_preferred_candidate'][-1].lower()
    fav_candidate = row['uuid_' + fav_candidate]

    # store state counts
    state = row['_region']
    if state == '':
      pass
    else:
      if state not in state_count_dict and state != '':
        state_count_dict[state] = [0, 0, 0]
      state_count_dict[state][int(fav_candidate) - 3] += 1

    if int(fav_candidate) - 3 == a:
      a_votes += 1
      pairwise_matrix[a][b] += 1.0
    else:
      b_votes += 1
      pairwise_matrix[b][a] += 1.0

    if fav_candidate not in candidate_dict:
      candidate_dict[fav_candidate] = 0
    candidate_dict[fav_candidate] += 1

  print pairwise_matrix
  #plot_stacked_comparison(pairwise_matrix)
  #analyze_commments(comment_list)
  plot_state_distribution(state_count_dict)
  return candidate_dict

def plot_state_distribution(state_dict):
  test = []
  states = []
  for (k, v) in state_dict.iteritems():
    test.append(v)
    states.append(k)

  red, blue, grey = '#B2182B', '#2166AC', '#808080'
  test = np.array(test)
  ind = np.arange(len(states)) + ([1] * len(states))
  w = 0.25
  n = np.arange(1, len(states) + 1)
  plt.bar(n, test[:, 0], color=grey, label='Votes for independent', width = w)
  plt.bar(n, test[:, 1], bottom=test[:, 0], color = red, label='Votes for conservative', width = w)
  plt.bar(n, test[:, 2], bottom = test[:, 1] + test[:, 0], color = blue, label='Votes for liberal', width = w)
  plt.xticks(ind + w/2., states, rotation='horizontal')
  plt.yticks([0, 10, 20, 30, 40])
  plt.ylabel("Number of votes")
  plt.xlabel("States")
  plt.legend(loc='upper right')
  plt.title('Statewide Distribution of Votes')
  plt.show()

def analyze_commments(comment_field):
  key_words = ['gun', 'health', 'liberal', 'conservative', 'job', 'defense', 'spending', 'government']
  keyword_dict = {k : 1 for k in key_words}
  for c in comment_field:
    for k in key_words:
      if k in c:
        keyword_dict[k] += 1

  print keyword_dict

  change = [d[1] for d in keyword_dict.iteritems()]
  city = [d[0] for d in keyword_dict.iteritems()]
  grad = pd.DataFrame({'change' : change, 'city': city})
  plt.figure(figsize=(3, 8))

  change = grad.change[grad.change > 0]
  city = grad.city[grad.change > 0]
  pos = np.arange(len(change))

  plt.title('Word Frequency in Comments Section')
  plt.barh(pos, change)

  #add the numbers to the side of each bar
  for p, c, ch in zip(pos, city, change):
      plt.annotate(str(ch), xy=(ch + 1, p + .5), va='center')

  #cutomize ticks
  print city
  ticks = plt.yticks(pos + .5, city)
  xt = plt.xticks()[0]
  plt.xticks(xt, [' '] * len(xt))

  #minimize chartjunk
  #remove_border(left=False, bottom=False)
  plt.grid(axis = 'x', color ='white', linestyle='-')

  #set plot limits
  plt.ylim(pos.max() + 1, pos.min() - 1)
  plt.xlabel('Word Frequency in Comments')
  plt.xlim(0, 25)
  plt.show()
  

def compare_two_candidates(candidate_a, candidate_b):
  candidate_a_wins = pairwise_matrix[candidate_a][candidate_b]
  candidate_b_wins = pairwise_matrix[candidate_b][candidate_a]

  print candidate_a_wins
  a_win_percentage = float((candidate_a_wins) / (candidate_a_wins + candidate_b_wins)) * 100
  print "Candidate A with uuid {} won {} percent of the time against Candidate B with uuid {}".format(str(candidate_a), str(a_win_percentage), str(candidate_b)) 

def plot_stacked_comparison(test):
  red, blue, grey = '#B2182B', '#2166AC', '#808080'

  # test = [[0, 2, 1],
  #         [2, 0, 4],
  #         [1, 2, 0]]
  test = np.array(test)
  print test
  ind = np.arange(3) + [1, 1, 1]
  print ind
  width = 0.5
  plt.bar([1, 2, 3], test[:, 0], color=grey, label='Wins over independent', width = 0.5)
  plt.bar([1, 2, 3], test[:, 1], bottom=test[:, 0], color = red, label='Wins over conservative', width = 0.5)
  plt.bar([1, 2, 3], test[:, 2], bottom = test[:, 1] + test[:, 0], color = blue, label='Wins over liberal', width = 0.5)
  plt.xticks(ind + width/2., ['Neutral', 'Conservative', 'Liberal'], rotation='horizontal')
  plt.yticks([0, 10, 20, 30, 40, 50])
  plt.ylabel("Number of pairwise election wins")
  plt.xlabel("Candidates")
  plt.legend(loc='upper center')
  plt.title('Election Results')

  #normalize each row by transposing, normalizing each column, and un-transposing
  #test = (1. * tclass.T / tclass.T.sum()).T

  # plt.subplot(122)
  # plt.bar([0, 1, 2], tclass[0], color=red, label='Died')
  # plt.bar([0, 1, 2], tclass[1], bottom=tclass[0], color=blue, label='Survived')
  # plt.xticks([0.5, 1.5, 2.5], ['1st Class', '2nd Class', '3rd Class'], rotation='horizontal')
  # plt.ylabel("Fraction")
  # plt.xlabel("")
  # remove_border()

  plt.show()


if __name__ == '__main__':
  candidates = get_candidates(sys.argv[1])
  print sorted(candidates.iteritems(), key = lambda x : x[1])
  print compare_two_candidates(1, 0)
  #plot_stacked_comparison()
  #analyze_comments()
