import numpy as np
 
#print np.__doc__
#np.lookfor("array")

# sigmoid function
def nonlin(x,deriv=False):
    if(deriv==True):
        return x*(1-x)
    return 1/(1+np.exp(-x))
 
def pp(arr):
    for aa in arr:
        print "%+03f " % aa,
    print
    
# input dataset
X = np.array([  [0,0,1],
                [0,1,1],
                [1,0,1],
                [1,1,1] ])
                
print X                 
     
# output dataset           
y = np.array([  [0,1,1,0]
             ]).T
#print y.T

  
print "input",  ; #pp(X.T)
print "expected output", y

# seed random numbers to make calculation
# deterministic (just a good practice)
np.random.seed(1)
 
# initialize weights randomly with mean 0
syn0 = 2*np.random.random((3,1)) - 1
 
for iter in xrange(1000):
 
    # forward propagation
    l0 = X
    l1 = nonlin(np.dot(l0,syn0))
 
    # how much did we miss?
    l1_error = y - l1
    if iter % 100 == 0:
        pp(l1_error)
 
    # multiply how much we missed by the
    # slope of the sigmoid at the values in l1
    l1_delta = l1_error * nonlin(l1,True)
 
    # update weights
    syn0 += np.dot(l0.T,l1_delta)
 
print "Output After Training:"
print l1
pp(l1)









