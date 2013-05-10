#Potential useful lines of NLTK for AAC#


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
    
