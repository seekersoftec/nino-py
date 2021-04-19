# validates mail 
import pandas as pd
from lib.constants import ROLE_BASED_NAMES
from lib.utils import verifyEmailORG

# 
class Validator:
  """
    Validates mails
  """
  def __init__(self):
    pass
    
  @classmethod 
  def _remove_role_based_accounts(cls, df, column_name = 'generated_strings'):
    return df[~df[column_name].isin(ROLE_BASED_NAMES)]
  
  @classmethod 
  def _verify(cls, args: list):
    # verifyEmailORG
    raise NotImplementedError

  @classmethod
  def _remove_non_dict_based_accounts(cls, df, column_name = 'generated_strings'):
    raise NotImplementedError
  
  def validate(self, dataframe):
    # Remove role based accounts
    df = self._remove_role_based_accounts(dataframe)
    # 
    return df
 
 


