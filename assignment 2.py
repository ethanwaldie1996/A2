'''Semantic Similarity: 
For a given text file, builds semantic descriptors for all words in a given
text file. Using this semantic descriptor, returns most similar word to the
each word in question and checks whether it is the right answer, returning 
the percentage of questions answered correctly.

Authors: Andrej Janda, Ethan Waldie. Last modified: Nov. 4, 2014.
'''

import math


def norm(vec):
    '''Return the norm of a vector stored as a dictionary,
    as described in the handout for Project 2.
    '''
    
    sum_of_squares = 0.0  # floating point to handle large numbers
    for x in vec:
        sum_of_squares += vec[x] * vec[x]
    
    return math.sqrt(sum_of_squares)


def cosine_similarity(vec1, vec2):
    '''Return the cosine similarity of sparse vectors vec1 and vec2,
    stored as dictionaries as described in the handout for Project 2.
    '''
    
    dot_product = 0.0  # floating point to handle large numbers
    for x in vec1:
        if x in vec2:
            dot_product += vec1[x] * vec2[x]
    
    return dot_product / (norm(vec1) * norm(vec2))


def get_sentence_lists(text):
    """ Return a new list of every sentence as an element in that list. Each 
    sentence element is split up into its individual words as individual
    strings. Opens file and splits it up into a list of all sentences as
    elements in that list.
    
    Arguments:
    text -- list
    """
   
    sentances = [] #Empty list will store the sentances
    
    
    lastperiod = 0 #Store the location in the text of the last sentance
    
    for i in range(len(text)):
        
        #if the word contains a period, remember punctuation was not 
        #stripped
        if charactercheck(text[i]):
            
            tmp = [] #temporay list to store each sentence
            
            
            if lastperiod == 0: #If first sentance
                
                #Add words from the first word to the end of this 
                #first sentance 
                for x in range (i+1):
                    
                    if text[x].find("'") > 0: #
                        #Set temporary string to hold
                        tmpstr = text[x].split("'") 
                        for string in tmpstr:
                            tmp.append(remove(string))
                    #Make sure empty strings are not included
                    elif remove(text[x]).isnumeric != True:
                        if remove(text[x]) != "":
                            tmp.append(remove(text[x]))
            else:
                #If not first sentance, Add words from the last sentance
                #period to the end of this sentance to the tmp list
                for u in range(lastperiod + 1, i+1):
                    #search for words with apporstafies in the middle
                    if text[u].find("'") > 0:
                        tmpstr = text[u].split("'")
                        for string in tmpstr:
                            tmp.append(remove(string)) 
                            
                    #Removes all strings that contain numbers
                    elif remove(text[u]).isnumeric() != True:
                        if remove(text[u]) != "":
                            tmp.append(remove(text[u]))
                    
            #append the tmp list to the sentances list
            if tmp != []:
                sentances.append(tmp)
            
            #set this period to be the last known period.
            lastperiod = i   
    
    #Returns the new list of all the sentences
    return sentances
                
        


def get_sentence_lists_from_files(filenames):
    '''Return a list of all the sentences with the individual words as
    strings in the elements of the list.
    
    Arguements:
    filenames -- text file
    '''
    #Open the file as a list of all the words as strings as its elements in
    #the list. Call function text_to_words(filenames):
    text = text_to_words(filenames)
    
    #turn the list into a list of all the sentences as the elements
    return get_sentence_lists(text)


def build_semantic_descriptors(sentences):
    '''Return a dictionary with the semantic descriptor of everyword. This
    semantic descriptor is stored as a value for the keyword in the dictonary
    
    Arguements
    sentences -- list
    '''
    
    #set new variable "d" to be the dictionary with every word in sentences
    #as a key and an emtpy dictionary as it's value
    #calls words_in_text(): to create this dictionary
    
    d = words_in_text(sentences)
    
    #For all keys in the dictionary of all the words in sentences, finds
    #the number of times each word appears in the same sentence as the keyword
    
    for keyword in d.keys():

        
        #create tempary dictionary to hold the values of frequency of 
        #everyword so that it can be added to its appropriate key in the 
        #dictionary
        tmp = {}
        
        #This section of for-loops goes into each word in each sentence and
        #adds the frequency of the the words in each sentence into the 
        #dictionary for each word
        
        #For every sentence in sentences
        for sentence in sentences:
            
            #if keyword in each sentence
            if keyword in sentence:
                
                #for every word in the sentence, add the frequency of that
                #word in that sentence to the dictionary for the keyword
                for word in sentence:
                    
                    #creates an input for that word if it does not exist
                    if word not in tmp.keys():
                        tmp[word] = 1
                        
                    #Updates the frequency of the word in the sentence
                    else:
                        tmp[word] += 1
                        
                #deletes the word iself from the list
                if keyword in tmp.keys():
                    del tmp[keyword]
                
        d[keyword] = tmp #Set the dictionary at that word equal to the
                         #semantic descriptor for that keyword
        
    return d  #Return the semantic descriptor
    
        
