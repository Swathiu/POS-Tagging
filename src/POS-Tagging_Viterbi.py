from collections import defaultdict
from collections import Counter
from itertools import count
import numpy as np
import pandas as pd 
import pprint
import io 
from sklearn.preprocessing import normalize
import sys
from collections import OrderedDict
import re
Tagger_Dict = {}
Tagger_Dict_List = {}
temp_dict = {}
Tagger_Dict = defaultdict(list)
Tag_List = []
Word_List = []
Tag_Count_List = []
Count_Tags = {}
Word_Count_List = []
for line in open('berp-POS-training.txt','r').readlines():
	if line.strip():
		word_split = line.split()
		if word_split[2] not in Tag_List:
			Tag_List.append(word_split[2])


Test_File = sys.argv[1]


#For transition probability matrix, getting the count of each of unique tags
for line in open('berp-POS-training.txt','r').readlines():
	if line.strip():
		word_split = line.split()
		Tag_Count_List.append(word_split[2])

#Count of each tag for Estimation Probability -
Count_Tags=Counter(Tag_Count_List)
count_PRP = {}



indices = defaultdict(count().next)
unique_count = len(set(Tag_Count_List))
b = [[0 for _ in xrange(unique_count)] for _ in xrange(unique_count)]
for (x, y), c in Counter(zip(Tag_Count_List, Tag_Count_List[1:])).iteritems():
	b[indices[x]][indices[y]] = c
sorted_indices = sorted(indices, key=indices.get)
df = pd.DataFrame(b,index=sorted_indices, columns=sorted_indices)
df.to_csv('df.csv', index=True, header=True, sep=' ')
b = np.matrix(b);
row_sum = b.sum(axis=1)

#Transition Probability Matrix - Row_Normalized
Row_Normalized = normalize(b, norm='l1', axis=1)
Row_Normalized = np.matrix(Row_Normalized, dtype=np.float)
np.set_printoptions(precision=10,
                       threshold=10000,
                       linewidth=150,
			suppress = True)


#Implement Laplace smoothing for Transition Probability Matrix
df_Smoothed_Transition_Probabilty_Matrix = df + 1
df_Smoothed_Transition_Probabilty_Matrix["Row_sum_TPMatrix"] = df_Smoothed_Transition_Probabilty_Matrix.sum(axis=1)
df_Smoothed_Transition_Probabilty_Matrix["Row_sum_TPMatrix"] = df_Smoothed_Transition_Probabilty_Matrix["Row_sum_TPMatrix"] + unique_count
for x in sorted_indices:
    df_Smoothed_Transition_Probabilty_Matrix[x] /= df_Smoothed_Transition_Probabilty_Matrix['Row_sum_TPMatrix']
df_Smoothed_Transition_Probabilty_Matrix.round(10)
df_Smoothed_Transition_Probabilty_Matrix = df_Smoothed_Transition_Probabilty_Matrix.drop(labels='Row_sum_TPMatrix', axis=1) 
df_Smoothed_Transition_Probabilty_Matrix.to_csv('df_Smoothed_Transition_Probabilty_Matrix.csv', index=True, header=True, sep=' ')

#Create a dictionary with keys as words and values as Tags
for line in open('berp-POS-training.txt','r').readlines():
	if line.strip():
		word_split = line.split()
		if  word_split[1] in Tagger_Dict:
			Tagger_Dict[word_split[1]].append(word_split[2])
						
		else:
			Tagger_Dict[word_split[1]] = [word_split[2]]

Tagger_Dict_Word_Tag_Count = {}

for key in Tagger_Dict:
        data = dict(Counter(Tagger_Dict[key]))
	Tagger_Dict_Word_Tag_Count[key] = data

#Count the Maximum tags that occur for a particular key, create a new dictionary with this (Word, Tag) pair
for key in Tagger_Dict:
        data = Counter(Tagger_Dict[key])
	Tagger_Dict_List[key] = data.most_common(1)[0][0]

