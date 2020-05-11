import utilities

def parse_story (file_name):
    '''
    (string) -> (list)
    
    Returns an ordered list of words with bad characters processed (removed) from the textin the file given by file_name.
    
    >>>parse_story('test_text_parsing.txt')
    ['the', 'code', 'should', 'handle', 'correctly', 'the', 'following', ':', 'white', 'space', '.', 'sequences', 'of', 'punc    tuation', 'marks', '?', '!', '!', 'periods', 'with', 'or', 'without', 'spaces', ':', 'a', '.', '.', 'a', '.', 'a', "don't    ", 'worry', 'about', 'numbers', 'like', '1', '.', '5', 'remove', 'capitalization']
    ''' 
    with open (file_name) as story:
        lines = story.read().split()
        lines = [i.lower() for i in lines]
        for char in utilities.VALID_PUNCTUATION+utilities.BAD_CHARS:
            contin = True
            while contin:
                final = []
                for i in range (len(lines)):
                    if char in lines[i]:
                        index = lines[i].index(char)
                        str1= lines[i][:index]
                        if (index != len(lines) - 1):
                            str2= lines[i][index+1:]
                        else:
                            str2 = ''
                        final.extend([str1, char, str2])
                    else:
                        final.append(lines[i])
                final = [i for i in final if i != '']
                if final == lines:
                    contin = False
                else:
                    lines = final
    for char in utilities.BAD_CHARS:
        while char in lines:
            lines.pop(lines.index(char))             
    return lines
    
def get_prob_from_count(counts):
    '''
    (list) -> (list)
    
    Return a list of probabilitiesderived from counts. Countsis a list of counts  of occurrences of a token after the  previous n-gram.You should  not  round  the probabilities
    
    >>>get_prob_from_count([10, 20, 40, 30])
    [0.1, 0.2, 0.4, 0.3]
    '''
    temp = [0]*len(counts)
    for i in range (len(counts)):
        temp[i] = counts[i]/sum(counts)
    return temp

def build_ngram_counts(words, n):
    '''
    (list) -> (dict)
    
    Return a dictionary of N-grams (where N=n) and the counts  of the  words  that follow  the N-gram. The key  of  the  dictionary will be  the  N-gram in a tuple.  The  corresponding  value will be a list containing two  lists. The first list contains the words and the second list contains the corresponding  counts.
    
    >>>build_ngram_counts(words, 2)
    {(‘the’, ‘child’): [[‘will’, ‘can’], [1, 1]],(‘child’, ‘will’): [[‘go’], [1]], (‘will’, ‘go’): [[‘out’], [1]], (‘go’, out’): [[‘to’], [1]],(‘out’, ‘to’): [[‘play’], [1]], (‘to’, ‘play’): [[‘,’], [1]], (‘play’, ‘,’): [[‘and’], [1]], (‘,’, ‘and’): [[‘the’], [1]], (‘and’, ‘the’): [[‘child’], [1]], (‘child’, ‘can’): [[‘not’], [1]], (‘can’, ‘not’): [[‘be’], [1]], (‘not’, ‘be’): [[‘sad’], [1]], (‘be’, ‘sad’): [[‘anymore’],[1]],(‘sad’, ‘anymore’): [[‘.’], [1]]}
    '''
    list_of_nonunique_ngrams = [[] for i in range((len(words) - n))]
    for i in range (len(words)-n):
        list_of_nonunique_ngrams[i] = tuple(words[i:i+n])
    list_of_unique_ngrams = list(set(list_of_nonunique_ngrams))
    next_words = [[] for i in range(len(list_of_unique_ngrams))]
    occurences = [[] for i in range(len(list_of_unique_ngrams))]
    for i in range (len(list_of_nonunique_ngrams)):
        next_word = words [i+n]
        if next_word not in next_words[list_of_unique_ngrams.index(tuple(words[i:i+n]))]:
            next_words[list_of_unique_ngrams.index(tuple(words[i:i+n]))].append(next_word)
            occurences[list_of_unique_ngrams.index(tuple(words[i:i+n]))].append(1)
        else:
            print ('Here')
            occurences[list_of_unique_ngrams.index(list_of_nonunique_ngrams[i])][next_words[list_of_unique_ngrams.index(list_of_nonunique_ngrams[i])].index(next_word)] += 1
    mydict = {}
    for i in range (len(list_of_unique_ngrams)):
        mydict[list_of_unique_ngrams[i]] = [next_words[i], occurences[i]]
    return mydict

