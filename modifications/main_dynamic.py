import argparse
from random import seed
from sklearn import datasets
import test_dynamic
from sklearn.datasets import load_svmlight_file
import numpy as np
from sklearn.model_selection import train_test_split

if __name__ == "__main__":
	seed(0)
	parser = argparse.ArgumentParser()

	parser.add_argument('dataset', help='dataset filename')
	parser.add_argument('M', metavar='# weak_learners', help='number of weak learners', type=int)
	parser.add_argument('trials', help='number of trials (each with different shuffling of the data); defaults to 1', type=int, default=1, nargs='?')
	parser.add_argument('--record', action='store_const',const=True, default = False, help = 'export the results in file')
	args = parser.parse_args()

	
	data = datasets.load_iris()
	X = data.data
	y = data.target
	'''y_clean = []
	for item in y:
		if item==1:
			y_clean.append(item)
		elif item==0:
			y_clean.append(-1)

	y = np.array(y_clean)

	#df = pd.read_csv(dataset,header=None)
	raw_data = open(args.dataset, 'r')
	data = np.loadtxt(raw_data,delimiter=",")
	output_class = 6
	X,y = data[:,:output_class], data[:,output_class]
	#X = X.as_matrix()
	#y = y.as_matrix()'''
	X_train, X_test, y_train, y_test = train_test_split(X,y,test_size = 0.20, random_state = 1)
	model = test_dynamic.Test(X,y,args.M)
	train_accuracy, baseline_train_accuracy = model.test(X_train,y_train,X_test, y_test, args.M,trials=args.trials)
	print "Running for "+str(args.M)+" weak learners.."
	print "Shape of Train Data: ",X_train.shape,y_train.shape
	print "Shape of Test Data: ",X_test.shape, y_test.shape
	test_accuracy, baseline_test_accuracy = model.final_test(X_test,y_test,args.M)
	print "Accuracy on Training Set/ Baseline :"
	print train_accuracy, baseline_train_accuracy
	print "Test Accuracy/ Baseline: "
	print test_accuracy, baseline_test_accuracy

	if args.record:
		results = {
			'm': args.M,
			'Training Accuracy':train_accuracy,
			'Baseline Training Accuracy': baseline_train_accuracy,
			'Testing Accuracy': test_accuracy,
			'Baseline Testing Accuracy': baseline_test_accuracy,
			'trials': args.trials,
			'seed': 0
		}
		filename = open('adaboost_results_'+str(args.dataset)+'_'+str(args.M)+'.txt','a')
		filename.write("BEGIN\n")
		for k,v in results.items():
			filename.write(str(k)+"~~ "+str(v)+"\n")
		filename.write("END\n\n")
		filename.close()
