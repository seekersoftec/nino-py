# IMPORTS
import os
import time
# 
from lib.mail.generator import Generator
from lib.mail.validator import Validator
from dotenv import load_dotenv

# 
load_dotenv("config.env")

# settings
def get_config():
    config = {
        'DATA_DIR': os.getcwd() + '/' + os.getenv("DATA_DIR"),
    }
    
    return config


# input will be site name e.g coinbase.com
def main():
    # 
    config = get_config()
    # 
    length = 4 
    # 
    # how many emails to generate at once max is 500 
    # 
    generator = Generator(data_dir=config['DATA_DIR'])
    validator = Validator()
    # 
    t1 = time.time()
    # _generate = validator.validate(generator.permutate(length))
    _generate = validator.validate(generator.from_dictionary())
    # _generate = generator.scraper()
    t2 = time.time() 
    time_taken = t2-t1
    print(_generate)
    print(len(_generate), time_taken)
    # 
    # 
    
    
# 
if __name__ == '__main__':
    main()
