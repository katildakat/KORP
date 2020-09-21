import sys
import pandas as pd
import glob
import io

def check_corpus(corpus_path, csv_df):
    """
    This function compares the number of tokens in subcorpora we've collected
    to the number of 'match' tokens in the CSV files.

    INPUT: 
    corpus_path - path to .txt file of subcorpora 
    csv_df - dataframe with all csv files concatenated
    OUTPUT:
    result - a list containing:
      0. is_correct - True if number of 'match' tokens 
        matches the number of tokens in the subcorpora .txt
      1. len(match_tokens) - number of 'match' tokens in csv_df
      2. n - number of whitespace separated tokens in subcorpora sentences
      3. k - number of whitespaces in 'match' tokens
    """
    # take the sentences that you've collected into a .txt file
    f = io.open(corpus_path, 'r', encoding='UTF-8')
    sentences = f.readlines()
    f.close()
    
    # count whitespace separated tokens in those sentences
    n = 0
    for sent in sentences:
        n += len(sent.split())
    
    # get match tokens and count how many whitespaces they contain 
    match_tokens = csv_df['match'].tolist()
    k = 0
    for word in match_tokens:
        if len(word.split()) > 1:
            k+= len(word.split()) - 1 # count the whitespaces
        
    # check the number of tokens
    is_correct = (n - k) == len(match_tokens)

    result = [is_correct, len(match_tokens), n, k]

    return result

def write_into_corpus(paths, corpus_file_name, check):
    """
    This function concatenates Korp subcorpora CSV files into one dataframe, 
    selects only rows with empty left context,
    creats a column that contains full sentences,
    converts this column into a list of strings,
    writes this list into a .txt file with UTF-8 encoding, so that each sentences takes its own line. 
    If check is True, the function also compares the number of tokens in this .txt
    to the number of 'match' tokens in the CSV files.

    INPUT: 
    paths - paths to csv parts of subcorpora (sorted) 
    corpus_file_name - the name of output text file
    check - whether to check the number of tokens collected 
      vs the number of 'match' tokens in CSV files
    """
    paths 
    dfs = [pd.read_csv(paths[i]) for  i in range(len(paths))]
    df = pd.concat(dfs)
    df = df[df.match !='[omit copy]'] # this line helps with some korp mistake
    
    # selecting only text columns
    sentences = df[['left context','match','right context']]
    # selecting rows where 'match' starts the sentence (no left context)
    sentences = sentences[sentences['left context'].isnull()]
    # ignoring empty matches (if there are. korp has mistakes in some corpora)
    sentences = sentences[sentences['match'].notnull()]
    # converting empty cells into empty strings (for empty right contexts, if a sentence is one word)
    sentences = sentences.fillna('')
    # adding a column with full sentences
    sentences['full sentence'] = sentences['match'] + ' ' +  sentences['right context'] + '\n'
    
    # converting the column with sentences into a list
    corpus = sentences['full sentence'].tolist()
    # writing this list into a .txt file with UTF-8 encoding
    f = io.open(corpus_file_name+'.txt', 'w', encoding='UTF-8')
    f.writelines(corpus)
    f.close()

    if check:
      print(check_corpus(corpus_file_name+'.txt', df[df['match'].notnull()]))

def main(argv):

  # a name of the folder with csv parts of subcorpora
  if len(argv) == 1:
    corpus_level = str(argv[0])
    check = True
  else:
    corpus_level = str(argv[0])
    check = bool(argv[1])

  # collects paths to csv parts of subcorpora
  paths = sorted(glob.glob(corpus_level+'/korp*'))

  # write a subcorpus into a file
  write_into_corpus(paths, corpus_level, check)

if __name__ == '__main__':
  main(sys.argv[1:])