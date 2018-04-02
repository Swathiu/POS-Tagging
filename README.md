# POS-Tagging
Tagging Part of Speech for a series of Sentences

Baseline System - As a first step, a  “Most Frequent Tag” system is implemented. This is the baseline system for development of more advanced tagging system. It serves as a measure for calculating the accuracy of the system implemented using “Viterbi Algorithm”. In this baseline system, given a input word and list of tags associated with it in the training set, the word is assigned a tag which is most frequently  associated with it. It is implemented using python lists and dictionaries. Accuracy obtained is 90%.
 
Viterbi Algorithm for POS Tagging – 
 
A Bigram POS Tagging system is implemented next using Viterbi Algorithm. Transition Probability Matrix (Tag vs Tag) is created using the bigram counts from the training set. Then a Emission Matrix (Word vs Tag) is created using the counts from the training file. The probability estimates for each P(Tag|Previous Tag) and P(Word | Tag) is calculated and inserted into the matrices. “.” is considered as a final state. 
 
Since the Bigram tag model has many null values, Laplace Smoothing is implemented by adding one to all bigram counts before normalizing the matrices.  
 
To deal with the unknown words, basic morphological analysis is used. Furthermore, If the word did not fit into any of the tags assigned present in morphological analysis,  it is given an probability equal to the minimum probability equal to minimum values of all the values in the transition probability matrix and is assigned the corresponding tag. 
 
A Viterbi decoder is implemented using the algorithm and is tested on the training set. The training set is divided 80-20 ratio and Viterbi algorithm is trained using 80% data and tested on 20% data(unseen).  It will work fairly well on unseen data. Accuracy obtained in this case is 91%.
