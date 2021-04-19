# Email generator
# Generate email addresses and stores them in a csv file
# 
import glob, csv
import pandas as pd
from itertools import permutations, combinations, combinations_with_replacement
from lib.utils import df_read, df_write, add_domains, get_info
# from lib.utils import get_info
from lib.constants import ROLE_BASED_NAMES
# 
DATA_DIR = 'data/_dictionary/'
# 
# local_section@domain_section
# 
class Generator:
    def __init__(self, data_dir,local_max_length = 32, domain_max_length = 32):
      """
        Mail Generator class
        \n
        local_section@domain_section
        
      """
      # 
      self.data_dir = data_dir
      self.local_max_length = local_max_length
      self.domain_max_length = domain_max_length 
      
      # local section
      self.numbers = '0123456789'
      self.uppercase_letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' # not in use for permutation
      self.lowercase_letters = self.uppercase_letters.lower()
      self.local_section_symbols = '.-_'
      
      # 
      self.all = self.numbers + self.lowercase_letters + self.local_section_symbols
      self.alpha_numeric = self.lowercase_letters + self.numbers
      self.alpha_numeric_dash_symbol = self.lowercase_letters + self.numbers + '-'
      self.alpha_numeric_underscore_symbol = self.lowercase_letters + self.numbers + '_'
      self.alpha_numeric_dot_symbol = self.lowercase_letters + self.numbers + '.'
      
    # 
    def permutate(self,length: int):
      #
      if (length >= 5):
        raise NotImplementedError
      # 
      return pd.DataFrame(list(map(''.join, list(permutations(self.lowercase_letters,length)))),columns=['generated_strings']).drop_duplicates()

    # 
    def df_permutate(self, word: str):
      min_length = 1
      max_length = len(word) #maximum length
      # 
      all_df = pd.DataFrame(columns=['generated_strings'])
      # 
      for i in range(max_length):
        all_df.append(pd.DataFrame(list(map(''.join, list(permutations(word, i+1)))), columns=['generated_strings']).drop_duplicates(), ignore_index = True)
  
      # 
      return all_df.drop_duplicates()
    
    # 
    def df_combine(self, dataframe):
      # 
      all_df = pd.DataFrame(columns=['generated_strings'])
      # 
      for i in range(max_length):
        all_df.append(pd.DataFrame(list(map(''.join, list(permutations(word, i+1)))), columns=['generated_strings']).drop_duplicates(), ignore_index = True)
  
      # 
      return all_df.drop_duplicates()
    
    # 
    def from_dictionary(self):
      # 
      data_dir = self.data_dir + '/_dictionary/_data/'
      all_files = glob.glob(data_dir+'*.csv') + glob.glob(data_dir+'*.txt')
      df_from_each_file = (pd.read_csv(f, header = None, delimiter="\t", quoting=csv.QUOTE_NONE, encoding='ISO-8859-1').drop_duplicates() for f in all_files)
      # 
      df = pd.concat(df_from_each_file).drop_duplicates()
      df.columns = ['generated_strings']
      # 
      # df['generated_strings'].apply(lambda x: df.append(self.word_permutate(x), ignore_index = True))
      # 
      return df
    
    # 
    def scraper(self):
      bad_words = ['facebook', 'instagram', 'youtube', 'twitter', 'wiki' ] + ROLE_BASED_NAMES
      # df = get_info('mastering studio london', 300, 'pt', 'studios.csv', reject=bad_words)
      df = get_info('pastebin email address', 100, 'pt', self.data_dir+'/scraped_emails.csv', reject=bad_words)
      return df.head()
    
    





