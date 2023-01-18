#Group project

'''
Pseudocode
1. Allow user to input sequence either manually, via fasta or genbank file.
2. Extract the nucleotide sequence from the user input.
2. Determine the input file to ensure there are in fasta and genbank format.
3. Define function for finding reverse compliment.
4. Read bases in the sequence two by two.
5. Create search pattern for every two base using reverse and compliment function.
6. Search for the pattern and store the seq for each match.
7. Output the palindromic sequence with additional information.

'''

#library
import re
import string

seqFF = True

while seqFF:
    singleSeq = ''
    #User selects input format
    In = input ("\nPlease enter:\nM-Manual input\nF-Fasta file\nG-Genbank file\n->").upper()

    #Manual input
    if In == "M":
        singleSeq = input("\nEnter sequence to find palindromes: ").upper()

    #Fasta input
    elif In == "F":
        fn = input("\nEnter filename to find palindromes: ")
    
        #Pattern to recognize fasta format
        if re.search(r"(.+)fa(.*)|(.+)fasta(.+)", fn):
            my_str = open(fn,"r")
            lines = my_str.readlines()

            for line in lines:
                line = line.strip()
                head = re.match(r'>(.*)', line, re.I)

                if head:
                    continue
        
                else:
                    singleSeq += line.upper()

            my_str.close()
        
        else:
            print("Wrong file format.")
            seqFF = False

    #Genbank input
    elif In == "G":
        fn = input("\nEnter filename to find palindromes: ")

        #Pattern to recognize genbank format
        if re.search(r"(.+)gb(.*)|(.+)genbank(.+)", fn):
            my_str = open(fn,"r")

            lines = my_str.readlines()

            for line in lines:

                s = re.match(r"\s+\d+\s+(.+)",line, re.I)

                if s:

                    seqline = s.group(1)
                    seqline = re.sub(r" ","",seqline)
                    singleSeq += seqline.upper()
            my_str.close()
        
        else:
            print("Wrong file format.")
            seqFF = False
    
    else:
        print("Wrong input!")
        seqFF = False
      
    #Screen the input sequence
    m = re.search(r'[^ACGT]+',singleSeq)
    if m:
        print("This is not a Nucleotide sequence!")
        #shut the program if the extracted seq is not Nucleotide sequence
        seqFF = False
    
    #Function for reversing the sequence
    def reverse(Pattern):
        return Pattern[::-1]

    #Function for retrieving sequence compliment
    def compliment(Nucleotide):
        comp = ''
        for i in Nucleotide:
            if i == 'A':
                comp += 'T'
            elif i == 'T':
                comp += 'A'
            elif i == 'C':
                comp += 'G'
            elif i == 'G':
                comp += 'C'

        return comp

    #Function for prime numbers
    def prime(n):
        primes = [3]
        for i in range(2,n+1):
        
            for j in range(2,int(i**0.5)+1):
                if i%j == 0:
                    break
                else:
                    primes.append(i)
                
        return list(dict.fromkeys(primes))

    def checkchar(x):
        if all(char == x[0] for char in x):
            return 1
        else:
            return 0

    #Palindrome search
    #Declare variable
    count = 0
    palindrome = []

    for i in singleSeq:
        #Read seq base two by two
        head = singleSeq[0+count:2+count]
        count += 1
    
        if len(head)>1:
            #Identify the search pattern
            tail = compliment(reverse(head))
            #Identify the search region
            splitseq = singleSeq[count+1:count+19]

            if len(splitseq)>1:
                #Search the match
                palin = re.finditer(tail,splitseq)
            
                for i in palin:
                    #Append the first two base together with the bases until the match
                    palindrome.append(head + splitseq[0:i.end()])

                #Lookahead assertion for repeating character in search pattern
                if checkchar(tail)==1:
                    #Use prime no to generate all possible length
                    x = prime(int(len(splitseq)))
                
                    for i in x:
                       tail = tail[0]*i
                       palin = re.finditer(tail,splitseq)
                   
                       for i in palin:
                           palindrome.append(head + splitseq[0:i.end()])
                    
    #Search palindrome locus
    position=[]
    outseq=[]

    for i in palindrome:
        locus = re.finditer(i,singleSeq)
    
        for k in locus:
            locus = k.span()
            position.append(locus)#Store locus in list
            position = list(dict.fromkeys(position))#Remove redundant locus


    #Print(position)       
    for i in position:
        #Use locus to locate position of substring (palin seq)
        outseq.append(singleSeq[i[0]:i[1]])

    #Classify palindromic seq into spacer and non-spacer
    count = 0
    spacer=[]
    non_spacer=[]

    for i in outseq:
    
        #Spacer
        if i == reverse(compliment(i)):
            non_spacer.append('Palindrome seq\t:'+str(i)+'\nPosition\t:'+
                              re.sub(r',',' to',str(position[count]))+
                              '\nLength\t\t:'+str(len(i))+'\n')
            count+=1

        #Non-spacer   
        else:   
            spacer.append('Palindrome seq\t:'+str(i)+'\nPosition\t:'+
                          re.sub(r',',' to',str(position[count]))+
                          '\nLength\t\t:'+str(len(i))+'\n')
            count+=1



    #Design output 
    print("Length of Nucleotide sequence:",len(singleSeq))

    non_spacer = list(dict.fromkeys(non_spacer))
    spacer = list(dict.fromkeys(spacer))

    number = 1
    print("\nNon-spacer palindromes:")

    for i in non_spacer:
        print("\nPalindrome no\t:",number)
        print(i)
        number += 1
    print("\nTotal number of non-spacer palindrome:",number-1)

    number = 1
    print("\nSpacer palindromes:")

    for i in spacer:
        print("\nPalindrome no\t:",number)
        print(i)
        number += 1
    print("\nTotal number of spacer palindrome:",number-1)

    #loop for termination of the program
    print("\nDo you want to input sequence or file?\nY/N")
    In = input().upper()
    if In == "Y":
        seqFF = True

    elif In == "N":
        seqFF = False

    else:
        print("Wrong input!")
        seqFF = False
