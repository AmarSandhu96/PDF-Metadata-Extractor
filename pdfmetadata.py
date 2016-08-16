
def Welcome():
    return '''
    \ \      / /__| | ___ ___  _ __ ___   ___
     \ \ /\ / / _ \ |/ __/ _ \| _ ` _ \ / _  |
      \ V  V /  __/ | (_| (_) | | | | | |  __/
       \_/\_/ \___|_|\___\___/|_| |_| |_|\___|

        ______________________
< PDF Metadata Locator >
 ----------------------
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\/
                ||----w |
                ||     ||


       '''
print (Welcome())



def OnePDF():
    try:
        import PyPDF2
    except ImportError:
        print ('Sorry PyPDF2 not found. Please install this module to continue')

    print ('[*] Please enter the path of the file you would like to analyse:')
    PDFchoice = input(' >')
    try:
        PDFfile = open (PDFchoice, 'rb')
    except FileNotFoundError:

        print ('Sorry, File not found. Try again')
        OnePDF()

    targetpdf = PyPDF2.PdfFileReader(PDFfile)
    # if a pdf is encrypted notify the user and wait for responce
    encryptedpdf = targetpdf.isEncrypted
    if encryptedpdf == True:
        print ('The File You Entered Is Encrypted And Needs To Be Decrypted Before Further Analysis.')
        print ('Decrypt File? Y/N')
        Decryptchoice = input (' > ')
        if Decryptchoice == 'Y':
            # Read the encrypted File
            eachfile = PyPDF2.PdfFileReader(PDFfile)
            print ('Please specify the path to your password list. E.G /home/Brian/<Password List.txt>')
            passwordfilechoice = input (' > ')
            password_file = open (passwordfilechoice,'r')
            # For loop to bruteforce password
            for password in password_file:
                # strip each word which is tried of its new line. if the password is correct
                if eachfile.decrypt(password.strip('\n')) == 1:

                    print (' [+] Password Successful: {}'.format(password))
                    # extract Metadata
                    results = (eachfile.getDocumentInfo())
                    # for loop is just for formatting
                    for M in results:
                        print ('[*] ' + M + ': ' + results[M])

                    exit()

                else:
                    print (' [+] Password Unsuccessful: {}'.format(password))
        else:
            exit()
    # extract metadata for pdfs which were not encrypted
    results = (targetpdf.getDocumentInfo())
    for M in results:
        print ('[*] ' + M + ': ' + results[M])




def ManyPDF():
    try:
        import PyPDF2
    except ImportError:
        raise ImportError('<Unable to find PyPDF2. Please Install. >')

    import shutil
    import os

    print ('What type of File would you like to search for: .pdf, .py .html? Please note that Metadata extraction only works for PDFs. Choosing any other types of file will copy them to a location of your choosing but will be unable to extract Metadata')
    choice = input(' > ')
    rootDir = '.'
    pdflist = []
    path = []

    # Cycle through all the files in the directory and below
    for dirName, subdirList, fileList in os.walk(rootDir, topdown=False):
        for fname in fileList:
            if fname.endswith(choice):
                # for formating, add the dirName and fname together
                filewithpath = (dirName + '/' + fname)
                # add filewithpath to list
                path.append(filewithpath)
                # add new line to the list to seperate each element
                finalpath = ('\n'.join(path))
                # add file names of pdflist
                pdflist.append(fname)
                # find length of pdf list
                numberofpdfs = len(pdflist)

            else:
                pass
    print (' [*] Number of Files Found: {}' .format(numberofpdfs))
    print (finalpath)
    print ('Proceed With Inspection of The Files?')
    inspectiondec = input(' >  Y/N: ')


####################   Cycling through the files again and moving pdfs found ##########################

    if inspectiondec == 'Y':


            targetfolder = []

            print ('This program will now create a folder to contain the PDF files before further inspection. Please specify where you would like this folder to be located. E.G /home/Brian/Desktop/<FolderName>')
            # take name and path the user has provided
            pdffolder = input(' > ')
            # create folder to the specifications of the user
            os.mkdir(pdffolder)
            # Re-cycle through all the directories
            for dirName, subdirList, fileList in os.walk(rootDir, topdown=False):
                    for fname in fileList:
                        if fname.endswith(choice):
                            #again for formatting add dirname and fname together
                            fullfilepath = (dirName + '/' + fname)
                            # Try to copy pdfs into the users desired folder
                            try:
                                shutil.copy2(fullfilepath,pdffolder)
                            except shutil.SameFileError as e:
                                pass
                                # print the files which have been moved
                                print (fullfilepath)

                                # add the files which have been moved to a list called targetfolder for metadata Analysis
                                targetfolder.append(fullfilepath)

                        else:
                            pass

            if choice != 'pdf':
                print ('The file you have chosen cannot undergo metatdata extraction. Exiting...')
                exit()
            else:
                pass
###################    Extract Metadata for each file ######################



            for eachfile in targetfolder:
                try:

                    PDFfile = open(eachfile, 'rb')

                except RuntimeError :
                    pass

                targetpdf = PyPDF2.PdfFileReader(PDFfile)
                # detect if one of the files in targetfolder is encrypted. If this is true then begin the decryption routine
                encryptedpdf = targetpdf.isEncrypted
                if encryptedpdf == True:
                    print ('{} Is Encrypted And Needs To Be Decrypted Before Further Analysis'.format(eachfile))
                    print ('Decrypt File? Y/N')
                    Decryptchoice = input (' > ')
                    if Decryptchoice == 'Y':
                        eachfile = PyPDF2.PdfFileReader(PDFfile)
                        # Ask for the path to the password list
                        print ('Please Specify The Path To Your Password List. E.G /home/Brian/<Password List.txt>')
                        passwordfilechoice = input(' > ')
                        password_file = open(passwordfilechoice, 'r')
                        # Brute force the password
                        for password in password_file:

                            # strip each word in password list of its new line. If the password is Successful....
                            if eachfile.decrypt(password.strip('\n')) == 1:

                                print (' [+] Password successful: {}'.format(password))
                                results = (eachfile.getDocumentInfo())
                                # for loop is just for formatting
                                for Metadata in results:
                                    print ('[*] ' + Metadata + ': ' + results[Metadata])
                                exit()

                            else:
                                print (' [+] Password Unsuccessful: {}'.format(password))
                    else:
                        exit()


                else:
                    pass

                results = (targetpdf.getDocumentInfo())

                # print the Metadata for pdfs which were not encrypted
                print ('[-------------] PDF Metadata for : {} [----------------] '.format(eachfile))
                for M in results:
                    print ('[*] ' + M + ': ' + results[M])


    else:
        exit()










print ('[*] Press [1] for targeting a single PDF ')
print ('[*] Press [2] for all PDFs in the current directory and below')


choice = input(' >  ')

if choice == '1':
    OnePDF()
if choice == '2':
    ManyPDF()
