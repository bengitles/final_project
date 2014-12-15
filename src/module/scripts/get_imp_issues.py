import csv
import matplotlib.pyplot as plt
import operator
import numpy as np
import pandas as pd

questions = ['Answer.N1b', 'Answer.N1e', 'Answer.N2b', 'Answer.N2e', 'Answer.N3b',
			 'Answer.N3e', 'Answer.N3g', 'Answer.N4b', 'Answer.N4e', 'Answer.N4g',
			 'Answer.N5b1','Answer.P4b', 'Answer.P4e','Answer.P6a1', 'Answer.P7b',
			 'Answer.X8a']

issues = ['Govt Services', 'Increase Govt Services', 'Defense Spending', 'Increase Defense Spending', 
					'Health care', 'Drugs for Seniors', 'Universal Healthcare', 'Govt and Jobs', 'Illegal Immigration',
					'Immigration Citizenship', 'Race Relations', 'Environment and Jobs', 'Global Warming', 'Gun control',
					'Women', 'Religion']

question_to_issue_map = dict(zip(questions, issues))

	#Open-ended importantces qs: 01OpenEndedQ1, 01OpenEndedQ2, 01OpenEndedQ3, 01OpenEndedQ4
control_questions = {'Answer.Z1control1' : 'No' , 'Answer.Z1control2' : 'Bark', 
                       'Answer.Z1control3' : 'Agree strongly', 'Answer.Z1control4' : 'Meow', 
                       'Answer.Z1control5' : 'Cut out entirely', 'Answer.Z1control7' : '33', 
                       'Answer.Z1control8' : '222'}

def get_importance(filename):
	dict_reader = csv.DictReader(open(filename, 'rb'), delimiter=',')
	importances = [[0 for x in range(5)]for x in range(len(questions))]
	for row in dict_reader:
		# golden set check
	    golden_answers = [row[a] for a in control_questions.keys()]
	    if set(golden_answers) == set(control_questions.itervalues()):		
			for i in range(len(questions)):
				imp = row[questions[i]]
				if imp == 'Not important at all':
					importances[i][0] += 1
				elif imp == 'Not too important' or imp == 'Slightly important':
					importances[i][1] += 1
				elif imp == 'Somewhat important' or imp == 'Moderately important':
					importances[i][2] += 1
				elif imp == 'Very important':
					importances[i][3] += 1
				elif imp == 'Extremely important':
					importances[i][4] += 1
	return importances

imp1 = get_importance('Batch_951674_batch_results.csv')
imp2 = get_importance('Batch_951779_batch_results.csv')
imp3 = get_importance('Batch_952287_batch_results.csv')
imp_total = [[0 for x in range(5)]for x in range(len(questions))]
scores = {}
for q in questions:
	scores[q] = 0
for i in range(len(questions)):
	print "Question: " + questions[i]
	for j in range(5):
		imp_total[i][j] += imp1[i][j]
		imp_total[i][j] += imp2[i][j]
		imp_total[i][j] += imp3[i][j]
		scores[questions[i]] += j * imp_total[i][j]
		print str(j) + ": " + str(imp_total[i][j])
	print "Score: " + str(scores[questions[i]])

sorted_scores = sorted(scores.items(), key=operator.itemgetter(1))

sorted_scores = [(question_to_issue_map[k], v) for k, v in sorted_scores]

# N = np.arange(len(sorted_scores))
# vals = [d[1] for d in sorted_scores]
# questions = [d[0] for d in sorted_scores]
# width = 0.35       # the width of the bars
# fig, ax = plt.subplots()
# rects1 = ax.bar(N, vals, width)
# ax.set_ylabel('Scores')
# ax.set_title('Importance score across features')
# ax.set_xticks(N+width)
# ax.set_xticklabels(tuple(questions), size = '8')
# plt.show()
# print sorted_scores
change = [d[1] for d in sorted_scores]
city = [d[0] for d in sorted_scores]
grad = pd.DataFrame({'change' : change, 'city': city})
plt.figure(figsize=(3, 8))

change = grad.change[grad.change > 0]
city = grad.city[grad.change > 0]
pos = np.arange(len(change))

plt.title('Importance Score over Various Features')
plt.barh(pos, change)

#add the numbers to the side of each bar
for p, c, ch in zip(pos, city, change):
    plt.annotate(str(ch), xy=(ch + 1, p + .5), va='center')

#cutomize ticks
ticks = plt.yticks(pos + .5, city)
xt = plt.xticks()[0]
plt.xticks(xt, [' '] * len(xt))

#minimize chartjunk
#remove_border(left=False, bottom=False)
plt.grid(axis = 'x', color ='white', linestyle='-')

#set plot limits
plt.ylim(pos.max() + 1, pos.min() - 1)
plt.xlabel('Importance Score')
plt.xlim(0, 3000)
plt.show()