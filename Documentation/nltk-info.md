#Potential useful lines of NLTK for AAC#

This is really a collection of short notes from the [NLTK book](http://nltk.org/book). Find more info there.

##Glossary##

* set: set up a list of words from text. Creates unique list
* bigrams: extracts text as word-pairs. 
* collocation: A collocation is a sequence of words that occur together unusually often. Thus red wine is a collocation, whereas the wine is not. A characteristic of collocations is that they are resistant to substitution with words that have similar senses; for example, maroon wine sounds definitely odd. Think of these as frequent bigrams. 


* To find the number of unique words in a block of text

    len(set(text))

* To find the list of (sorted) unique words

     sorted(set(text3))
    
* How often is each word used on average?

    from __future__ import division
    len(text3) / len(set(text3))
    16.050197203298673
    (i.e approx 16%)
    
    or use
    
     def lexical_diversity(text): 
         return len(text) / len(set(text)) 


* How often does a particular word get noted in the text?

    text3.count("smote")
    5
    100 * text4.count('a') / len(text4)
    1.4643016433938312
    
    or use

     def percentage(count, total): 
         return 100 * count / total


* Find a frequency distribution of all words in text

    fdist1 = FreqDist(text1)
    vocabulary1 = fdist1.keys()

    And to find say the 50 most frequent words 
    
    vocabulary1[:50]
    
* Get words over a certain length

    V = set(text1)
    long_words = [w for w in V if len(w) > 15]
    sorted(long_words)

    
