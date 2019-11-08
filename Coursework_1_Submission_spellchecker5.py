#imports the two external packages added to program
import re
import time
from datetime import datetime
from difflib import get_close_matches
#Retrives the present date and time and sets the format it is displayed in
Date_time = str(datetime.today().strftime('%d/%m/%y  %H:%M'))
#Function that Asks user what they would like to do as part of a menu system
def menu_fun():
    global menu
    print (u'\u2554' + u'\u2550'*60 +u'\u2557')
    print(u'\u2551 '+' '*17 +"S P E L L   C H E C K E R" +' '*17 +u'\u2551')
    print(u'\u2551 ' +' '*22 + Date_time +' '*22 +u'\u2551')
    print (u'\u2560' + u'\u2550'*60 +u'\u2563')
    print(u'\u2551 '+"  Would you like to spell check a file or enter sentence?"+' '*2 + u'\u2551'+ u'\n\u2551 ' +' '*23 + "1. Check file" +' '*23 + u'\u2551' + u'\n\u2551 '+ ' '*23 +"2. Check a sentence"+' '*17 + u'\u2551' )
    print(u'\u2551' + ' '*20 + "    0. Quit" + ' '*29 + u'\u2551')
    print (u'\u2560' + u'\u2550'*60 +u'\u255D')
    menu = input(u'\u255A' + u'\u2550'*15 + " Please enter a number: ")
#Summary Function Prints a summary including the numbers of each action
def summary(n):
    if n == 1:
        print (u'\u2554' + u'\u2550'*60 +u'\u2557')
        print(u'\u2551 ' +' '*12 +"Number of words: " + str(len(index)) +' '*29 +u'\u2551')
        print(u'\u2551 ' +' '*12 +"Number of words corectly spelt: " + str(correct_words) +' '*14 +u'\u2551')
        print(u'\u2551 ' +' '*12 +"Number of words incorectly spelt: " + str(words_not_found) +' '*12 +u'\u2551')
        print (u'\u255A' + u'\u2550'*60 +u'\u255D')
    elif n == 2:
        print (u'\u2554' + u'\u2550'*60 +u'\u2557')
        print(u'\u2551 ' +' '*12 +"Number of words: " + str(len(index)) +' '*28 +u'\u2551')
        print(u'\u2551 ' +' '*12 +"Number of words corectly spelt: " + str(correct_words) +' '*13 +u'\u2551')
        print(u'\u2551 ' +' '*12 +"Number of words incorectly spelt: " + str(words_not_found)+' '*12 +u'\u2551')
        print(u'\u2551 ' +' '*12 +"Number of words ignored: " + str(words_Ignored)  +' '*21 + u'\u2551' + u'\n\u2551' + ' '*12 + " Number of words marked: " + str(words_marked) + ' '*(23-len(str(words_marked))) +u'\u2551')
        print(u'\u2551' +' '*12 +" Number of words added to dictionary: " + str(words_added_to_dictionary) + ' '*(10-len(str(words_added_to_dictionary))) + u'\u2551')
        print (u'\u255A' + u'\u2550'*60 +u'\u255D')
#The function creates a new text file with the appended text
def NewFile():
    new_file = open("201_checkMe.txt","w")
    new_file.write(Date_time + "\nNumber of words: " + str(len(index)) + "\nNumber of words corectly spelt: " + str(correct_words) + "\nNumber of words incorectly spelt: " + str(words_not_found) +"\nNumber of words ignored: " + str(words_Ignored)+ "\nNumber of words marked: "+ str(words_marked) +"\nNumber of words added to the dictionary: "+ str(words_added_to_dictionary) + "\n\n" + appended_text)
    new_file.close()
#Function asks what action they would like to take (ignore, mark, add, word) serves as an additional option on the menu
def MarkIgnAdd():
    global Opportunity
    print("Word not found: "+ alpha_file_list[count] + u'\n\u2554'+ u'\u2550'*60 + u'\u2557'+ u'\n\u2551Would you like to:'+' '*(60-18)+ u'\u2551' + u'\n\u25511. Ignore Word '+' '*(60-15)+ u'\u2551')
    print( u'\u25512. Mark word' + ' '*(60-12) + u'\u2551' + u'\n\u2551'  + '3. Add Word to Dictionary' + ' '*(60-25) +u'\u2551')
    Opportunity = input( u'\u2560'+ u'\u2550'*60 +u'\u255D'+ u'\n\u255A' + u'\u2550'*15 +' Please Enter either 1, 2 or 3:')

menu_fun()
#Creates diffeernt pathways dependin on what user intends to do.
while menu != "0" :
    if menu == "1":
#opens file chosen splits each word up based on the spaces between and strips it of non-alpha characters before entering it into a list.
        fo = open(input("Enter the name of the file to be spell checked: "), "r")
        fo_file_word_str = fo.read()
        file_filter = re.compile('[^a-zA-Z]')
        alpha_file = file_filter.sub(' ', fo_file_word_str)
        alpha_file_list = alpha_file.split()
#opens text file and stores each line as an elelment in a list whilst removing "\n"
        f = open("EnglishWords.txt", "r")
        dictionary = [line.rstrip('\n') for line in f]
        f.close()
#Empty list that will make note of which elements in the text file's list need to be changed.
        no_incorect_elementM = []
        no_incorect_elementI = []
        no_incorect_elementA = []
#Records the time at this point in the code settin equal to variable STime
        STime = time.time()
        count,correct_words, words_not_found, words_Ignored, words_marked, words_added_to_dictionary = 0,0,0,0,0,0
        index = alpha_file_list
        appendedlist = alpha_file_list
        while count != len(alpha_file_list):
