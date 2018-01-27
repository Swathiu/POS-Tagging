# POS-Tagging
Tagging Part of Speech for a series of Sentences

Baseline System - As a first step, a  “Most Frequent Tag” system was implemented. This was the baseline system for development of more advanced tagging system. It served as a measure for calculating the accuracy of the system implemented using “Viterbi Algorithm”. In this baseline system, given a input word and list of tags associated with it in the training set, the word was assigned a tag which was most frequently  associated with it. It was implemented using python lists and dictionaries. Accuracy obtained was 90%.
 
Viterbi Algorithm for POS Tagging – 
 
A Bigram POS Tagging system was implemented next using Viterbi Algorithm. Transition Probability Matrix (Tag vs Tag) was created using the bigram counts from the training set. Then a Emission Matrix (Word vs Tag) was created using the counts from the training file. The probability estimates for each P(Tag|Previous Tag) and P(Word | Tag) was calculated and inserted into the matrices. “.” Was considered as a final state. 
 
Since the Bigram tag model had many null values, Laplace Smoothing was implemented by adding one to all bigram counts before normalizing the matrices.  
 
To deal with the unknown words, basic morphological analysis was used. Furthermore, If the word did not fit into any of the tags assigned present in morphological analysis,  It was given an probability equal to the minimum probability equal to minimum values of all the values in the transition probability matrix and was assigned the corresponding tag. 
 
A Viterbi decoder was implemented using the algorithm and was tested on the training set. The training set was divided 80-20 ratio and Viterbi algorithm was trained using 80% data and tested on 20% data(unseen).  It will work fairly well on unseen data. Accuracy obtained in this case was around 91%.
