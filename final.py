import urllib
import urllib.request
import requests
import time
from preset import OrderedSet

import time

start = time.time()

acc_list = []  #List of all the account
k = 0 #counter for accounts
le =0 #for testing  

def valid_pics(lst): #delete video thumbs, turn into a list of valid pictures
    count = 0
    for item in lst: 
        count += 1
        if (item[-4:]) == ".mp4": #delete all the item 
            del(lst[count])
    return lst

def gen_deleted(orig,new): #get deleted, workfs for strings not responses
    c = 0
    k = 0
    new =  OrderedSet(new) #set of new pictures comming in
    orig = OrderedSet(orig) #set of old pictures
    new_orig= (list(new - orig))  #list of all new pictures that were not there before
    orig_new= (list(orig - new)) #list of all old pictures that were not there before
    new = list(new)
    if orig_new == []: #no new pics
        return []
    if (len(new) < len(orig)): #some pictures were deleted
        return orig_new
    for ele in new_orig: 
        if not(new_orig[c] == new[c]): #if same length and pics different
            return (orig_new)  #return corresponding list
        c +=1   
    rev_orig = list(orig)
    rev_orig = rev_orig[::-1] #delete invalid element
    rev_orig_new = orig_new[::-1]
    for ele in rev_orig_new:
        if not(rev_orig_new[k] == rev_orig[k]): #if same length and pics different
            return (orig_new)
        k +=1
    return ([])

def get_pics_URL(url): #gets string htmls
    persons_pics = []
    response = urllib.request.urlopen(url) #get response and read it
    html = response.read()
    html = str(html)
    html = html[2:-1]
    html = html.split(",") #split into marks of the response
    for sec in html:      
        if "standard_resolution" in sec:   #get and clean links
            sec = sec[30:-1]
            new_sec= sec.replace("\\", "") #gathering links using profile ID
            persons_pics.append(new_sec)
    persons_pics = (valid_pics(persons_pics))  
    return (persons_pics)


def get_ucodes(lst):
    ucode_list = []
    for urls in lst: #get unique codes for all the pictures
        ucode = (urls[-41:])
        ucode_list.append(ucode)    
    return ucode_list

def download_pics(lst):
    response_list= [] 
    for pics in lst:  
        response_list.append(requests.get(pics)) #download the pics 
    return response_list


class Account:
    def __init__(self, name, ID):
        self.name = name
        self.ID = ID
        self.URLs = ""
        self.downloaded_pics = ""
        self.ucodes = ""
        

################################################################################
################################################################################


acc2 = Account("other_test_acc", "2131832594") ##
acc_list.append(acc2)

acc3 = Account("claudialeitte", "25751803")
acc_list.append(acc3)

acc4 = Account("fakeliampayne", "1293310212")
acc_list.append(acc4)

acc5 = Account("beyonce", "247944034")
acc_list.append(acc5)

acc6 = Account("kimkardashian", "18428658")
acc_list.append(acc6)

acc7 = Account("zendaya", "9777455")
acc_list.append(acc7)

acc8 = Account("ladygaga", "184692323")
acc_list.append(acc8)

acc9 = Account("shaym", "2364270")
acc_list.append(acc9)

acc10 = Account("jlo", "305701719")
acc_list.append(acc10)

#Testing on top 9 most followed account for reference 


################################################################################
################################################################################

for account in acc_list: #get originals, before loop
    last_acc = (account.name)    
    
    account.URLs = get_pics_URL("https://api.instagram.com/v1/users/" + account.ID + "/media/recent/?client_id=9e72d5067efd4e21bcb2d01a3560868e") #get the pics
    account.ucodes = get_ucodes(account.URLs) #get the unique codes of pictures
    account.downloaded_pics = download_pics(account.URLs) #download said pics
    


while True: #cycle this
    
    for account in acc_list:
        last_acc = (account.name)    #get account name     
        new_URLs = get_pics_URL("https://api.instagram.com/v1/users/" + account.ID + "/media/recent/?client_id=9e72d5067efd4e21bcb2d01a3560868e")
        
        if not(new_URLs == account.URLs):   #if media has changed
            new_ucodes = get_ucodes(new_URLs) #new ucodes
            deleted_pics = gen_deleted(account.ucodes,new_ucodes)
    
            #if nothing deleted does not update actual response, only ucodes
            for pics in deleted_pics:
                k += 1
                Ftype = pics[-4:]
                place = account.ucodes.index(pics) #check this

                #write it in text file
                with open(((account.name)+ str(k) +(Ftype)), 'wb') as test:
                    test.write(account.downloaded_pics[place].content) 
                    #write out the image
            account.URLs = new_URLs #update corresponding object properties
            account.ucodes = new_ucodes
            account.downloaded_pics = download_pics(new_URLs)


    time.sleep(2) #to not overload the API due to too many requests
    
    #le +=1
