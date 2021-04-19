import random
import requests
from .validate_email import validate_email
import json
import pkg_resources
import itertools


def email_permuter(first_name='', middle_name='', last_name='', domain_name=''):
    """
        Excepts first_name, last_name and domain_name as arguments and returns a
        list of all permutations of possible mail id's.
    """
    first_name = first_name.lower()
    last_name = last_name.lower()
    domain_name = domain_name.lower()
    #
    all_names = [[first_name, first_name[0]], [last_name, last_name[0]]]
    print(all_names)
    #
    punctuations = ". _ - ".split()
    #
    a = list(itertools.product(all_names[0], all_names[1], punctuations))
    b = list(itertools.product(all_names[0], all_names[1]))
    #
    combinations = [s for x in a for s in itertools.permutations(
        x, 3) if s[0] not in punctuations if s[-1]not in punctuations]
    combinations.extend(["".join(s) for x in b
                         for s in itertools.permutations(x, 2)
                         if s[0] not in punctuations
                         if s[-1]not in punctuations])

    combinations = ["".join(s) for s in combinations]
    combinations.extend([first_name, last_name])
    permuted_emails = [f"{s}@{domain_name}" for s in combinations]

    return permuted_emails


#
#
# Specify the first name, last name and domain name
first_name = "ojietohamen"
last_name = "samuel"
domain_name = "gmail.com"

permuted_emails = email_permuter(first_name=first_name,
                                 last_name=last_name,
                                 domain_name=domain_name
                                 )

print(permuted_emails)


#
#
#

# generate emails from personal info if domains are specified,generates usernames if not

