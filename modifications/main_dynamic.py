import argparse
from random import seed
from sklearn import datasets
import test_dynamic
import numpy as np
from .../ensembles import osboost, ocpboost, expboost, ozaboost, smoothboost
from sklearn.model_selection import train_test_split
from learners import nb_gaussian,sk_nb, nb, perceptron, random_stump, sk_decisiontree, decision_trees

if __name__ == "__main__":
	seed(0)
	parser = argparse.ArgumentParser()

	parser.add_argument('dataset', help='dataset filename')
	parser.add_argument('algorithm', help = 'Boosting algorithm')
	parser.add_argument('weak_learner', help='chosen weak learner')
	parser.add_argument('M', metavar='# weak_learners', help='number of weak learners', type=int)
	parser.add_argument('trials', help='number of trials (each with different shuffling of the data); defaults to 1', type=int, default=1, nargs='?')
	parser.add_argument('--record', action='store_const',const=True, default = False, help = 'export the results in file')
	args = parser.parse_args()

	'''Car Dataset'''
	#data = np.genfromtxt("data/car.csv",delimiter=",")
	#rows,cols = data.shape
	#X,y = data[1:,1:cols-1],data[1:,cols-1]
	#X,y = X.astype(int), y.astype(int)

	'''Heart Dataset''' 
	data = np.genfromtxt("data/heart.csv",delimiter=",")
	rows,cols = data.shape
	X,y = data[1:,1:cols-1],data[1:,cols-1]
	y = np.where(y>0, 1,-1)
	y = y.astype(int)
    
	#print (X[0:10],y[0:10])
    
	'''Ionosphere Dataset''' 
	#data = np.genfromtxt("data/ionosphere.csv",delimiter=",")
	#rows,cols = data.shape
	#X,y = data[1:,1:cols-1],data[1:,cols-1]
	#y = y.astype(int)
    
	
	'''Breast Cancer Dataset'''
	#data = datasets.load_breast_cancer()
	#X = data.data
	#y = data.target
	
	# binary classification:  changing 1/0 to 1/-1
	'''
	y_clean = []
	for item in y:
		if item==1:
			y_clean.append(item)
		elif item==0:
			y_clean.append(-1)

	y = np.array(y_clean)
	'''

	algorithms = {
	"smoothboost":smoothboost.SmoothBoost,
	"osboost":osboost.OSBoost,
	"ocpboost":ocpboost.OCPBoost,
	"expboost":expboost.EXPBoost,
	"ozaboost":ozaboost.OzaBoostClassifier}

	weak_learners ={
	"sk_nb":sk_nb.NaiveBayes,
	"gaussian_nb":nb_gaussian.NaiveBayes,
	"nb": nb.NaiveBayes,
	"sk_decisiontree": sk_decisiontree.DecisionTree,
	"random_stump":random_stump.RandomStump,
	"decisiontree":decision_trees.DecisionTree,
	"perceptron":perceptron.Perceptron}


	#model = test.Test(weak_learners[args.weak_learner],X,y,args.M)
	#print model.test(X,y,[],[],args.M, trials = args.trials)
		
	X_train, X_test, y_train, y_test = train_test_split(X,y,test_size = 0.20, random_state = 1)
	model = test_dynamic.Test(algorithms[args.algorithm], weak_learners[args.weak_learner],X,y,args.M)
	train_accuracy, baseline_train_accuracy = model.test(X_train,y_train,X_test, y_test, args.M,trials=args.trials)
	print "Running for "+str(args.M)+" weak learners.."
	print "Shape of Train Data: ",X_train.shape,y_train.shape
	print "Shape of Test Data: ",X_test.shape, y_test.shape
	test_accuracy, baseline_test_accuracy = model.final_test(X_test,y_test,args.M)
	print "Accuracy on Training Set/ Baseline :"
	print train_accuracy[-1], baseline_train_accuracy[-1]
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