def prune_ngram_counts (counts, prune_len):
    '''
    (dict, int) -> dict
    
    Return a dictionary of N-grams and counts  of words with lower frequency (i.e. occurring less often) words  removed. 
    
    >>>ngram_counts= {(‘i’, ‘love’): [[‘js’, ‘py3’, ‘c’, ‘no’], [20, 20, 10, 2]],(‘u’, ‘r’): [[‘cool’, ‘nice’, ‘lit’, 'kind’], [8, 7, 5, 5]],('toronto’, ‘is’): [[‘six’, ‘drake’], [2, 3]]}
    >>>prune_ngram_counts(ngram_counts, 3)
    {(‘i’, ‘love’): [[‘js’, ‘py3’, ‘c’], [20, 20, 10]],(‘u’, ‘r’): [[‘cool’, ‘nice’, ‘lit’, 'kind’], [8, 7, 5, 5]],('toronto’, ‘is’): [[‘six’, ‘drake’],[2, 3]]}
    '''
    for key in counts:
        temp = counts[key]
        contin = True
        while contin:
            curr = temp[1]
            for i in range (len(temp[1])-1):
                if temp[1][i] < temp[1][i+1]:
                    temp[1][i], temp[i][i+1] = temp[1][i+1], temp[i][i]
            if (temp[1] == curr):
                contin = False
        if prune_len <= len(temp[1]):
            maximum = temp[1][prune_len-1]
            for i in range (len(temp[1])):
                if (temp[1][i] < maximum):
                    del temp[1][i]
                    del temp[0][i]
        counts[key] = temp
    return counts
  
def probify_ngram_counts(counts):
    '''
    (dict) -> (dict)
    
    Takea  dictionary  of N-grams  and  counts  and  convert the  counts  to  probabilities.
    
    >>>probify_ngram_counts(ngram_counts)
    {(‘i’, ‘love’): [[‘js’, ‘py3’, ‘c’], [0.4, 0.4, 0.2]],(‘u’, ‘r’): [[‘cool’, ‘nice’, ‘lit’, 'kind’], [0.32, 0.28, 0.2, 0.2]],('toronto’, ‘is’): [[‘six’, ‘drake’], [0.4, 0.6]]}
    '''
    for key in counts:
        counts[key][1] = get_prob_from_count (counts[key][1])
    return counts

def build_ngram_model(words, n):
    '''
    (list) -> (dict)
    
    Create  and  return  a  dictionary  of  the  format  given  above  in probify_ngram_counts.  This dictionary is your  final model that will be used  to auto-generate text.
    
    >>>words = [‘the’, ‘child’, ‘will’, ‘the’, ‘child’, ‘can’, ‘the’, ‘child’, ‘will’, ‘the’, ‘child’, ‘may’,‘go’, ‘home’, ‘.’]
    >>>build_ngram_model(words, 2)
    {(‘the’, ‘child’): [[‘will’, ‘can’, ‘may’], [0.5, 0.25, 0.25]],(‘child’, ‘will’): [[‘the’], [1.0]],(‘will’, ‘the’): [[‘child’],[1.0]],(‘child’, ‘can’): [[‘the’], [1.0]],(‘can’, ‘the’): [[‘child’], [1.0]],(‘child’, ‘may’): [[‘go’], [1.0]],(‘may’, ‘go’): [[‘home’], [1.0]],(‘go’, ‘home’): [[‘.’], [1.0]]}
    '''
    return probify_ngram_counts(prune_ngram_counts (build_ngram_counts(words, n), 15))

def gen_bot_list(ngram_model, seed, num_tokens=0):
    '''
    (dict, tuple) -> (list)
    
    Returns a randomly generated list of  tokens  (strings) that starts  with the  N tokens  in seed, selecting  all subsequent  tokens  using gen_next_token.
    '''
    n = len(seed)
    words = list(seed)
    if (len(words) > num_tokens):
        return words[:num_tokens]
    current = tuple(words[-1*n:])
    while len(words) < num_tokens:
        if tuple(words[-1*n:]) in ngram_model.keys():
            words.append(utilities.gen_next_token(current, ngram_model))
            current = tuple(words[-1*n:])
        else:
            return words
    return words

