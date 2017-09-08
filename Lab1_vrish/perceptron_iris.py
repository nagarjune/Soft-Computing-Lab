from random import randrange
import csv 
 
# Load a CSV file
def load_csv(filename):
	dataset = list()
	with open(filename, 'r') as input1:
		reader =csv. reader(input1)
		for row in reader:
			dataset.append(row)
		dataset.pop(0)
	numrow = len(dataset)
	numcol = len(dataset[0])
	return dataset, numrow, numcol
 
 
#coverting the string into int
def number_classlabel(dataset):
	for i in range(100):
		for j in range(5):
			if (dataset[i][j] == 'Iris-setosa'):
				dataset[i][j] = 0
			elif (dataset[i][j] == 'Iris-versicolor'):
				dataset[i][j] = 1
 
#converting the string into float in the dataset
def string_to_float(dataset):
	for i in range(100):
		for j in range(4):
			dataset[i][j] = float(dataset[i][j])


# Make a prediction with weights
def predict(row, weights, threshold):
	sum_weight = weights[0] #this is the weight of the bias
	for i in range(len(row)-1):
		sum_weight += weights[i + 1] * row[i]
	return 1 if sum_weight >= threshold else 0
	

# Estimate weights
def train_weights(trainset, l_rate, max_iter,threshold):
	weights = [0.2 for i in range(len(trainset[0]))]
	total_error = 0
	for itern in range(max_iter):
		for row in trainset:
			prediction = predict(row, weights, threshold)
			error = row[-1] - prediction               
			total_error += error * error
			weights[0] = weights[0] + l_rate * error  
			for i in range(len(row)-1):
				weights[i + 1] = weights[i + 1] + l_rate * error * row[i] 
		if(total_error == 0):
			break
	return weights
	
	 
# Split a dataset into k folds
def cross_validation_split(dataset, n_folds):
	dataset_split = list()
	dataset_copy = list(dataset)
	fold_size = int(len(dataset) / n_folds)
	for i in range(n_folds):
		fold = list()
		while len(fold) < fold_size:
			index = randrange(len(dataset_copy))
			fold.append(dataset_copy.pop(index))
		dataset_split.append(fold)
	return dataset_split
 
# Calculate accuracy percentage
def accuracy_metric(actual, predicted):
	correct = 0
	for i in range(len(actual)):
		if actual[i] == predicted[i]:
			correct += 1
	return correct / float(len(actual)) * 100.0
 
# Evaluate an algorithm using a cross validation split
def evaluate_algorithm(dataset, algorithm, n_folds, l_rate,max_iter,threshold):
	folds = cross_validation_split(dataset, n_folds)
	scores = list()
	for fold in folds:
		train_set = list(folds)
		train_set.remove(fold)
		train_set = sum(train_set, [])
		test_set = list()
		for row in fold:
			row_copy = list(row)
			test_set.append(row_copy)
			row_copy[-1] = None
		predicted = algorithm(train_set, test_set, l_rate, max_iter,threshold)
		actual = [row[-1] for row in fold]
		accuracy = accuracy_metric(actual, predicted)
		scores.append(accuracy)
	return scores
 
 
# Perceptron Algorithm With Stochastic Gradient Descent
def perceptron(train, test, l_rate, max_iter,threshold):
	predictions = list()
	weights = train_weights(train, l_rate, max_iter,threshold)
	print weights
	for row in test:
		prediction = predict(row, weights,threshold)
		predictions.append(prediction)
	return(predictions)
 

if __name__ == '__main__':
	filename = 'IRIS.csv'
	dataset = load_csv(filename)
	dataset, numrow, numcol = load_csv(filename)
	number_classlabel(dataset)
	string_to_float(dataset)
	l_rate = .15
	threshold = 2.5
	max_iter= 100
	n_folds = 10
	scores = evaluate_algorithm(dataset, perceptron, n_folds, l_rate, max_iter,threshold)
	print('Scores: %s' % scores)
	print('Mean Accuracy: %.3f%%' % (sum(scores)/float(len(scores))))
