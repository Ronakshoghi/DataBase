"""
This file contains some code to perform spacing filling. 

"""
import numpy as np
from scipy.spatial import KDTree

def softmax_simplex_weights(n, num_points):
    """
    A method for sampling n-dimenionsal simplex weights
    (must sum to 1).
    
    This method samples each dimension independently and
    then reweights the line using softmax. 

    Args:
        n (int): the dimension of the simplex
        num_points (int): the number of samples that are desired. 

    Returns:
        numpy array: [num_points, n] dimensional numpy array containing
                     the simplex weights. 
    """
    weight_list = np.random.rand(num_points, n)
    weight_list = (weight_list.transpose() / weight_list.sum(axis=1)).transpose()
    return weight_list

def sequential_simplex_weights(n, num_points):
    """
    A method for sampling n-dimensional simplex weights
    (must some to 1). 

    Weights are sequentially produced by first sampling
    the first dimension and then assigning the remaining
    dimensions to the remaining portion recursively. 

    Args:
        n (int): the dimension of the simplex
        num_points (int): the number of samples that are desired. 

    Returns:
        numpy array: [num_points, n] dimensional numpy array containing
                     the simplex weights. 
    """
    weight_list = np.zeros([num_points, n])
    weight_list[:, 0] = np.random.rand(num_points)
    
    for i in range(1, n-1):
        weight_list[:, i] = (1 - weight_list.sum(axis=1)) * \
            np.random.rand(num_points)
    
    weight_list[:, -1] = 1 - weight_list.sum(axis=1)
    
    return weight_list

def permutedsequential_simplex_weights(n, num_points):
    """
    A method for sampling n-dimensional simplex weights
    (must some to 1). 

    First, follows the sequential strategy: 
    Weights are sequentially produced by first sampling
    the first dimension and then assigning the remaining
    dimensions to the remaining portion recursively. 

    Next: columns are randomly permuted. 

    Args:
        n (int): the dimension of the simplex
        num_points (int): the number of samples that are desired. 

    Returns:
        numpy array: [num_points, n] dimensional numpy array containing
                     the simplex weights. 
    """
    weight_list = np.zeros([num_points, n])
    weight_list[:, 0] = np.random.rand(num_points)
    
    for i in range(1, n-1):
        weight_list[:, i] = (1 - weight_list.sum(axis=1)) * \
            np.random.rand(num_points)
    
    weight_list[:, -1] = 1 - weight_list.sum(axis=1)

    for i in range(num_points):
        # permute each line
        weight_list[i, :] = weight_list[i, :][np.random.permutation(n)]
    
    return weight_list

def permutedsequentialsoftmax_simplex_weights(n, num_points):
    """
    THIS IS THE PREFERRED BARYCENTRIC SAMPLER.
    
    A method for sampling n-dimensional simplex weights
    (must some to 1). 

    First, follows the sequential strategy: 
    Weights are sequentially produced by first sampling
    the first dimension and then assigning the remaining
    dimensions to the remaining portion recursively. 

    Next: columns are randomly permuted. 

    Next: some softmax samples are adding to sample the center better. 

    Args:
        n (int): the dimension of the simplex
        num_points (int): the number of samples that are desired. 

    Returns:
        numpy array: [num_points, n] dimensional numpy array containing
                     the simplex weights. 
    """
    num_softmax = int(num_points * 0.25)
    num_points = num_points - num_softmax

    weight_list = np.zeros([num_points, n])
    weight_list[:, 0] = np.random.rand(num_points)
    
    for i in range(1, n-1):
        weight_list[:, i] = (1 - weight_list.sum(axis=1)) * \
            np.random.rand(num_points)
    
    weight_list[:, -1] = 1 - weight_list.sum(axis=1)

    for i in range(num_points):
        # permute each line
        weight_list[i, :] = weight_list[i, :][np.random.permutation(n)]

    softmax_list = np.random.rand(num_softmax, n)
    softmax_list = (softmax_list.transpose() / softmax_list.sum(axis=1)).transpose()

    weight_list = np.concatenate([weight_list, softmax_list], axis=0)
    
    return weight_list

def generate_design(example_statistics, \
                simplex_weights):
    """
    This method generates new statistics by interpolating (using
    the simplex weights) an initial candidate
    set of examples (the statistics of an initial
    set of structures).

    Args:
        example_statistics (numpy array): a KxREMAINING DIMENSIONS array (where K is
            the number of statistics and N are spatial dimensions)
        simplex_weights (numpy array): a W x K simplex weights matrix
            (K is the number of dimensions - i.e., the number of original
            statistics that we are combining and W is the size of the design.)
    Returns:
        (numpy array): a W x REMAINING DIMENSIONS design in the real space.
    """
    assert type(example_statistics) == np.ndarray

    # ... is producing a weird bug
    letters = ''
    for i in range(len(example_statistics.shape)):
        letters += chr(106 + i)
    
    return np.einsum('ij,'+letters, simplex_weights, example_statistics)

def greedy_thinning(candidate_pool, number_kept, initial_design=None):
    """
    This method thins out an initial candidate pool to produce 
    a final candidate pool. 

    It returns a list of indexes that index the candidate pool
    to identify the desired additions to the design.

    Args:
        candidate pool (numpy array): a (Kx...) array containing candidates
        number_kept (int): the size of the final design that you want. 
        initial_design (numpy array): a (Kx...) array containing the initial
                            design. The initial design needs to have the same
                            dimenionality (except the initial dimension) as the
                            candidate set. Default is None. If default, 
                            no initial design is assumed. 
    """
    assert number_kept <= len(candidate_pool), "The design must be smaller than the initial candidate pool."
    if initial_design is not None:
        assert type(initial_design) is np.ndarray, 'Must pass an ndarray'
        assert candidate_pool.shape[1:] == initial_design.shape[1:], 'The initial design must have the same shape as the candidate pool.'
    import random
    
    candidate_pool = candidate_pool.reshape(len(candidate_pool), -1)

    candidate_indexes = list(range(len(candidate_pool)))
    final_pool_indexes = []
    
    # initial choice:
    if initial_design is None:
        # pick a random point to start the design
        temp_index = random.choice(list(range(len(candidate_indexes))))
        final_pool_indexes.append(candidate_indexes[temp_index])
        del candidate_indexes[temp_index]

    #debug(final_pool_indexes, candidate_indexes, candidate_pool)

    # produce the remaining structure
    while len(final_pool_indexes) < number_kept:
        if initial_design is None:
            current_design = candidate_pool[final_pool_indexes]
        else:
            # add initial design to current design
            current_design = np.concatenate(
                [
                    initial_design,
                    candidate_pool[final_pool_indexes],
                ],
                axis=0
            )
        remainder = candidate_pool[candidate_indexes]

        # build the KD tree:
        kd = KDTree(current_design)
        distances, _ = kd.query(remainder)
        max_distance_indx = distances.argmax()
        
        # add the point to the pool
        final_pool_indexes.append(candidate_indexes[max_distance_indx])
        del candidate_indexes[max_distance_indx]

        #debug(final_pool_indexes, candidate_indexes, candidate_pool)
    
    return final_pool_indexes