#if statement checks if word text file is in the dictionary list.
            if alpha_file_list[count] in dictionary:
                correct_words += 1
            else:
# Using the Sequence Matcher package the word most likend to the current selected word is suggested to the user. User is then asked if they want to change it to it.
                print("Word not found: " + alpha_file_list[count])
                suggestion = get_close_matches(alpha_file_list[count], dictionary)
                print (u'\n\u2554' + u'\u2550'*60 + u'\u2557')
                print ( u'\u2551' + "Suggested word: " + suggestion[0] + ' '*(60-(16 + len(suggestion[0]))) + u'\u2551')
                wordsugg = input( u'\u2551' + "Would you like to change the word to: " + suggestion[0]+ ' '*(60-(38+ len(suggestion[0]))) + u'\u2551' + u'\n\u2560' + u'\u2550'*60 +u'\u255D'+ u'\n\u255A'+ u'\u2550'*15 + "[y] for yes or [n] for no: " )
#while statement verifies the users input preventing them from moving on without entering something valid.
                while wordsugg != "y" and wordsugg != "n":
                    wordsugg = input("INVALID ENTRY!\n Please enter either\n [y] for yes or [n] for no: " )
                if wordsugg == "y":
                    print ("Word changed from", alpha_file_list[count]," to ", suggestion[0] )
                    appendedlist[count] = suggestion[0]
                elif wordsugg == "n":
                    words_not_found += 1
                    MarkIgnAdd()
                    while Opportunity !="1" and Opportunity !="2" and Opportunity !="3":
                        print("INVALID ENTRY! \nPlease select either 1, 2 or 3\n")
                        MarkIgnAdd()
#Based on each option(Mark, Ignore and Add)the no. at which the word element is in the list is added to temp
# list so that the appended list can change the element at the intended place accordingly.
                    if Opportunity == "1":
                        print(alpha_file_list[count] +" has been ignored.")
                        words_Ignored += 1
                        no_incorect_elementI.append(count)
                        for x in no_incorect_elementI:
                            appendedlist[x] = ("!" + alpha_file_list[x] + "!")#prepends and appends the element in the new list with !
                    elif Opportunity == "2":
                        print(alpha_file_list[count] +" has been marked.")
                        words_marked += 1
                        no_incorect_elementM.append(count)
                        for x in no_incorect_elementM:
                            appendedlist[x] = ("?" + alpha_file_list[x] + "?")
                    elif Opportunity == "3":
                        print(alpha_file_list[count] +" has been added to the dictionary.")
                        words_added_to_dictionary += 1
                        dictionary.append(alpha_file_list[count])
                        no_incorect_elementA.append(count)
                        for x in no_incorect_elementA:
                            appendedlist[x] = ("*" + alpha_file_list[x] + "*")
#opens the Words lists and updtates it by adding the word to next line in the file
                        f = open("EnglishWords.txt","a")
                        f.write("\n" + alpha_file_list[count])
                        f.close()
#Adds 1 to the count in order to move to the next word in the list.
#Turns the appended list back into a string so it may be printed in the text file.
            count += 1
            appended_text = ' '.join(appendedlist)
            NewFile()

        fo.close()
        summary(2)
#Takes the time at this point and subtracts the time recorded earlier to calculate and display the time elapsed in microsecods.
        ETime = int((time.time() - STime)*(10**6))
        print("Time Elapsed: " + str(ETime)+ " microseconds.")
        menu_fun()

    elif menu == "2":
#Filters sentence removing any non alphabetic characters then placing it into a list.
        print (u'\u2554' + u'\u2550'*60 +u'\u2557')
        sen_filter = re.compile('[^a-zA-Z]')
        sentence = str(input(u'\u2551 ' +"Please enter sentence you want to be spell checked" + u'\n\u255A' + u'\u2550'*15 +": " ))
        alpha_sen = sen_filter.sub(' ', sentence)

        list_of_words = alpha_sen.lower().split()
        print("\n")

        f = open("EnglishWords.txt", "r")
        dictionary = [line.rstrip('\n') for line in f]

        count,correct_words, words_not_found = 0,0,0
        index = list_of_words
        while count != len(list_of_words):
            if list_of_words[count] in dictionary:#Checks each word in list_of_words to see if its in the dictionary
                print (u'\u2554' + u'\u2550'*60 +u'\u2557')#if the program goes down this branch word is splelt correctly so correct count increases by 1
                print(u'\u2551 ' + list_of_words[count] + " is spelt correctly." +' '*(60-(len(list_of_words[count])+21)) +u'\u2551')
                print (u'\u255A' + u'\u2550'*60 +u'\u255D')
                correct_words += 1
            else:
                print (u'\u2554' + u'\u2550'*60 +u'\u2557')#if the program goes down this branch word isnt in dictionary so words not found count increases by 1
                print(u'\u2551 ' + list_of_words[count] + " is not found in dictionary" +' '*(60-(len(list_of_words[count])+28)) +u'\u2551')
                print (u'\u255A' + u'\u2550'*60 +u'\u255D')
                words_not_found += 1
            count += 1
        f.close
        summary(1)
        menu_fun()
    else:
#if one of the correct values is not inputted by the user error message displayed and menu function is asked again
        print(u'\u250F' + u'\u2501'*60 + u'\u2513')
        print(u'\u2503' + "ENTRY INVALID!" + ' '*46 + u'\u2503'+ u'\n\u2503' + "Please enter either 0 , 1 or 2" +' '*30 + u'\u2503')
        print(u'\u2517' + u'\u2501'*60 + u'\u251B')
        menu_fun()
