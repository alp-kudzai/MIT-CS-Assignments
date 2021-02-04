# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name:
# Collaborators:
# Time:

import feedparser
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime
import pytz
import re


#-----------------------------------------------------------------------

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        # print('YES SIR!!!!!!!')
        ed = entry.description
        # print('OK!!!!!!!!!')
        description = translate_html(ed)
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
          #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
          #  pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret

def sanitise(text):
        new_string = ' '
        for c in text:
            if c.isalpha() or (c == ' ' and new_string[-1] != ' '):
                new_string += c
            elif c in string.punctuation and new_string[-1] != ' ':
                new_string += ' '
        return (new_string + ' ')

#======================
# Data structure design
#======================

# Problem 1

# TODO: NewsStory

class NewsStory(object):
    '''
    Your task, in this problem, is to write a class, ​NewsStory​, 
    ​starting with a constructor​ that takes (​guid, title, 
                                              description, link,
                                              pubdate​) 
    as argumentsand stores them appropriately. 
    ​NewsStory​ also needs to contain the following methods:
        ●get_guid(self)
        ●get_title(self)
        ●get_description(self)
        ●get_link(self)
        ●get_pubdate(self)
    '''
    
    def __init__(self, guid, title, description, link, pubdate):
        self.guid = guid
        self.title = title.lower()
        self.description = description.lower()
        self.link = link
        self.pubdate = pubdate
        
    def get_guid(self):
        return self.guid[:]
    
    def get_title(self):
        return self.title[:]
    
    def get_description(self):
        return self.description[:]
    
    def get_link(self):
        return self.link
    
    def get_pubdate(self):
        return self.pubdate

#======================
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError
        
    # def __str__(self):
    #     return Trigger

class PhraseTrigger(Trigger):
    def __init__(self, phrase):
        phrase = phrase.lower()
        for i in range(len(phrase)):
            if phrase[i] in string.punctuation:
                raise Exception('Invalid input')
            elif phrase[i] == ' ':
                if phrase[i+1] == ' ':
                    raise Exception('Invalid input')
        self.phrase = phrase
                      
    def evaluate(self, story):
        split_phrase = self.phrase.split(' ')
        for word in split_phrase:
            pass
        if self.phrase in sanitise(str(story.get_title())):
            return True
        elif self.phrase in sanitise(str(story.get_description())):
            return True
        else:
            return False
        
    def is_phrase_in(self, text):
        '''
        It has one new method,is_phrase_in​, which takes in one 
        string argument text. It returns ​True​ if the whole 
        phrasephrase​ is present in text, ​False​ otherwise, as 
        described in the examples.
        '''
        
        text = text.lower()
        split_string = self.phrase.split(' ')
        clean_text = sanitise(text)
        re_search = ''
        for words in split_string:
            re_search += words + '(\s|\b)+'
        re_search = re_search
        results = re.search(re_search, clean_text)
        # #can also use search the group() to get the object
        # print(results)
        if results:
            return True
        else:
            return False
# PHRASE TRIGGERS

# Problem 3
# TODO: TitleTrigger
class TitleTrigger(PhraseTrigger):
    
    def evaluate(self, story):
        clean_story = sanitise(story.get_title())
        if PhraseTrigger.is_phrase_in(self, clean_story):
            return True
        else:
            return False
        
# Problem 4
# TODO: DescriptionTrigger
class DescriptionTrigger(PhraseTrigger):
    def evaluate(self, story):
        clean_story = sanitise(story.get_description())
        if PhraseTrigger.is_phrase_in(self, clean_story):
            return True
        else:
            return False

# TIME TRIGGERS

# Problem 5
# TODO: TimeTrigger
# Constructor:
#        Input: Time has to be in EST and in the format of "%d %b %Y %H:%M:%S".
#        Convert time from string to a datetime before saving it as an attribute.
class TimeTrigger(Trigger):
    def __init__(self, time):
        '''
        Given a time (time) it will intialise the required variables
        and convert time to a format for datetime
        '''
        real_time = datetime.strptime(time, '%d %b %Y %H:%M:%S')
        self.time = real_time