def gen_emails_from_info(input_info, input_domains):
    user_list = []
    if("first" in input_info and "last" in input_info):
        user_list.append(input_info["first"] + input_info["last"])
        user_list.append(input_info["first"] + "." + input_info["last"])
        user_list.append(input_info["first"] + "_" + input_info["last"])

    if("first" in input_info and "middle" in input_info and "last" in input_info):
        user_list.append(input_info["first"] +
                         input_info["middle"] + input_info["last"])
        user_list.append(input_info["first"] +
                         input_info["middle"][0] + input_info["last"])
        user_list.append(
            input_info["first"] + "." + input_info["middle"][0] + "." + input_info["last"])
        user_list.append(
            input_info["first"] + "_" + input_info["middle"][0] + "_" + input_info["last"])

    if("first" in input_info and "birthdate" in input_info and "last" in input_info):
        birthdate = input_info["birthdate"].replace('*', '')
        yyyy = input_info["birthdate"][-4:]
        yy = input_info["birthdate"][-2:]

        user_list.append(input_info["first"] + input_info["last"] + yyyy)
        user_list.append(input_info["first"] + input_info["last"] + "." + yyyy)
        user_list.append(input_info["first"] + input_info["last"] + "_" + yyyy)
        user_list.append(input_info["first"] + input_info["last"] + yy)
        user_list.append(input_info["first"] + input_info["last"] + "." + yy)
        user_list.append(input_info["first"] + input_info["last"] + "_" + yy)
        user_list.append(input_info["first"] + "." +
                         input_info["last"] + "." + yyyy)
        user_list.append(input_info["first"] + "_" +
                         input_info["last"] + "_" + yyyy)
        user_list.append(input_info["first"] + "." +
                         input_info["last"] + "." + yy)
        user_list.append(input_info["first"] + "_" +
                         input_info["last"] + "_" + yy)

        user_list.append(input_info["first"][0] + input_info["last"] + yyyy)
        user_list.append(input_info["first"][0] +
                         input_info["last"] + "." + yyyy)
        user_list.append(input_info["first"][0] +
                         input_info["last"] + "_" + yyyy)
        user_list.append(input_info["first"][0] + input_info["last"] + yy)
        user_list.append(input_info["first"][0] +
                         input_info["last"] + "." + yy)
        user_list.append(input_info["first"][0] +
                         input_info["last"] + "_" + yy)
        user_list.append(input_info["first"][0] +
                         "." + input_info["last"] + "." + yyyy)
        user_list.append(input_info["first"][0] +
                         "_" + input_info["last"] + "_" + yyyy)
        user_list.append(input_info["first"][0] +
                         "." + input_info["last"] + "." + yy)
        user_list.append(input_info["first"][0] +
                         "_" + input_info["last"] + "_" + yy)

        user_list.append(input_info["first"] + input_info["last"][0] + yyyy)
        user_list.append(input_info["first"] +
                         input_info["last"][0] + "." + yyyy)
        user_list.append(input_info["first"] +
                         input_info["last"][0] + "_" + yyyy)
        user_list.append(input_info["first"] + input_info["last"][0] + yy)
        user_list.append(input_info["first"] +
                         input_info["last"][0] + "." + yy)
        user_list.append(input_info["first"] +
                         input_info["last"][0] + "_" + yy)
        user_list.append(input_info["first"] + "." +
                         input_info["last"][0] + "." + yyyy)
        user_list.append(input_info["first"] + "_" +
                         input_info["last"][0] + "_" + yyyy)
        user_list.append(input_info["first"] + "." +
                         input_info["last"][0] + "." + yy)
        user_list.append(input_info["first"] + "_" +
                         input_info["last"][0] + "_" + yy)

        if (len(birthdate) == 8):
            dd = (input_info["birthdate"][0:2]).replace('0', '')
            mm = (input_info["birthdate"][2:4]).replace('0', '')

            user_list.append(input_info["first"] + input_info["last"] + mm)
            user_list.append(input_info["first"] +
                             input_info["last"] + "." + mm)
            user_list.append(input_info["first"] +
                             input_info["last"] + "_" + mm)
            user_list.append(input_info["first"] + input_info["last"] + dd)
            user_list.append(input_info["first"] +
                             input_info["last"] + "." + dd)
            user_list.append(input_info["first"] +
                             input_info["last"] + "_" + dd)
            user_list.append(input_info["first"] +
                             "." + input_info["last"] + "." + mm)
            user_list.append(input_info["first"] +
                             "_" + input_info["last"] + "_" + mm)
            user_list.append(input_info["first"] +
                             "." + input_info["last"] + "." + dd)
            user_list.append(input_info["first"] +
                             "_" + input_info["last"] + "_" + dd)

            user_list.append(input_info["first"][0] + input_info["last"] + mm)
            user_list.append(input_info["first"]
                             [0] + input_info["last"] + "." + mm)
            user_list.append(input_info["first"]
                             [0] + input_info["last"] + "_" + mm)
            user_list.append(input_info["first"][0] + input_info["last"] + dd)
            user_list.append(input_info["first"]
                             [0] + input_info["last"] + "." + dd)
            user_list.append(input_info["first"]
                             [0] + input_info["last"] + "_" + dd)
            user_list.append(input_info["first"][0] +
                             "." + input_info["last"] + "." + mm)
            user_list.append(input_info["first"][0] +
                             "_" + input_info["last"] + "_" + mm)
            user_list.append(input_info["first"][0] +
                             "." + input_info["last"] + "." + dd)
            user_list.append(input_info["first"][0] +
                             "_" + input_info["last"] + "_" + dd)

            user_list.append(input_info["first"] + input_info["last"][0] + mm)
            user_list.append(input_info["first"] +
                             input_info["last"][0] + "." + mm)
            user_list.append(input_info["first"] +
                             input_info["last"][0] + "_" + mm)
            user_list.append(input_info["first"] + input_info["last"][0] + dd)
            user_list.append(input_info["first"] +
                             input_info["last"][0] + "." + dd)
            user_list.append(input_info["first"] +
                             input_info["last"][0] + "_" + dd)
            user_list.append(input_info["first"] +
                             "." + input_info["last"][0] + "." + mm)
            user_list.append(input_info["first"] +
                             "_" + input_info["last"][0] + "_" + mm)
            user_list.append(input_info["first"] +
                             "." + input_info["last"][0] + "." + dd)
            user_list.append(input_info["first"] +
                             "_" + input_info["last"][0] + "_" + dd)

            user_list.append(input_info["first"] +
                             input_info["last"] + dd + mm)
            user_list.append(input_info["first"] +
                             input_info["last"] + "." + dd + mm)
            user_list.append(input_info["first"] +
                             input_info["last"] + "_" + dd + mm)
            user_list.append(input_info["first"] +
                             input_info["last"] + dd + mm)
            user_list.append(input_info["first"] +
                             input_info["last"] + "." + dd + mm)
            user_list.append(input_info["first"] +
                             input_info["last"] + "_" + dd + mm)
            user_list.append(input_info["first"] +
                             "." + input_info["last"] + "." + dd + mm)
            user_list.append(input_info["first"] +
                             "_" + input_info["last"] + "_" + dd + mm)
            user_list.append(input_info["first"] +
                             "." + input_info["last"] + "." + dd + mm)
            user_list.append(input_info["first"] +
                             "_" + input_info["last"] + "_" + dd + mm)

    if("first" in input_info and "middle" in input_info and "last" in input_info and "birthdate" in input_info):
        yyyy = input_info["birthdate"][-4:]
        yy = input_info["birthdate"][-2:]

        user_list.append(
            input_info["first"] + input_info["middle"][0] + input_info["last"] + yyyy)
        user_list.append(
            input_info["first"] + input_info["middle"][0] + input_info["last"] + "." + yyyy)
        user_list.append(
            input_info["first"] + input_info["middle"][0] + input_info["last"] + "_" + yyyy)
        user_list.append(
            input_info["first"] + input_info["middle"][0] + input_info["last"] + yy)
        user_list.append(
            input_info["first"] + input_info["middle"][0] + input_info["last"] + "." + yy)
        user_list.append(
            input_info["first"] + input_info["middle"][0] + input_info["last"] + "_" + yy)

    email_list = []
    for domain in input_domains:
        for user in user_list:
            email_list.append(user + '@' + domain)

    if(input_domains == []):
        return user_list
    else:
        return email_list