for line in open('berp-POS-training.txt','r').readlines():
	if line.strip():
		word_split = line.split()
		Word_Count_List.append(word_split[1])

for line in open('berp-POS-training.txt','r').readlines():
	if line.strip():
		word_split = line.split()
		if word_split[1] not in Word_List:
			Word_List.append(word_split[1])

#Emission Matrix 
df = pd.DataFrame.from_dict(Tagger_Dict_Word_Tag_Count, orient='columns')
df = df.replace(np.nan, 0)
df["row_sum"] = df.sum(axis=1)
df_EmissionMatrix = df.loc[:,"'":"zachary's"].div(df["row_sum"], axis=0)
df_EmissionMatrix.round(10)
df_EmissionMatrix.to_csv('emission_probability.csv', index=True, header=True, sep=' ')

#Viterbi Implementation
Best_Sequence = {}
Best_Sequence = OrderedDict()
Best_Tag_Dict = {}
Best_Tag_Dict = OrderedDict()


#Writing the word-tag pair to the Output File
def write_to_file(Sentence,Squence):

	index = 1
	with open("Upadhyaya-Swathi-assgn2-test-output.txt",'a') as ofile:
				for word in Sentence:
					if word in Squence:
						temp = Squence[word]
        	        			ofile.write((str(index) + '\t' + word + '\t' + str(temp) + '\n'))
						index+=1
					else:
						print ("Word Not in TagList")
				ofile.write("\n")	
	
#Basic Morphological Analysis for unknown words
def Morphology_UnknownWords (UnknownWord):
	Interrogative_Pronoun_List = ['what','which','who','whom','whose']
	Wh_Adverb_List = ['why','where','when','how']
	Conjunction_List = ['both','and']
	Determiner_list = ['a','an','every','no','the','another','any','some','each','either','neither','that','this','these','those','nor']
	Interjection_List = ['aha','ahem','ahh','ahoy','alas','arg','aw','bam','bingo','blah','boo','cheers','congratulations','darn','duh','phew','yeah','yippee','oh','uh-huh','uh-oh','ugh','hello','hey','hi','please','uh','yes']
	Model_verb_list  = ['can','could','may','might','must','ought','shall','should','will','would']
	if re.match(r'(\d+)\.(\d+)+',UnknownWord):
		tag = 'CD'
		return tag
	elif re.match(r'(\d+)',UnknownWord):
		tag = 'CD'
		return tag
	elif re.match(r'[a-zA-Z]+er',UnknownWord):
		tag = 'JJR'
		return tag
	elif re.match(r'[a-zA-Z]+est',UnknownWord):
		tag = 'JJS'
		return tag		
	elif re.match(r'[a-zA-Z]+ing',UnknownWord): 
	        tag = 'VBG'
		return tag
	elif re.match(r'[a-zA-Z]+en',UnknownWord):
		tag = 'VBN'
		return tag
	elif re.match(r'[a-zA-Z]+able',UnknownWord):
		tag = 'RB'
		return tag	
	elif re.match(r'[a-zA-Z]+ed',UnknownWord):
		tag = 'VBD'
		return tag
	elif re.match(r"[a-zA-Z]+'s",UnknownWord):
		tag = 'POS'
		return tag
	elif UnknownWord in Interrogative_Pronoun_List:
		tag = 'WP'
		return tag	
	elif UnknownWord in Wh_Adverb_List:
		tag = 'WRB'
		return tag
	elif re.match(r"[a-zA-Z]+ly",UnknownWord):
		tag = 'RB'
		return tag
	elif UnknownWord in Determiner_list:
		tag = 'DT'
		return tag
	elif UnknownWord in Interjection_List:
		tag = 'UH'
		return tag
	elif UnknownWord in Conjunction_List:
		tag = 'CC'
		return tag
	elif UnknownWord in Model_verb_list:
		tag = 'MD'
		return tag
	else:
		return -1;
    