def most_similar_word(word, choices, semantic_descriptors):
    '''Return the most smiliar word to the keyword
    
    Arguements:
    word -- string
    choices -- list
    semantic_descriptors -- dictionary
    '''
    
    #Create empty list to store the cosine similarty for each choice
    sim = []
    
    print("Called")

    for choice in choices:
        #appends the cosine similarity of each respective choice
        #If the 
        if word in semantic_descriptors.keys() and choice in \
           semantic_descriptors.keys():
            
            sim.append(cosine_similarity(semantic_descriptors[word],\
            semantic_descriptors[choice]))
        else:
            sim.append(-1) #If the word is not in the semantic descrpiptor
                           #return -1 so that it does not get
    if -1 in sim:
        return "Word not in text"
    print(word, "Similarity", str(sim))
    
    #Set variable maxrun to store the highest similarity
    maxrun = 0
    
    pos = 0 #Stores the position of the word with the highest similarity
    for i in range(len(sim)): 
        if sim[i] > maxrun: #checks if the similarity is a max
            maxrun = sim[i] #update the max similarity
            pos = i  #update the position of the highest similarity
    
    return choices[pos] #return the word with the highest similarity


def run_similarity_test(filename, semantic_descriptors):
    '''Retrun the percentage that the program guess the answers to the 
    TOFEL questions corretly.
    
    Arguements:
    filename -- text file
    Semantic_descriptor -- dictionary
    '''
    testcases = []     #Empty list stores the TOFEL Questions with answers
    correct = 0        #number of correct answers
    trials = 0         #number of trials run
    file = open(filename) #Open the text file with the TOFEL questions
    line_strings = file.readlines() #list of all lines as elements
    file.close()       #Close file being read
    
    #Checks to make sure semantic_descriptors is not an empty dictionary
    if len(semantic_descriptors.keys()) == 0:
        return 0
   
    
    for line in  line_strings:
        #appends testcases with a list of all the words in each line
        testcases.append(line.split())
    
    for test in testcases:
        choices = [] #Stores choices in each question
        
        #since first two elements are the question word and the answer
        #make choices any entry after those two elements
        for i in range(2, len(test)):
            choices.append(test[i])
        
        #Check if the question word is in the semantic descriptor
        if test[0] in semantic_descriptors.keys():
            
            #check which word is the most similar
            synonym = most_similar_word(test[0], choices, semantic_descriptors)
            if synonym == test[1]:
                print(test[1], "we chose", synonym)
                
                #If the program guessed correctly, update number of correct
                #guesses
                correct += 1
        
        trials +=1 #Updates the number of trials run
        
    print(trials, "tests:", len(testcases))
    
    #Calculates the percentage that the program guesses correctly
    if trials != 0: # cannot divide by zero if trials is not updated
        percentage = (correct/trials)*100 
    
    return percentage   
    

def text_to_words(text):
    '''Return a list from a file with all words as strings in the list. 
    
    Arguements:
    text -- text file
    '''
    return open(text, "r", encoding="utf-8").read().split()

def remove(word):
    '''Return the word without any extra characters
    
    Arguemnts:
    word -- string
    '''
    return word.lower().strip("?,.!;:+()-/*--'")

def charactercheck(word):
    '''Return a booliean. True if ".", "!", "?" are in the word and 
    false otherwise
    
    Arguements:
    word -- string
    '''
    return ("." in word or "!" in word or "?" in word)

def words_in_text(sentances):
    '''Return a dictionary with all the words in the text as keys and 
    an empty dictionary as their values
    
    Arguments:
    sentances -- list
    '''
    
    words = {}   #set empty dictionary to store all words
    
    for sentance in sentances:
        for word in sentance:
            if word not in words.keys():
                if word != '':
                    words[word] = {}  #Sets the value to be an empty dictionary
                
    return words


