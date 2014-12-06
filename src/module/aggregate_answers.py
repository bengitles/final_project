import csv
import numpy as np
import sys

from sklearn.neighbors import NearestNeighbors


def import_answers(filename):
  feature_questions = ['Answer.E1a', 'Answer.E1b', 'Answer.J1', 'Answer.N1a', 'Answer.N1b', 
                       'Answer.N2a', 'Answer.N2b', 'Answer.N3a', 'Answer.N3b', 'Answer.N4a', 
                       'Answer.N4b', 'Answer.N4f', 'Answer.N4f1', 'Answer.N4g', 'Answer.P4a', 
                       'Answer.P4b', 'Answer.P6', 'Answer.P6a1', 'Answer.X13', 'Answer.X13a']
  control_questions = {'Answer.Z1control1' : 'No' , 'Answer.Z1control2' : 'Bark', 
                       'Answer.Z1control3' : 'Agree strongly', 'Answer.Z1control4' : 'Meow', 
                       'Answer.Z1control5' : 'Cut out entirely', 'Answer.Z1control7' : '33', 
                       'Answer.Z1control8' : '222'}
  
  dict_reader = csv.DictReader(open(filename, 'rb'), delimiter=',')
  dict_reader.next()
  X = []
  for row in dict_reader:
    # golden set check
    golden_answers = [row[a] for a in control_questions.keys()]
    if set(golden_answers) != set(control_questions.itervalues()):
      continue

    result = []

    # E1a
    answer_e1a = row['Answer.E1a']
    possible_e1a_answers = ['Extremely liberal', 'Liberal', 'Slightly liberal', 'Moderate; middle of the road',
                            'Slightly conservative', 'Conservative', 'Extremely conservative']

    result.append(possible_e1a_answers.index(answer_e1a) - 3)

    # E1b
    if row['Answer.E1b'] == 'Liberal':
      result.append(0)
    else:
      result.append(1)

    # J1
    party_affil = row['Answer.J1']
    if party_affil == 'Democrat':
      result.append(-1)
    elif party_affil == 'Republican':
      result.append(1)
    else:
      result.append(0)

    # N1a and N1b
    N_ans = [('Answer.N1a', 'Answer.N1b'), ('Answer.N2a', 'Answer.N2b'), ('Answer.N3a', 'Answer.N3b'), ('Answer.N4a', 'Answer.N4b')]
    importance_list = ['Not important at all', 'Not too important', 'Somewhat important', 'Very important', 'Extremely important']

    for (a, b) in N_ans:
      if row[a].startswith('1'):
        result.append(1)
      elif row[a].startswith('7'):
        result.append(7)
      else:
        result.append(int(row[a]))

      result.append(importance_list.index(row[b]))


    # N4f and N4f1
    n4f_ans = row['Answer.N4f']
    if n4f_ans == 'Favor':
      result.append(1)
    elif n4f_ans == 'Oppose':
      result.append(2)
    else:
      result.append(3)

    n4f1_ans = row['Answer.N4f1']
    if n4f1_ans == 'A great deal':
      result.append(1)
    elif n4f1_ans == 'Moderately':
      result.append(2)
    else:
      result.append(3)

    # N4g
    modified_importance_list = ['Not important at all', 'Slightly important', 'Moderately important', 'Very important', 'Extremely important']

    result.append(modified_importance_list.index(row['Answer.N4g']))

    # P4a and b
    a = 'Answer.P4a'
    if row[a].startswith('1'):
      result.append(1)
    elif row[a].startswith('7'):
      result.append(7)
    elif row[a] == '':
      result.append(0)
    else:
      result.append(int(row[a]))
    result.append(importance_list.index(row['Answer.P4b']))

    # P6 (gun control)
    p6_ans = row['Answer.P6']
    if p6_ans == 'More difficult':  # negative bc democratic stance
      result.append(-1)
    elif p6_ans == 'Make it easier':
      result.append(1)
    else:
      result.append(0)
    result.append(importance_list.index(row['Answer.P6a1']))

    # X13 (Homesexuality)
    x13_ans = row['Answer.X13']
    if x13_ans == 'Favor':
      result.append(-1)
    else:
      result.append(1)

    x131_ans = row['Answer.X13a']
    if x131_ans == 'Strongly':
      result.append(1)
    else:
      result.append(0)

    X.append(result)

  return X

def k_nearest_neighbors(X):
  nbrs = NearestNeighbors(n_neighbors=3, algorithm='ball_tree').fit(X)  # unsupervised learning
  distances, indices = nbrs.kneighbors(X)


if __name__ == '__main__':
  X = import_answers(sys.argv[1])
  X = np.asarray(X)
  k_nearest_neighbors(X) 