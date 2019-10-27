# markov_chains.py

import numpy as np
import scipy as sp
from scipy import linalg as la
from numpy import linalg as nla


def random_markov(n):
    """Create and return a transition matrix for a random Markov chain with
    'n' states, stored as an nxn NumPy array.
    """
    A = np.random.random((n,n))

    #normalize the columns
    for i in xrange(n):

        A[:,i] = A[:,i] / np.sum(A[:,i])

    return A


def forecast(days):
    """Forecast tomorrow's weather given that today is hot=0."""
         #success is 1 = cold

    t_matrix = np.array(([0.7, 0.6], [0.3, 0.4]))

    forecast = []
    today = 0
    
    for i in xrange(0, days):
        today = np.random.binomial(1, t_matrix[1, today])
        # Sample from a binomial distribution (with n=1) to choose a new state.

        forecast.append(today)

    return forecast


def four_state_forecast(days):
    """Run a simulation for the weather over the specified number of days,
    with mild as the starting state, using the four-state Markov chain.
    Return a list containing the day-by-day results, not including the
    starting day.

    Examples:
        >>> four_state_forecast(3)
        [0, 1, 3]
        >>> four_state_forecast(5)
        [2, 1, 2, 1, 1]

    0= hot, 1= mild, 2= cold, 3= freezing
    """
    today = 1 #first day is Mild
    forecast = []
    t_matrix = np.array([[0.5, 0.3, 0.1, .0], [0.3, 0.3, 0.3, 0.3], [0.2, 0.3, 0.4, 0.5], [0., 0.1, 0.2, 0.2]])

    for i in xrange(0, days):
                #np.random.multinomial(1, probabilities)
        array = np.random.multinomial(1, t_matrix[:,today])  #to get the column
                    #returns an array [0 ... 1 ... 0 0]
             
        #today gets set to where the 1 is in the array 
        today = np.argmax(array)   
        
        forecast.append(today)

    return forecast


def steady_state(A, tol=1e-12, N=40):
    """Compute the steady state of the transition matrix A.

    Inputs:
        A ((n,n) ndarray): A column-stochastic transition matrix.
        tol (float): The convergence tolerance.
        N (int): The maximum number of iterations to compute.

    Raises:
        ValueError: if the iteration does not converge within N steps.

    Returns:
        x ((n,) ndarray): The steady state distribution vector of A.
    """
    n,n = A.shape

    x = abs(np.random.rand(n,1))

    #normalize
    x = x / float(np.sum(x)) 
    i = 0
    t = 1

    while i <= N and t >= tol:
        
        i+=1
        newx = np.dot(A, x)
        #calculate x^(k+1) = A x^k

        t = la.norm(newx - x, ord=np.inf)
        x = newx
        if i > N:
            raise ValueError("the matrix A^k does not converge")
            break

    return newx


# Problems 5 and 6
class SentenceGenerator(object):
    """Markov chain creator for simulating bad English.

    Attributes:
        (what attributes do you need to keep track of?)

    Example:
        >>> yoda = SentenceGenerator("Yoda.txt")
        >>> print yoda.babble()
        The dark side of loss is a path as one with you.
    """

    def __init__(self, filename):
        """Read the specified file and build a transition matrix from its
        contents. You may assume that the file has one complete sentence
        written on each line.
        """
        self.filename = filename
        #one sentence on each line
        with open(filename, 'r') as sentence_file:

            my_lines = []

            states = ["$tart"]

            for line in sentence_file:

                sentence = line.strip("\n")
                my_lines.append(sentence)

            for s in my_lines:

                words = s.split(" ")

                for w in words:
                    if w not in states:
                        states.append(w)
            
            states.append("$top")
            
        first_array = np.zeros((len(states), len(states)))

        for line in my_lines:
            words = ["$tart"] + line.split(" ") + ["$top"]
                #example of words = [$tart, I, am , Sam, Sam, I, am., $top] (first line)

                #states = [$tart, I, am, Sam, am., $top]
            indices = [states.index(w) for w in words]

                #becomes [0, 1, 2, 3, 3, 1, 2, 4, 5]

            for i in xrange(len(words)-1):
                first_array[indices[i+1], indices[i]] +=1
            #P [1 , 0]      0 --> 1
            #P [2, 1]      1 -- connected --> to 2


        first_array[-1,-1] +=1    #so no division by 0 in last column

        new_array = first_array / np.sum(first_array, axis=0)

        #print new_array.sum(axis=0)  adding up columns to see if = 1

        self.t_matrix = new_array
        self.states = states

    def babble(self):
        """Begin at the start sate and use the strategy from
        four_state_forecast() to transition through the Markov chain.
        Keep track of the path through the chain and the corresponding words.
        When the stop state is reached, stop transitioning and terminate the
        sentence. Return the resulting sentence as a single string.
        """

        current_state = 0 # self.states[0]
        path = []

        while current_state != self.states.index("$top"):

            array = np.random.multinomial(1, self.t_matrix[:,current_state])  #to get the column
                #returns an array [0 ... 1 ... 0 0]
             
            #current_state gets set to where the 1 is in the array 
            current_state = np.argmax(array)
            path.append(current_state)

        path.pop()  #gets rid of "$top"
        #return path
        #make list called "path" into a string
        word_list = [self.states[p] for p in path]

        return " ".join(word_list)


if __name__ == '__main__':
    #print forecast(5)
    #B = random_markov(3)
    #print steady_state(B)
    #print nla.matrix_power(B, 8) #check B_k
    #print steady_state(np.array([[0.7, 0.6], [0.3, 0.4]]))
    #print four_state_forecast(5)
    b = SentenceGenerator("tswift1989.txt")
    print b
    print b.babble()