#
#
#


# check if a string matches a pattern
def matches_pattern(string, pattern):
    nb = 0
    dict = {}
    if (len(pattern) == len(string.rstrip())):
        for i in range(0, len(pattern)):
            if pattern[i] != '*':
                dict[i] = pattern[i]
        for i in dict:
            if (dict[i] == string[i]):
                nb = nb+1
        if(nb == len(dict)):
            return True
        else:
            return False
    else:
        return False


# generate emails from personal information and email pattern
def gen_emails_from_pattern(input_info, email_pattern):
    # split email in to 2 parts
    splitAddress = email_pattern.split('@')
    user_pattern = str(splitAddress[0])
    domain_pattern = str(splitAddress[1])

    additional_info = ['.', '.', '_', '_']
    # parse current info to generate additional info
    for i in input_info:

        if(i == "first" and len(input_info[i][0]) >= 2):
            input_info[i].append(input_info[i][0][0])
        elif(i == "last" and len(input_info[i][0]) >= 4):
            input_info[i].append(input_info[i][0][0:1])
            input_info[i].append(input_info[i][0][0:2])
            input_info[i].append(input_info[i][0][0:3])
            input_info[i].append(input_info[i][0][0:4])
        elif(i == "middle" and len(input_info[i][0]) >= 2):
            input_info[i].append(input_info[i][0][0])
        elif(i == "birthdate"):
            input_info[i][0] = input_info[i][0].replace('*', '')
            yyyy = input_info[i][0][-4:]
            yy = input_info[i][0][-2:]
            input_info[i].append(yy)

            if(len(input_info[i][0]) == 8):
                dd = input_info[i][0][0:2]
                mm = input_info[i][0][2:4]
                input_info[i].append(dd)
                input_info[i].append(mm)
                input_info[i].append(dd + mm + yy)
                input_info[i].append(dd + mm)
                input_info[i].append(yyyy)

                if(dd[0] == '0' and mm[0] != '0'):
                    input_info[i].append(dd.replace('0', ''))
                    input_info[i].append(dd.replace('0', '') + mm + yy)
                    input_info[i].append(dd.replace('0', '') + mm + yyyy)
                    input_info[i].append(dd.replace('0', '') + mm)
                elif(mm[0] == '0' and dd[0] != '0'):
                    input_info[i].append(mm.replace('0', ''))
                    input_info[i].append(dd + mm.replace('0', '') + yy)
                    input_info[i].append(dd + mm.replace('0', '') + yyyy)
                    input_info[i].append(dd + mm.replace('0', ''))
                elif(mm[0] == '0' and dd[0] == '0'):
                    input_info[i].append(dd.replace('0', ''))
                    input_info[i].append(mm.replace('0', ''))
                    input_info[i].append(dd.replace(
                        '0', '') + mm.replace('0', '') + yy)
                    input_info[i].append(dd.replace(
                        '0', '') + mm.replace('0', '') + yyyy)
                    input_info[i].append(dd.replace(
                        '0', '') + mm.replace('0', ''))
        elif(i == "additional_info"):
            additional_info = additional_info + input_info[i]

    # generate possible user list from user pattern and available info
    user_list = []
    for combination in itertools.product(*[v for v in input_info. values()]):
        comb = (list(combination))
        comb.extend(additional_info)
        for i in range(2, 7):
            permutations = list(itertools.permutations(comb, i))

            for p in permutations:
                user = ""
                for i in p:
                    user = user+i
                if (matches_pattern(user, user_pattern) and (".." not in user) and ("__" not in user) and ("._" not in user) and ("_." not in user) and (user.endswith('.') == False) and (user.endswith('_') == False)):
                    user_list.append(user)

    # remove duplicates
    user_list = list(dict.fromkeys(user_list))

    # generate possible domain list from a domain pattern
    domain_list = []
    with open(pkg_resources.resource_filename('data', 'email-providers.json'), 'r') as json_file:
        domains = json.loads(json_file.read())
        for domain in domains:
            if (matches_pattern(domain, domain_pattern)):
                domain_list.append(domain.rstrip())

    # reconstruct emails from user list and domain list
    email_list = []
    if(domain_list != [] and user_list != []):
        for domain in domain_list:
            for user in user_list:
                email_list.append(user + '@' + domain)
        return email_list

    elif(domain_list == []):
        print("we couldnt find the email provider in our database,if you know it pass it with the -p option")

        return

    elif(user_list == []):

        print("we couldnt find any email that matches the pattern you provided,try adding more info with the -a option")

        return


