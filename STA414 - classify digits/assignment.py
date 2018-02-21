from __future__ import absolute_import
from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

import numpy as np

from scipy.misc import logsumexp
import os
import gzip
import struct
import array

import matplotlib.pyplot as plt
import matplotlib.image
from urllib.request import urlretrieve

def download(url, filename):
    if not os.path.exists('data'):
        os.makedirs('data')
    out_file = os.path.join('data', filename)
    if not os.path.isfile(out_file):
        urlretrieve(url, out_file)

def mnist():
    base_url = 'http://yann.lecun.com/exdb/mnist/'

    def parse_labels(filename):
        with gzip.open(filename, 'rb') as fh:
            magic, num_data = struct.unpack(">II", fh.read(8))
            return np.array(array.array("B", fh.read()), dtype=np.uint8)

    def parse_images(filename):
        with gzip.open(filename, 'rb') as fh:
            magic, num_data, rows, cols = struct.unpack(">IIII", fh.read(16))
            return np.array(array.array("B", fh.read()), dtype=np.uint8).reshape(num_data, rows, cols)

    for filename in ['train-images-idx3-ubyte.gz',
                     'train-labels-idx1-ubyte.gz',
                     't10k-images-idx3-ubyte.gz',
                     't10k-labels-idx1-ubyte.gz']:
        download(base_url + filename, filename)

    train_images = parse_images('data/train-images-idx3-ubyte.gz') [0:10000]
    train_labels = parse_labels('data/train-labels-idx1-ubyte.gz')[0:10000]
    test_images  = parse_images('data/t10k-images-idx3-ubyte.gz')[0:10000]
    test_labels  = parse_labels('data/t10k-labels-idx1-ubyte.gz')[0:10000]

    return train_images, train_labels, test_images, test_labels


def load_mnist():
    partial_flatten = lambda x : np.reshape(x, (x.shape[0], np.prod(x.shape[1:])))    
    one_hot = lambda x, k: np.array(x[:,None] == np.arange(k)[None, :], dtype=int)
    train_images, train_labels, test_images, test_labels = mnist()
    train_images = partial_flatten(train_images) / 255.0
    test_images  = partial_flatten(test_images)  / 255.0 # each row is an image (size 784)
    train_labels = one_hot(train_labels, 10) # converts to k coding, where each row is the coding for 1 image
    test_labels = one_hot(test_labels, 10)
    N_data = train_images.shape[0] # = number of training images

    np.place(train_images, train_images<0.5, [0])
    np.place(train_images, train_images>=0.5, [1])

    np.place(test_images, test_images<0.5, [0])
    np.place(test_images, test_images>=0.5, [1])
    
    return N_data, train_images, train_labels, test_images, test_labels,

def plot_images(images, ax, ims_per_row=5, padding=5, digit_dimensions=(28, 28),
                cmap=matplotlib.cm.binary, vmin=None, vmax=None):
    """Images should be a (N_images x pixels) matrix.""" #ie. an array of n images whicha are represented by a matrix
    N_images = images.shape[0]
    N_rows = np.int32(np.ceil(float(N_images) / ims_per_row))
    pad_value = np.min(images.ravel())
    concat_images = np.full(((digit_dimensions[0] + padding) * N_rows + padding,
                             (digit_dimensions[1] + padding) * ims_per_row + padding), pad_value)
    for i in range(N_images):
        cur_image = np.reshape(images[i, :], digit_dimensions)
        row_ix = i // ims_per_row
        col_ix = i % ims_per_row
        row_start = padding + (padding + digit_dimensions[0]) * row_ix
        col_start = padding + (padding + digit_dimensions[1]) * col_ix
        concat_images[row_start: row_start + digit_dimensions[0],
                      col_start: col_start + digit_dimensions[1]] = cur_image
    cax = ax.matshow(concat_images, cmap=cmap, vmin=vmin, vmax=vmax)
    plt.xticks(np.array([]))
    plt.yticks(np.array([]))
    return cax

