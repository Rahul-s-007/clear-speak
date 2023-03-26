import textblob

def keywords_extract(summarized_txt):
    # Use TextBlob to extract the keywords from the summary
    blob = textblob.TextBlob(summarized_txt)
    keywords = [word for word, pos in blob.tags if pos in ['NN', 'NNS', 'NNP', 'NNPS']]
    print("Total Number of keywords: ",len(keywords))
    #print(keywords)

    # String to list
    word_list = summarized_txt.split()
    #print(word_list)

    modified_keywords = []

    # Iterate through the word list
    for i, word in enumerate(word_list):
        # Check if the current word is a keyword
        if word in keywords:
            # Check if the next word is also a keyword
            if i < len(word_list) - 1 and word_list[i + 1] in keywords:
                # If the next word is also a keyword, add the modified keyword to the modified_keywords list
                modified_keywords.append(f"{word} {word_list[i + 1]}")
                # Remove the current and next keywords from the word list
                word_list.pop(i)
                word_list.pop(i)
            else:
                # If the next word is not a keyword, add the current keyword to the modified_keywords list
                modified_keywords.append(word)
                # Remove the current keyword from the word list
                word_list.pop(i)

    # Print the modified word list and modified keywords
    print(modified_keywords)
    keyword_lst = []
    [keyword_lst.append(x) for x in modified_keywords if x not in keyword_lst]
    print("Number of Distinct keywords: ",len(keyword_lst))
    print(keyword_lst)
    return keyword_lst

# text = """The COVID-19 pandemic has had a major impact on the world, causing widespread illness and death, as well as economic and social disruption. As of March 2021, there have been over 120 million confirmed cases of COVID-19 and over 2.6 million deaths worldwide. The pandemic has also led to school closures, job losses, and mental health issues for many people.
# Despite the challenges posed by the pandemic, there has been progress in the development and distribution of COVID-19 vaccines. Several vaccines have been approved for emergency use, and many countries are working to vaccinate their populations as quickly as possible. However, there are concerns about vaccine distribution and vaccine hesitancy, particularly in low- and middle-income countries.
# Overall, the COVID-19 pandemic has highlighted the importance of public health preparedness and international cooperation in responding to global health crises."""
# keywords_extract(text)
    # keyword_freq = {}
    # for i in modified_keywords:
    #     try:
    #         keyword_freq[i] += 1
    #     except:
    #         keyword_freq[i] = 1

    # return keyword_freq