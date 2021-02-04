# Problem Set 4A
# Name: <your name here>
# Collaborators:
# Time Spent: x:xx
from memoization import cached
from functools import lru_cache
import time



# def swap(sequence, index_i, index_j):
#     '''
#     sequence is assumed to be an array of the characters to swap
#     '''
#     temp = sequence[index_i]
#     sequence[index_i] = sequence[index_j]
#     sequence[index_j] = temp
#     # return sequence
    
# def clean(container):
#     new_container = []
#     # print(container)    
#     for i in container:
#         s = ''
#         for o in i:
#             if o.isalpha():
#                 s += o
#         new_container.append(s)
        
#     # print(new_container)
#     return new_container
    
@cached
# @lru_cache
def get_permutations(sequence):   #curr_index=0, container = ''
    '''
    Enumerate all permutations of a given string

    sequence (string): an arbitrary list string to permute. Assume that it is a
    non-empty list.  

    You MUST use recursion for this part. Non-recursive solutions will not be
    accepted.

    Returns: a list of all permutations of sequence

    Example:
    >>> get_permutations('abc')
    ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']

    Note: depending on your implementation, you may return the permutations in
    a different order than what is listed here.
    '''
    if len(sequence) == 0:
        return ['']
    prev_list = get_permutations(sequence[1:len(sequence)])
    next_list = []
    for i in range(0,len(prev_list)):
        for j in range(0,len(sequence)):
	           new_str = prev_list[i][0:j]+sequence[0]+prev_list[i][j:len(sequence)-1]
               #prev_list[i][0:j] is accessing a nested list
	           if new_str not in next_list:
	               next_list.append(new_str)
    return next_list
# start = time.time()	
# print(get_permutations('1234567'))
# end = time.time()
# time_taken = end - start
# print(f'\nTime taken: {time_taken}')

    

# if __name__ == '__main__':
#     # EXAMPLE
#     example_input = list('abc')
#     print('Input:', example_input)
#     print('Expected Output:', ['abc', 'acb', 'bac', 'bca', 'cab', 'cba'])
#     print('Actual Output:') 
#     o = get_permutations(example_input)
    
#     ex_in = list('123')
#     print('Input:', ex_in)
#     print('Expected Output:')
#     print('Actual Output:') 
#     get_permutations(ex_in)
    
#     ex_in = list('son')
#     print('Input:', ex_in)
#     print('Expected Output:')
#     print('Actual Output:')
#     get_permutations(ex_in)
#    # Put three example test cases here (for your sanity, limit your inputs
#    to be three characters or fewer as you will have n! permutations for a 
#    sequence of length n