def save_images(images, filename, ims_per_row = 5, **kwargs):
    fig = plt.figure(1)
    fig.clf()
    ax = fig.add_subplot(111)
    plot_images(images, ax, ims_per_row = ims_per_row, **kwargs)
    fig.patch.set_visible(False)
    ax.patch.set_visible(False)
    plt.savefig(filename)
    
########################################################################################################################











class BasicNaiveBayesModel():
    
    def __init__(self, imagesIn, labelsIn):
        self.tainImages = imagesIn
        self.trainLabels = labelsIn 
        self.thetas = np.zeros( (10,784), float )
    
    # Question 1b
    def trainModel(self):
        iamgeDigit = np.argmax(self.trainLabels, axis = 1) 
        thetas = np.empty((0, 784), float)
        for c_i in range(10):
            imagesOfc_i = self.tainImages[iamgeDigit == c_i, ]
            pixelSum = np.sum(imagesOfc_i, axis = 0)
            theta_ci =(pixelSum + 1) / (imagesOfc_i.shape[0] + 2)
            thetas = np.append(thetas, np.array([theta_ci]), axis=0)
        self.thetas = thetas

    # Question 1d
    def predictiveLogLikelihood(self, images_in, labelsKCoding):
        iamgeDigit = np.argmax(labelsKCoding, axis = 1) 
        
        # caculate the log likelihood for each image and image class combinations
        firstTerm = np.dot( np.log(self.thetas), np.transpose(images_in))
        secondTerm = np.dot( np.log(1 - self.thetas), np.transpose(1-images_in))
        thirdTerm = np.zeros((10, images_in.shape[0]))
        for c_i in range(10):
            row = np.prod(np.power(self.thetas[c_i,], images_in) *  
                          np.power(( 1 - self.thetas[c_i, ]), (1-images_in)), axis = 1 )
            thirdTerm = thirdTerm + row
        predictiveLogLikelihood = firstTerm + secondTerm - np.log( thirdTerm )
        
        averageLikelihood = np.sum( np.transpose(predictiveLogLikelihood) * labelsKCoding)   
        averageLikelihood = averageLikelihood  / images_in.shape[0]
        
        maxIndex = np.argmax(predictiveLogLikelihood, axis = 0)
        predictiveAccuracy = np.true_divide(np.sum(maxIndex == iamgeDigit ), 
                                            images_in.shape[0]/100) 
        
        return averageLikelihood, predictiveAccuracy   
     
    # Question 2c    
    def generateRandomSample(self):
        randomThetas = self.thetas[ np.random.randint(low = 0, high = 10, size =10), ]
        randomDigits = np.random.binomial(1, randomThetas)
        return randomDigits
    
    # Question 2f
    def calculateProbabilityOfBotton(self, image, thetas):
        bottonThetas = thetas[: ,392:784]
        imageTop = image[0:392]
        topThetas = thetas[: ,0:392]
    
        topThetasProduct = np.prod(np.power(topThetas, imageTop ) *
                                   np.power((1-topThetas),(1-imageTop))  , axis = 1 )    
        bottomProbabilities = np.dot(topThetasProduct, bottonThetas) / np.sum(topThetasProduct) 
        newImage = np.concatenate( (imageTop, bottomProbabilities), axis =0)
        
        return newImage, image
    
    
########################################################################################################################
    


















































