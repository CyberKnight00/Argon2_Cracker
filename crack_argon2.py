import concurrent.futures
import os, time
import optparse
from argon2 import PasswordHasher # Argon2 library is used to hash and verify passwords
from termcolor import colored, cprint # termcolor library is used to add colors to the output

# Auther Vishal Biswas (https://twitter.com/CyberKnight00)
start = time.time()

def check(word):
    """
    Function to check if the word matches the given hash
    """
    try:
        if(ph.verify(hash, word) == True) :
            cprint("{0} -> {1} ".format(hash,word),'green', attrs=['bold'])
            print("Total time taken : {}".format(time.time() - start))
            os._exit(1)
        else:
            if(options.verbose): cprint("{0} x-> {1} is not valid.".format(hash,word),'red', attrs=['bold'])
    except :
        if(options.verbose):
            cprint("{0} x-> {1} is not valid.".format(hash,word),'red', attrs=['bold'])
        else:
            pass

# Start

if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option('-v', '--verbose', action="store_true", help = "Verbose = True" )
    parser.add_option('-c', '--crack', action="store", dest="argon2_hash", help="Argon2 hash to be crack")
    parser.add_option('-w', '--wordlist', action="store", dest="wordlist", help="Wordlist for crack salted hash")
    parser.add_option('-t', '--threads', action="store", dest="threads", type=int, help="Number of threads to use")

    options, args = parser.parse_args()

    if not options.argon2_hash:
        cprint("[+] Specify a Argon2 hash",'red', attrs=['bold'])
        cprint("[+] Example usage crack_Argon2.py -c argon2_hash -w path-to-wordlist",'yellow', attrs=['bold'])
        exit()
    else:
        hash = options.argon2_hash

    wordlist_tmp = '/usr/share/wordlists/fasttrack.txt'

    if not options.wordlist :
        wordlist = wordlist_tmp
    else:
        wordlist = options.wordlist

    ph = PasswordHasher()
    result = None
    if options.threads:
        with concurrent.futures.ThreadPoolExecutor(max_workers=options.threads) as executor:
            futures = {executor.submit(check, word) for word in open(wordlist, 'r', encoding='Latin-1').read().splitlines()}
            for future in concurrent.futures.as_completed(futures):
                if future.result() and future.result()[0]:
                    result = future.result()[1]
                    os._exit(1)
    else:
    	# Go rogue
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = {executor.submit(check, word) for word in open(wordlist, 'r', encoding='Latin-1').read().splitlines()}
            for future in concurrent.futures.as_completed(futures):
                if future.result() and future.result()[0]:
                    result = future.result()[1]
                    os._exit(1)
    if result is not None:
        print("Plaintext found:",result)
        print("Total time taken : {}".format(time.time() - start))
    else:
        print("Plain text not found !!!\nTotal time taken : {}".format(time.time() - start))