if __name__ == '__main__':
    
    #Question 3 this code reads in war and peace and then appends the sentences
    #from swan lake to War and Peace.
    #Then it builds sematic descriptors
    #then it runs a similarity test using then words found in the test file.
    
    #sentances = get_sentence_lists_from_files("War and Peace.txt")
    
    sentances2 = get_sentence_lists_from_files("Swann's Way.txt")
    
    merge_sentances = sentances2
        
    f = open('sentances.txt', 'w', encoding="utf-8")
    f.write(str(merge_sentances))
    f.close()   
    
    print("Building")
    
    sem_des = build_semantic_descriptors(merge_sentances)
    
    f = open('semantic.txt', 'w', encoding="utf-8")
    f.write(str(sem_des))
    f.close()    
    
    print(run_similarity_test('testingdata.txt', sem_des))
    
    
    #Testing strategy:
    #Test all boundry cases for each function 
    #Since many functions are soley for the use of another function, those
    #functions are tested by testing the large functions for which the 
    #smaller functions function. Thus if an error occurs, it can be 
    #traced back to that function
    
    
#############################################################################
#Boundary cases for get_sentences_lists()
#Test by calling a text file which tests many cases

    print("\ntesting get_sentences_lists()")
    test_n = 1
       
    #This is the expected output of when the function runs the test file
    expected =     [['this', 'file', 'contains', 'testing', 'cases', 'for', 
                'get', 'sentance', 'lists'], ['hello'], ['my', 'name', 
                'is', 'ethan'], ['testing', 'functions'], 
                ['is', 'a', 'good'], ['job'], ['and'], 
                ['must'], ['be', 'done'], ['to', 'get'], ['a', 'good'], 
                ['mark'], ['in', 'csc'], ["don", "t", "school", "s"]]    
    
    #run the test file
    sentences = get_sentence_lists(text_to_words("get_sentence_lists_test1.txt"))

    #-------------------------------------------------------------------------
    #Test 1: Tests whether multiple characters will be stripped and not be 
    #included in the list
    #could be an issue because it could also not strip all the caracters 
    #causing words that are the same to register as different
    
    forbid = [" ", ".", "?", "/", "!", ";", ":"]
    for sentence in sentences:
        for word in sentence:
            for e in forbid:
                if e in word:
                    print('TEST', test_n, ": False")

    print('TEST', test_n, ": True")
    test_n += 1
    
    #-------------------------------------------------------------------------
    #Test 2: Tests for sentences without words and only characters that are
    #stripped. Should not be included in the list
    #empty lists could cause the program to glitch and feed wrong information
    #to subsequent functions
    
    for sentence in sentences:
            for word in sentence:
                if '' == word:
                    print('TEST', test_n, ": False")
                    break
                
    print('TEST', test_n, ": True")
    test_n += 1
    
    #-------------------------------------------------------------------------
    #Test 3: Tests to make sure that numbers are not returned in the list
    #numbers cannot have synonyms and therefore could cause an error in the
    #result if not removed
    
    for sentence in sentences:
                for word in sentence:
                    if word.isdecimal() == True:
                        print('TEST', test_n, ": False")
                        break
    print('TEST', test_n, ": True")
    test_n += 1    
    
    #-------------------------------------------------------------------------
    #Test 4: Checks if list matches referance
    print('TEST', test_n, ":", expected == sentences)
    test_n += 1        