########################################################################################################################
class LogisticRegression():

    def __init__(self, train_images, train_labels, batchSize, trainingSteps ):
        self.train_images = train_images
        self.train_labels = train_labels
        self.weights = [np.zeros( (10,784) )]
        self.batchSize = batchSize
        self.trainingSteps = trainingSteps
    
    def gradientCal(self, images, weights, labels):
        exp_wx = np.exp( np.dot(weights[0], np.transpose(images)) )
        sumOf_wx = np.sum(exp_wx, axis = 0)   
        y = np.divide(exp_wx, sumOf_wx )
        grad =np.dot( np.transpose(labels) - y , images  ) / images.shape[0]
        return grad
    
    def accuracyCalculation(self, weights, images, labels):
        predictions = np.dot(weights[0], np.transpose(images)) 
        sumWX =  predictions - logsumexp(predictions, axis = 0)
        
        TotalLikelihood =  np.sum( np.transpose(sumWX ) *labels) 
        imageDigit = np.argmax(labels  , axis = 1)
        maxIndex = np.argmax(sumWX  , axis = 0)    
        correctClassified = np.sum(maxIndex == imageDigit )

        averageLikelihood = TotalLikelihood  / labels.shape[0] 
        predictiveAccuracy = np.true_divide(correctClassified , images.shape[0]) 
        
        return  averageLikelihood, predictiveAccuracy
     
    def train(self):
        averageLL = []
        predictionAccuracy = []
        step = []
        for i in range(1, self.trainingSteps):
            BatchIndexes = np.random.randint(low = 0, high = self.train_images.shape[0], 
                                             size = self.batchSize )
            BatchImages = self.train_images[BatchIndexes,]
            grad = self.gradientCal(BatchImages, self.weights, self.train_labels[BatchIndexes])
            self.weights[0] += 0.01 * grad
            if i%200 == 0:
                averageLikelihood, predictiveAccuracy = self.accuracyCalculation(self.weights, 
                                                        self.train_images, self.train_labels) 
                averageLL.append(averageLikelihood)
                step.append(i)
                predictionAccuracy.append(predictiveAccuracy)
        return self.weights, averageLL, predictionAccuracy, step

########################################################################################################################
    

########################################################################################################################

class UnsupervisedNaiveBayes():
    def __init__(self, images, numOfClassifications ):
        rand = np.random.uniform(low=0.3, high=0.7, size=784*numOfClassifications)
        self.thetas =  rand.reshape(numOfClassifications, 784)
        self.k = numOfClassifications
        self.images = images        
        self.numOfImage =  images.shape[0]
        self.E = np.empty( (numOfClassifications, self.numOfImage) )
            
    def EM(self):
        for i in range(10):
            print(i)
            self.eStep()
            self.mStep()
           
    def eStep(self):
        self.E = np.empty((0, self.images.shape[0] ))
        for c_i in range(self.k):
            row = np.prod(np.power(self.thetas[c_i,], self.images) * np.power(( 1 - self.thetas[c_i, ]), (1-self.images)), axis = 1 )
            self.E = np.append(self.E , row.reshape(1, self.images.shape[0]), axis = 0)
        totalProb = np.sum(self.E, axis = 0)
        self.E = np.divide( self.E, totalProb )

    def mStep(self):          
        NE = np.dot(self.E, self.images)
        totalE = np.sum(self.E, axis = 1).reshape(self.k, 1)
        self.thetas = NE / totalE
        
    def grad(self, image):
        pp = 1/self.thetas * image - 1/(1-self.thetas) * (1-image)
        qq =np.diagonal(  np.dot( np.power(self.thetas, image), np.transpose( np.power(1-self.thetas,1- image)))). reshape(self.k,1)
        grad = pp * qq / np.sum(qq)
        return grad
    
    def gradas(self):
        for i in range(5000):
            BatchIndexes = np.random.randint(low = 0, high = self.images.shape[0],  size = 1 )
            BatchImages = self.images[BatchIndexes,]
            grad = self.grad(BatchImages)
            self.thetas += 0.01 * grad
        
    #Question 4e
    def calculateProbabilityOfBotton(self, image, thetas):
        bottonThetas = thetas[: ,392:784]
        imageTop = image[0:392]
        topThetas = thetas[: ,0:392]
    
        topThetasProduct = np.prod(np.power(topThetas, imageTop ) *  np.power((1-topThetas),(1-imageTop))  , axis = 1 )    
        bottomProbabilities = np.dot(topThetasProduct, bottonThetas) / np.sum(topThetasProduct) 
        newImage = np.concatenate( (imageTop, bottomProbabilities), axis =0)
        
        return newImage, image
         ########################################################################################################################       











      