# Problem 6
# TODO: BeforeTrigger and AfterTrigger
class BeforeTrigger(TimeTrigger):
    def evaluate(self, story):
        '''
        Returns True when the date of the story is before the 
        given time.
        '''
        story_time = story.get_pubdate()
        if story_time < self.time:
            return True
        else:
            return False
        
class AfterTrigger(TimeTrigger):
    def evaluate(self, story):
        '''
        Returns True when the date of story is after the given
        time
        '''
        story_time = story.get_pubdate()
        if story_time > self.time:
            return True
        else:
            return False


# COMPOSITE TRIGGERS

# Problem 7
# TODO: NotTrigger
class NotTrigger(Trigger):
    def __init__(self, trigger):
        self.trigger = trigger
        
    def evaluate(self, story):
        if not self.trigger.evaluate(story):
            return True
        else:
            return False

# Problem 8
# TODO: AndTrigger

class AndTrigger(Trigger):
    def __init__(self, trigger1, trigger2):
        self.trigger1 = trigger1
        self.trigger2 = trigger2
        
    def evaluate(self, story):
        if (self.trigger1.evaluate(story)) and (self.trigger2.evaluate(story)):
            return True
        else:
            return False
# Problem 9
# TODO: OrTrigger
class OrTrigger(Trigger):
    def __init__(self, trigger1, trigger2):
        self.trigger1 = trigger1
        self.trigger2 = trigger2
        
    def evaluate(self, story):
        if (self.trigger1.evaluate(story)) or (self.trigger2.evaluate(story)):
            return True
        else:
            return False


#======================
# Filtering
#======================

# Problem 10
def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    # TODO: Problem 10
    # This is a placeholder
    # (we're just returning all the stories, with no filtering)
    story_container = []
    for stry in stories:
        for trigger in triggerlist:
            if trigger.evaluate(stry):
                story_container.append(stry)
    return story_container



#======================
# User-Specified Triggers
#======================
# Problem 11
def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """
#     # We give you the code to read in the file and eliminate blank lines and
#     # comments. You don't need to know how it works for now!
    trigger_file = open(filename, 'r')
    lines = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)
    lines_list = []
    #Here we are going to split the instructions into a list called
    #lines_list
    for l in lines:
        temp = l.split(',')
        lines_list.append(temp)
    trigger_build = {}
    trigger_list = []
    #We are going to start trying to build the trigger from the instructions
    # in lines_list and put then in a dictionary
    for trigger in lines_list:
        tr_name = trigger[0]
        if not tr_name == 'ADD':
            order = trigger[1]
            # if order == ('TITLE' or 'DESCRIPTION' or 'AFTER' or 'BEFORE' or 'AND' or 'OR'):
            if order == 'TITLE':
                trigger_build[tr_name] = TitleTrigger(trigger[2])
            elif order == 'DESCRIPTION':
                trigger_build[tr_name] = DescriptionTrigger(trigger[2])
            elif order == 'AFTER':
                trigger_build[tr_name] = AfterTrigger(trigger[2])
            elif order == 'BEFORE':
                trigger_build[tr_name] = BeforeTrigger(trigger[2])
            elif order == 'AND':
                trigger_build[tr_name] = AndTrigger(trigger_build[trigger[2]], trigger_build[trigger[3]])
            elif order == 'OR':
                trigger_build[tr_name] = OrTrigger(trigger_build[trigger[2]], trigger_build[trigger[3]])
        elif tr_name == 'ADD':
            trigger_list.append(trigger_build[trigger[1]])
            trigger_list.append(trigger_build[trigger[2]])
            
    return trigger_list

    # TODO: Problem 11
    # line is the list of lines that you need to parse and for which you need
    # to build triggers

 





SLEEPTIME = 10 #seconds -- how often we poll

def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
        # t1 = TitleTrigger("election")
        # t2 = DescriptionTrigger("Trump")
        # t3 = DescriptionTrigger("Biden")
        # t4 = AndTrigger(t2, t3)
        # trigger_list = [t1, t4]
        trigger_list = read_trigger_config('triggers.txt')

        # Problem 11
        # TODO: After implementing read_trigger_config, uncomment this line 
        # triggerlist = read_trigger_config('triggers.txt')
        
        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT,fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica",11), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []
        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title()+"\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:

            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            # stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, trigger_list)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)


            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()

