import json
import statsmodels.stats.inter_rater as stats
import sys


# Function that calculates the maximum amount of evaluations for all the videos. It also returns the amount
# of excluded evaluations in the dataset
def get_max_evaluations(dict):
    maxT = 0
    count = 0
    for val in dict.keys():
        tot = dict[val]['total']
        if maxT < tot:
            maxT = tot
        if dict[val]['total'] < 3:
            count += 1
    return maxT, count


# Function that computes the weighted sum of kappas to obtain the overall kappa
def compute_weighted_kappa(dict):
    randolph, fleiss = 0, 0
    for key in dict.keys():
        randolph += dict[key]['value_randolph'] * dict[key]['weight']
        fleiss += dict[key]['value_fleiss'] * dict[key]['weight']
    return randolph, fleiss


# Function that returns the class to which the given nominal class belongs
def group_difficulty(nominal, classes):
    difs = ['VeryEasy', 'Easy', 'Intermediate', 'Difficult', 'VeryDifficult']
    index = difs.index(nominal)
    if classes == 2:
        if index > 1:
            return 'Difficult'
        else:
            return 'Easy'
    else:
        return nominal


# Get the number of classes by input
classes = int(sys.argv[1])

# Evaluations load from json file, generated from MongoDB export
transcriptFile = open('../InitialData/evaluations_new.json', 'r')
lines = transcriptFile.read()
data = json.loads(lines)

matrix_dict = {}

# Iterate user and extract evaluations
for user in data:
    evals = user['evaluations']
    for ev in evals:
        videoID = ev['videoId']
        difficulty = ev['difficulty']
        difficulty = group_difficulty(difficulty, classes)
        if videoID not in matrix_dict.keys():
            matrix_dict[videoID] = {}
            matrix_dict[videoID][difficulty] = 1
            matrix_dict[videoID]['total'] = 1
        else:
            if difficulty not in matrix_dict[videoID]:
                matrix_dict[videoID][difficulty] = 1
            else:
                matrix_dict[videoID][difficulty] += 1
            matrix_dict[videoID]['total'] += 1

transcriptFile.close()

# Evaluations load from json file, generated from MongoDB export
transcriptFile = open('../InitialData/evaluations27-04-2018.json', 'r')
lines = transcriptFile.read()
data = json.loads(lines)

for user in data:
    evals = user['evaluations']
    for ev in evals:
        videoID = ev['resource']['id']
        difficulty = ev['resource']['evaluation'][0]['answer']['text']
        difficulty = group_difficulty(difficulty, classes)
        if videoID not in matrix_dict.keys():
            matrix_dict[videoID] = {}
            matrix_dict[videoID][difficulty] = 1
            matrix_dict[videoID]['total'] = 1
        else:
            if difficulty not in matrix_dict[videoID]:
                matrix_dict[videoID][difficulty] = 1
            else:
                matrix_dict[videoID][difficulty] += 1
            matrix_dict[videoID]['total'] += 1

transcriptFile.close()

# Evaluations load from json file, generated from MongoDB export
transcriptFile = open('../InitialData/evaluations_phase2.json', 'r')
lines = transcriptFile.read()
data = json.loads(lines)

for user in data:
    evals = user['evaluations']
    for ev in evals:
        videoID = ev['resource']['id']
        difficulty = ev['resource']['evaluation'][0]['answer']['text']
        difficulty = group_difficulty(difficulty, classes)
        if videoID not in matrix_dict.keys():
            matrix_dict[videoID] = {}
            matrix_dict[videoID][difficulty] = 1
            matrix_dict[videoID]['total'] = 1
        else:
            if difficulty not in matrix_dict[videoID]:
                matrix_dict[videoID][difficulty] = 1
            else:
                matrix_dict[videoID][difficulty] += 1
            matrix_dict[videoID]['total'] += 1

print len(matrix_dict)
print json.dumps(matrix_dict, sort_keys=True, indent=4)
transcriptFile.close()

hash = {}
difs = ['VeryEasy', 'Easy', 'Intermediate', 'Difficult', 'VeryDifficult']

i = 0
th, count = get_max_evaluations(matrix_dict)
ref = len(matrix_dict) - count
kappas = {}

matrix = []
for key in sorted(matrix_dict.keys()):
    if matrix_dict[key]['total'] == 1:
        hash[i] = key
        vals = []
        for dif in difs:
            if dif not in matrix_dict[key].keys():
                vals.append(0)
            else:
                vals.append(matrix_dict[key][dif])
        matrix.append(vals)

print "VIDEOS CON 1 EVAL: "+str(len(matrix))

matrix = []
for key in sorted(matrix_dict.keys()):
    if matrix_dict[key]['total'] == 2:
        hash[i] = key
        vals = []
        for dif in difs:
            if dif not in matrix_dict[key].keys():
                vals.append(0)
            else:
                vals.append(matrix_dict[key][dif])
        matrix.append(vals)

print "VIDEOS CON 2 EVALS: "+str(len(matrix))

# For every amount of qualifications the kappa is calculated
for sub in range(3, th + 1, 1):

    matrix = []
    for key in sorted(matrix_dict.keys()):
        if matrix_dict[key]['total'] == sub:
            hash[i] = key
            vals = []
            for dif in difs:
                if dif not in matrix_dict[key].keys():
                    vals.append(0)
                else:
                    vals.append(matrix_dict[key][dif])
            matrix.append(vals)

    if len(matrix) > 0:
        kappas[sub] = {}
        kappas[sub]['weight'] = float(len(matrix)) / float(ref)
        kappa = stats.fleiss_kappa(matrix, method='randolph')
        kappas[sub]['value_randolph'] = kappa
        kappa = stats.fleiss_kappa(matrix)
        kappas[sub]['value_fleiss'] = kappa

print json.dumps(kappas, sort_keys=True, indent=4)
randolph, fleiss = compute_weighted_kappa(kappas)
print 'OVERALL FLEISS KAPPA: ' + str(randolph)
print 'OVERALL RANDOLPH KAPPA: ' + str(fleiss)