def gen_bot_text(token_list, bad_author):
    '''
    (list) -> (string)
    
    If bad_author is True,  returns  the   string  containing  all  tokens   in token_list, separated  by a space.Otherwise, returns  this  string  of  text,  respecting  some grammar rules
    
    >>>token_list= ['this', 'is', 'a', 'string', 'of', 'text', '.', 'which', 'needs', 'to', 'be', 'created', '.']
    >>>gen_bot_text(token_list, False)
    'This is a string of text. Which needs to be created.'
    '''
    if bad_author:
        mystr = ''
        for word in token_list:
            mystr += token_list[i] + ' ' # will give end space, remove or no?
        return mystr
    cases = [j.lower() for j in utilities.ALWAYS_CAPITALIZE]
    for i in range (len(token_list)):
        if (token_list[i] in cases):
            token_list[i] = utilities.ALWAYS_CAPITALIZE[cases.index(token_list[i])]
    mystr = ''
    for i in range (len(token_list)):
        mystr += token_list[i].strip() + ' '
    for char in utilities.END_OF_SENTENCE_PUNCTUATION:
        mylist = mystr.split (char)
        mystr = ''
        for i in range (len(mylist)):
            temp = list(mylist[i].strip())
            if temp != []:
                temp[0] = temp[0].upper()
            tempstr = ''
            for j in range (len(temp)):
                tempstr += temp[j]
            mystr += tempstr + char + ' '
        mystr = mystr[:-2]
    list2 = list(mystr)
    for i in range (len(list2) - 1):
        if (list2[i] == ' ' and list2[i+1] in utilities.VALID_PUNCTUATION):
            list2[i] = ''
    mystr = ''
    for i in range (len(list2)):
        mystr += list2[i]
    return mystr

def write_story(file_name, text, title, student_name, author, year):
    '''   
    Writes the text to  the file with name file_name.
    '''
    with open(file_name, 'w') as f:
        for i in range (10):
            f.write('\n')
        f.write (title + ': ' + str(year) + ', UNLEASHED\n')
        f.write (student_name + ', inspired by ' + author + '\n')
        f.write ('Copyright year published (' + str(year) + '), publisher: EngSci press\n')
        for i in range (17):
            f.write('\n')
        
        words = text.split()
        i = 0
        count_line = 0
        chapter = 1
        while i < len(words):
            stringlen = 90
            temp = ''        
            if count_line % 360 == 0:
                f.write('CHAPTER ' + str(chapter) + '\n\n')
                chapter+=1
                count_line+=2            
            while stringlen >= len(words[i]):
                temp += words[i] + ' '
                stringlen -= (len(words[i])+1)   
                i+=1
                if i == len(words):
                    break
            f.write (temp.strip()+ '\n')
            count_line += 1
            if count_line % 30 == 28:
                f.write('\n' + str(int(count_line/30)+1) + '\n')
                count_line += 2
        for i in range (29-(count_line%30)):
            f.write ('\n')
        f.write(str(int(count_line/30)+1))
        f.write ('\n')
            
if __name__ == "__main__":
    '''ngram_model = {('the', 'child'): [['will', 'can','may'], [0.5, 0.25, 0.25]], ('child', 'will'): [['the'], [1.0]], ('will', 'the'): [['child'], [1.0]], ('can', 'the'): [['child'], [1.0]],('child', 'may'): [['go'], [1.0]],('may', 'go'): [['home'], [1.0]], ('go', 'home'): [['.'], [1.0]] }
    random.seed(10)
    print(gen_bot_list(ngram_model, ('hello', 'world')))
    print(gen_bot_list(ngram_model, ('hello', 'world'), 5))
    print(gen_bot_list(ngram_model, ('the', 'child'), 5))
    print(gen_bot_list(ngram_model, ('the', 'child'), 5))VALID_PUNCTUATION = ['?', '.' , '!', ',', ':', ';']
    token_list = ['this', 'is', 'a', 'string', 'of', 'text', '.', 'which', 'needs', 'to', 'be', 'created', '.', 'george']    
    print(gen_bot_text(token_list, False))'''
    text = ' '.join(parse_story('308.txt'))
    write_story('testing2.txt', text, 'Three Men in a Boat', 'Jerome K. Jerome', 'Jerome K. Jerome', 1889)
    token_list = parse_story("308.txt")
    text = gen_bot_text(token_list, False)
    write_story('test_gen_bot_text_student.txt', text, 'Three Men in a Boat', 'Jerome K. Jerome', 'Jerome K. Jerome', 1889)
