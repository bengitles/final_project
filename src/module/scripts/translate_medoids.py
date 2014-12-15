import ast
import csv 
import sys

from itertools import permutations

feature_names = ['ideology', 'Liberal or not', 'Party affiliation', 'defense spending position', 'healthcare position',  'Govt and jobs position', 'Gun control position']

def translate(input_file):
  f = open(input_file, 'r')
  f.next()  
  dictionary_lst = []
  for line in f:
    line = line.replace("  ", " ")
    line = line.replace(" ", ",")
    lst = ast.literal_eval(line)
    
    zipped_dict = dict(zip(feature_names, lst))
    dictionary_lst.append(zipped_dict)

  candidate_id = 0
  for d in dictionary_lst:
    for (k, v) in d.iteritems():

      # translation
      if k == 'ideology':
        possible_e1a_answers = ['Extremely liberal', 'Liberal', 'Slightly liberal', 'Moderate; middle of the road',
                            'Slightly conservative', 'Conservative', 'Extremely conservative']
        d[k] = possible_e1a_answers[v + 3]

      if k == 'Party affiliation':
        if v == -1:
          d[k] = 'Democrat'
        elif v == 1:
          d[k] = 'Republican'
        else:
          d[k] = 'Other'

      if k == 'Gun control position':
          if v == -1:
            d[k] = 1
          elif v == 1:
            d[k] == 7
          else:
            d[k] = 4

    d['uuid'] = candidate_id  # unique candidate identifier
    candidate_id += 1

    d.pop('Liberal or not', None)  # used in ML model -- not needed anymore
    
  print dictionary_lst
  return dictionary_lst  



def write_to_output(output_file, features):
  with open(output_file, 'w') as csvfile:
    header = ['uuid_A', 'Ideology_A', 'Party_affiliation_A', 'defense_A', 'healthcare_A',  'govt_jobs_A', 'gun_control_A', 'uuid_B', 'Ideology_B', 'Party_affiliation_B', 'defense_B', 'healthcare_B',  'govt_jobs_B', 'gun_control_B']
    writer = csv.DictWriter(csvfile, fieldnames = header)
    writer.writeheader()

    for subset in permutations(range(len(features)), 2):
      temp_d = {k : None for k in header}
      
      # A
      A = features[subset[0]]
      B = features[subset[1]]

      temp_d['uuid_A'] = A['uuid']
      temp_d['Ideology_A'] = A['ideology']
      temp_d['Party_affiliation_A'] = A['Party affiliation']
      temp_d['defense_A'] = A['defense spending position']
      temp_d['healthcare_A'] = A['healthcare position']
      temp_d['govt_jobs_A'] = A['Govt and jobs position']
      temp_d['gun_control_A'] = A['Gun control position']

      temp_d['uuid_B'] = B['uuid']
      temp_d['Ideology_B'] = B['ideology']
      temp_d['Party_affiliation_B'] = B['Party affiliation']
      temp_d['defense_B'] = B['defense spending position']
      temp_d['healthcare_B'] = B['healthcare position']
      temp_d['govt_jobs_B'] = B['Govt and jobs position']
      temp_d['gun_control_B'] = B['Gun control position']

      writer.writerow(temp_d)

if __name__ == '__main__':
  input_file = sys.argv[1]
  output_file = sys.argv[2]

  translated_features = translate(input_file)

  write_to_output(output_file, translated_features)