#############################################################################
#Test cases for build_semantic_descriptors
    #Comprises of two tests
    print("\ntesting build_semantic_descpriptors()")
    test_n = 1

    #-------------------------------------------------------------------------
    #TEST 1: Tests to see if every word in each sematnt descriptor shows up
    #at least once in the same sentence as the key word
    
    words_in_file = text_to_words("build_semantic_descirptors_test1.txt")
    
    text = get_sentence_lists_from_files("build_semantic_descirptors_test1.txt")
    
    sem_des = build_semantic_descriptors(text)
    
    res = {}
    
    #Go through all the words with semantic descriptor vectors
    for keyword in sem_des.keys():
        #go through all the words that it says appears in the same sentance
        for word in sem_des[keyword].keys():
            
            #go through all the sentances in the text
            for sentance in text:
                #if the keyword we are looking for is in the same sentance 
                #as the word we are on in its simliarity vector
                #at least once, the res dictionary at that keyword will be True
                if keyword in sentance and word in sentance:
                    res[keyword] = True
    
    #As long as all items in res are True this will return True
    #Because res is a dictionary any problem words can be easily identifyed
    #this assists in troubleshooting and dubugging
    print ('TEST', test_n, ':', False not in res.items())
    test_n += 1
    
    #-------------------------------------------------------------------------
    #TEST 2: checks that all words not in the description vector are not found 
    #in the same sentance as that word to save on processing
    #as this has many more calcualtions than the previous res will be a boolean
    
    res = {}
    
    #go through all keys in sem_des
    for keyword in sem_des.keys():
        #go through all unique words in text
        for word in words_in_text(text):
            #if the word is not in the list of words known to be in same 
            #sentance as keyword
            if word not in sem_des[keyword].items():
                #go look through all the sentances and check
                for sentance in text:
                    #if they are in the same sentanace add a False enrty to res
                    #at word
                    if word in sentance and keyword in sentance:
                        res[word] = False
    #print if res contains any False elements                     
    print ('TEST', test_n, ':', False not in res.items())
    

##########################################################################
#Testing most_simlar_word()   
#Tests a wide range of vectors and makes sure that the program picks the
#one with the highest similarity

#TEST OVERVIEW
#TEST 1: Both of the options are the same as the word, should pick a
#TEST 2: 
#TEST 3:
#TEST 4:
#TEST 5:
#TEST 6:



    print("\ntesting most_similiar_word()")
    
    sem_des = {"a":{"b":1, "c":1, "d":1, "e":1, "f":1 },
               "b":{"a":0, "c":1, "d":2, "e":3, "f":1 },
               "c":{"a":0, "b":1, "d":1, "e":1, "f":1 },
               "d":{"a":5, "b":6, "c":4, "e":2, "f":6 },
               "e":{"a":8, "b":4, "c":2, "d":1, "f":3 },
               "f":{"a":0, "b":1, "c":1, "d":1, "e":1,},
               }
    
    """
    These lists prepare words to compare with choices
    
    word -- [words to compare]
    
    choices -- [choices for corrisponding word]
    
    expected -- [expected answer]
    """
    
    word = ["a", "a", "a", "d", "e", "f"]
    
    choices = [["a", "a"],["c", "f"],["d", "f", "c"],["e", "b", "c"],
               ["d", "f"],["e", "b"]]
    
    expected = ["a", "c", "f", "e", "d", "b"]
    
    
    for test_n in range(len(word)):
        res = most_similar_word(word[test_n],choices[test_n],sem_des) 
        print("TEST ", test_n + 1, " : ", expected[test_n] == res )

    
    
#############################################################################
#Test cases for run_similarity_test()
#Tested using a testing file "run_similarity_test_test1.txt" with all test
#cases found inside

    print("\ntesting run_similarity_test()")
    test_n = 1
    
    sem_des = build_semantic_descriptors(text)
    
    #-------------------------------------------------------------------------
    #TEST 1: check if the choices do not contain the answer or if no choices
    #are given or if the question is given in other characters, whether the
    #program will return 0 percentage correct
    #If the questions don't contain the answer, then the question is 
    #inherently wrong and needs to return nothing
    
    check = run_similarity_test('run_similarity_test_test1.txt', sem_des)
    if check == 0:
        test_boolean = True
    else:
        test_boolean = False
    print ('TEST', test_n, ':', test_boolean)
    test_n += 1
    
    #-------------------------------------------------------------------------
    #TEST 2: Check whether numbers in the file will cause an error
    #numbers should not be registered as questions since they cannot have
    #synonyms. This would cause large problems in the code.
    
    check = run_similarity_test('run_similarity_test_test1.txt', sem_des)
    
    #Should give zero percent correct since the semantic descriptor has no
    #data for numbers
    if check == 0:
        test_boolean = True
    else:
        test_boolean = False    
    
    print ('TEST', test_n, ':', test_boolean)
    test_n += 1    
    
    
    #-------------------------------------------------------------------------
    #TEST 3: Check if when the function is fed an empty list as the semantic
    #descriptor
    #Should return a value of zero as the percentage
    #possibility of an empty list being fed into the program could cause
    #a list index out of range error
    
    sem_des2 = {}
    
    test = run_similarity_test('run_similarity_test_test1.txt', sem_des2)
    if test == 0:
        test_boolean = True
    else:
        test_boolean = False
    print ('TEST', test_n, ':', test_boolean)



