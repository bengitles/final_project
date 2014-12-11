import csv
import operator

questions = ['Answer.N1b', 'Answer.N1e', 'Answer.N2b', 'Answer.N2e', 'Answer.N3b',
			 'Answer.N3e', 'Answer.N3g', 'Answer.N4b', 'Answer.N4e', 'Answer.N4g',
			 'Answer.N5b1','Answer.P4b', 'Answer.P4e','Answer.P6a1', 'Answer.P7b',
			 'Answer.X8a']
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
print sorted_scores