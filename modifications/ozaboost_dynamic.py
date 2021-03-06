#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:mod:`Ozaboost_dynamic`
==================

.. module:: Ozaboost_dynamic
:platform: Mac OS X
:synopsis:

.. moduleauthor:: deshana.desai@nyu.edu

Created on 2017-11-19, 5:00

"""
from collections import defaultdict
from math import log
import math
import numpy as np
from numpy.random import poisson, seed

from sklearn.tree import DecisionTreeClassifier
#from sgdclassifier import sgd_classifier


class OzaBoostClassifier():
    def __init__(self, learners, classes, total_points):
        self.total_points = total_points
        self.classes = classes
        self.learners = [learners(classes) for i in range(self.total_points)]
        #self.learners = [DecisionTree(classes) for i in range(self.total_points)]
        #self.learners = [perceptron.Perceptron(classes) for i in range(self.total_points)]
        #self.learners = [sgd_classifier(classes) for i in range(self.total_points)]
        self.correct = [0.0 for i in range(self.total_points)]
        self.incorrect = [0.0 for i in range(self.total_points)]
        self.error = [0.0 for i in range(self.total_points)]
        self.coeff = [0.0 for i in range(self.total_points)]

        def get_error_rate(self, predictions, Y):
            temp = zip(predictions, Y)
            correct = 0.0
            for (p,y) in temp:
                if p==y:
                    correct+=1
            return float(correct)/float(len(Y))


    def initialize_new_learner(self, learner, X, Y, weight, prev_points):

        dt = learner(self.classes)
        correct = incorrect = 0.0

        for (x,y) in prev_points:
            dt.partial_fit(x,y)
            if dt.predict(x)==y:
                correct+=1.0
            else:
                incorrect += 1.0
        '''
        dt = self.learners[len(self.learners)//2]
        correct = self.correct[len(self.learners)//2]
        incorrect = self.incorrect[len(self.learners)//2]
        '''

        # Check: order matters in online boosting.
        for i in range(poisson(weight)):
            dt.partial_fit(X,Y)
        if dt.predict(X)==Y:
            correct+= weight
        else:
            incorrect += weight


        self.learners.append(dt)
        self.correct.append(correct)
        self.incorrect.append(incorrect)
        self.error.append(0.0)
        self.coeff.append(0.0)	 


        #print ("Is the new classification correct/closer for Y: %d" % (Y))
        (key, conf, label_weights) = self.classify(X)
        #print ("The classification: ",key,"the weight: ", conf, "& Y: ",Y)
        #print(label_weights)
        #print ("\n\n")



    def pretrain(self, train_X, train_Y, X_val, y_val):
        errors = []
        import random
        data = zip(train_X, train_Y)
        for i, learner in enumerate(self.learners):
            datapoints_x = []
            datapoints_y = []
            while True:
                index_point = random.randint(0,train_X.shape[0]-1)
                datapoints_x.append(train_X[index_point])
                datapoints_y.append(train_Y[index_point])
                learner.fit(datapoints_x, datapoints_y, self.classes)
                test_error = self.get_error_rate(learner.model.predict(X_val), y_val)
                if test_error>0.5:
                    break
                #train_X, train_Y, test_X, test_Y = train_test_split(data, test_size = 0.2)
            #learner.model.fit(datapoint_x, train_Y)
            #learner.model.fit(datapoints_x,datapoints_y)
            #test_error = learner.model.predict(X_val)
            training_error = learner.model.predict(train_X)
            errors.append((self.get_error_rate(training_error, train_Y),test_error))
        return errors

    def update(self, X, Y):
        weight = 1.0
        for i, learner in enumerate(self.learners):
            #print "Round: ",i
            k = poisson(weight)
            #print "Poisson Dist: ",k
            if not k:
                continue

            for j in range(k):
                learner.partial_fit(X,Y)

            prediction = learner.predict(X)

            #print "Initial Weight: ", weight

            if prediction == Y:
                self.correct[i] = self.correct[i]+weight
                N = float(self.correct[i]+self.incorrect[i])
                temp = (N/(2.0*float(self.correct[i])))

                weight *= temp
                #print "Weight of example has decreased to: ",weight
            else:
                self.incorrect[i] = self.incorrect[i]+weight
                N = float(self.correct[i]+self.incorrect[i])
                weight = weight*(N/(2*self.incorrect[i]))
                #print "Weight of example has increased to: ",weight
        return weight

    def classify(self,X):	
        label_weights = {}

        for i, learner in enumerate(self.learners):
            N = self.correct[i]+self.incorrect[i]+ 1e-16
            self.error[i] = (self.incorrect[i]+ 1e-16)/N
            self.coeff[i] = (self.error[i]+ 1e-16)/(1.0-self.error[i]+ 1e-16)

        for i,learner in enumerate(self.learners):
            weight_learner = log(1/self.coeff[i])
            label = learner.predict(X)
            if label in label_weights.keys():
                label_weights[label] += weight_learner
            else:
                label_weights[label] = weight_learner
        #print("learner ",i,": ",format(weight_learner,"0.2f"))

        key =  max(label_weights.iterkeys(), key = (lambda key: label_weights[key]))


        return (key,label_weights[key], label_weights) 		