#
#
#
#


# generate emails from username

def gen_emails_from_username(username, domains):

    email_list = []

    for domain in domains:
        email_list.append(username + '@' + domain)

    return email_list


#
#
#
#


def merge_two_dicts(x, y):
    z = x.copy()
    z.update(y)
    return z


# generate work email from first name,last name and company domain
# returns the email with information associated to it

def gen_work_email(first, last, domain, api_key):

    useragents = [
        'Mozilla/5.0 (X11; U; Linux i686; fr; rv:1.9.2.17) Gecko/20110422 Ubuntu/10.04 (lucid) Firefox/3.6.17',
        'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3',
        'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:61.0) Gecko/20100101 Firefox/61.0',
        'Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14',
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'
    ]
    headers = {'User-Agent': random.choice(useragents)}

    work_email_info = {}

    if api_key == "":
        response = requests.get("https://hunter.io/trial/v2/email-finder?domain=" +
                                domain + "&first_name=" + first + "&last_name=" + last, headers=headers)
    else:
        response = requests.get("https://api.hunter.io/v2/email-finder?domain=" +
                                domain + "&first_name=" + first + "&last_name=" + last + "&api_key=" + api_key)

    if response.status_code == 200:
        data = response.json()
        work_email = data["data"]["email"]

        if(data["data"]["position"] != ""):
            work_email_info["position"] = data["data"]["position"]
        if(data["data"]["twitter"] != ""):
            work_email_info["twitter"] = "https://www.twitter.com/" + \
                data["data"]["twitter"]
        if(data["data"]["phone_number"] != ""):
            work_email_info["phone_number"] = data["data"]["phone_number"]

        info = merge_two_dicts(work_email_info, validate_email(work_email))
    else:
        info = {"hunter_limit_reached": True}

    return info