Best_Sequence = OrderedDict()
def viterbi_decoder(Sentence, taglist):
	Num_of_rows = len (taglist)
	Num_of_Columns = len (Sentence)	
	Viterbi_Matrix = pd.DataFrame(np.nan,index = taglist, columns = Sentence)
	rows = tuple(taglist)
	cols = tuple(Sentence)
	df_Viterbi = pd.DataFrame(Viterbi_Matrix, index=rows, columns=cols)
	df_Viterbi = df_Viterbi.replace(np.nan, 0)
	for each_tag in taglist:
		if Sentence[0] in Tagger_Dict_Word_Tag_Count:
			df_Viterbi.loc[each_tag:,Sentence[0]] = df_Smoothed_Transition_Probabilty_Matrix.get_value(".",each_tag) * df_EmissionMatrix.get_value(each_tag,Sentence[0])
		else:
			df_Viterbi.loc[each_tag:,Sentence[0]] = df_Smoothed_Transition_Probabilty_Matrix.get_value(".",each_tag)
	first_row_tag = df_Viterbi.idxmax(axis=0)[0]
	Best_Sequence[Sentence[0]] = first_row_tag 
	Possible_Path_Dict = {}
	Possible_Path_Dict = defaultdict(dict)
	taglist_values = []
	Possible_Values_Tag_Dict = {}
	k = 0
	l = 0
	for col_Size in range (1,Num_of_Columns):
		column_header = df_Viterbi.columns[col_Size]	
		if column_header in Tagger_Dict_Word_Tag_Count:				
			for each_tag in Tagger_Dict_Word_Tag_Count[column_header].keys():
				taglist_values.append(each_tag)
				i = 1
				for each_item in taglist_values:
					temp_str = str(each_item)					
					for k in range (0, Num_of_rows):
						if df_Viterbi.iloc[k][i-1] != 0:
							previous_tag = df_Viterbi.index[k]		 
							Possible_Values_Tag_Dict.update({temp_str : (df_Viterbi.iloc[k][i-1] * df_Smoothed_Transition_Probabilty_Matrix.get_value(previous_tag,temp_str) *  df_EmissionMatrix.get_value(temp_str,column_header))})
						else :
							continue
					maximum = max(Possible_Values_Tag_Dict, key=Possible_Values_Tag_Dict.get)	
					tag_index = df_Viterbi.index.get_loc(temp_str)
					word_index = df_Viterbi.columns.get_loc(column_header)
					df_Viterbi.iloc[tag_index][word_index] = Possible_Values_Tag_Dict[maximum]
					if column_header in Possible_Path_Dict:
						Possible_Path_Dict[column_header].update ({maximum:Possible_Values_Tag_Dict[maximum]})	
					else:
						Possible_Path_Dict.update ({column_header :{maximum:Possible_Values_Tag_Dict[maximum]}}) 
					Possible_Values_Tag_Dict.clear()
					taglist_values [:] = []
					i+=1
		else:
			Word_tag = Morphology_UnknownWords(column_header)
			if Word_tag != -1:
				Best_Sequence.update({column_header:Word_tag})
			else:
				Min_Value = df_Smoothed_Transition_Probabilty_Matrix.values.min()
				Min_Tag = df_Smoothed_Transition_Probabilty_Matrix.min(axis=1).idxmin()
				Best_Sequence.update({column_header:Min_Tag})
		for outer_key,inner_key in Possible_Path_Dict.items():	
			maximum = max(inner_key.values())
			for inside_key, inner_value in inner_key.iteritems():
 				   if inner_value == maximum:
					Best_Sequence.update({outer_key:inside_key})

	if test_file == True:
		write_to_file (Sentence,Best_Sequence)	
				
#Generating tags for TestFile
Sequence_Words_TestSet = []
for line in open(Test_File,'r').readlines():
	test_file = True
	if line.strip():
		word_split = line.split()
		if word_split[1] == ".":
			Sequence_Words_TestSet.append(word_split[1])
			viterbi_decoder(Sequence_Words_TestSet,sorted_indices)
			Sequence_Words_TestSet[:] = [] 
		else:
			Sequence_Words_TestSet.append(word_split[1])


	