def main():
    N_data, train_images, train_labels, test_images, test_labels = load_mnist()
    save = False
    DoQuestion1And2 = True
    DoQuestion3 = True
    DoQuestion4 = False
    
    
    if (DoQuestion1And2):
        basicNaiveBayesModel = BasicNaiveBayesModel(train_images, train_labels)
        
        # Question 1 b
        basicNaiveBayesModel.trainModel()
        if save == True:
            save_images(basicNaiveBayesModel.thetas, "Q1b" )
        else:
           plot_images(basicNaiveBayesModel.thetas, plt) 

        # Question 1 d
        averageLikelihood , predictiveAccuracy = basicNaiveBayesModel.predictiveLogLikelihood(train_images, train_labels)
        print("For the training set,predictiveAccuracy = ", "{:.2f}" .format( predictiveAccuracy), "averageLikelihood = ", averageLikelihood)
        
        averageLikelihood , predictiveAccuracy = basicNaiveBayesModel.predictiveLogLikelihood(test_images, test_labels)
        print("For the testing set,predictiveAccuracy = ", "{:.2f}" .format( predictiveAccuracy), "averageLikelihood = ", averageLikelihood)
        
        # Question 2 c
        randomSample = basicNaiveBayesModel.generateRandomSample()
        if save == True:
             save_images(randomSample, "Q2c" )
        else:
            plot_images(randomSample, plt)
       
        # Question 2 f
        randomSample =  np.random.randint(low = 0, high = train_images.shape[1] , size = 20 )         
        pics = np.empty((0,784), float)
        for index in randomSample:
            pic1, pic2 = basicNaiveBayesModel.calculateProbabilityOfBotton(train_images[index,], basicNaiveBayesModel.thetas)
            pics = np.append(pics, np.array([pic1]), axis=0)
            pics = np.append(pics, np.array([pic2]), axis=0)
        if save == True:
             save_images(pics, "Q2f", ims_per_row = 4 )
        else:
            plot_images(pics, plt, ims_per_row = 4)
  
     
    if (DoQuestion3): 
        logisticRegression = LogisticRegression( train_images, train_labels, 200, 20000)
        weights, averageLL, predictionAccuracy, steps = logisticRegression.train()
        
        if save == True:
            save_images(weights[0], "Q3d" )
        else:
            plot_images(weights[0], plt)

        fig2 = plt.figure()
        ax2 = fig2.add_subplot(111)
        plt.xlabel("Step") 
        plt.ylabel("Average Likelihood")
        plt.title("Average Likelihood")
        ax2.plot(steps, averageLL)
        plt.savefig("llCurve")
        
        fig3 = plt.figure()
        ax3 = fig3.add_subplot(222)
        plt.xlabel("Step") 
        plt.ylabel("Predictive Accuracy")
        plt.title("Predictive Accuracy")
        ax3.plot(steps, predictionAccuracy)  
        plt.savefig("Pred accuracy")
        
        averageLikelihood , predictiveAccuracy = logisticRegression.accuracyCalculation(weights, train_images , train_labels)
        print("For the training set,predictiveAccuracy = ", "{:.3f}" .format( predictiveAccuracy), "averageLikelihood = ", averageLikelihood)
        
        averageLikelihood , predictiveAccuracy = logisticRegression.accuracyCalculation(weights, test_images , test_labels)
        print("For the testing set,predictiveAccuracy = ", "{:.3f}" .format( predictiveAccuracy), "averageLikelihood = ", averageLikelihood)
        
    if (DoQuestion4):   
        unsupervisedNaiveBayes = UnsupervisedNaiveBayes( train_images, 30)
        unsupervisedNaiveBayes.gradas()
        
        if save == True:
            save_images(unsupervisedNaiveBayes.thetas, "Q4d" )
        else:
            plot_images(unsupervisedNaiveBayes.thetas, plt)
            
            
        randomSample =  np.random.randint(low = 0, high = train_images.shape[1] , size = 20 )         
        pics = np.empty((0,784), float)
        for index in randomSample:
            pic1, pic2 = unsupervisedNaiveBayes.calculateProbabilityOfBotton(train_images[index,], unsupervisedNaiveBayes.thetas)
            pics = np.append(pics, np.array([pic1]), axis=0)
            pics = np.append(pics, np.array([pic2]), axis=0)
        if save == True:
             save_images(pics, "Q4e", ims_per_row = 4 )
        else:
            plot_images(pics, plt, ims_per_row = 4)
      
main()
