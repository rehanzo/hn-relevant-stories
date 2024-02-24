from hackernews import HackerNews
import nltk
from nltk.stem import WordNetLemmatizer
from flask import Flask, request, jsonify
import asyncio

flask = Flask(__name__)

def hn_parse(limit=500):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    hn = HackerNews()
    top_stories = hn.top_stories(limit=limit)
    # Closing event loop
    loop.close()
    return top_stories
def lemmatize(string):
    # tokenize
    words = nltk.word_tokenize(string)

    # lowercase, remove non alphanumeric, remove stopwords
    stopwords = set(nltk.corpus.stopwords.words('english'))
    words=[word.lower() for word in words if word.isalpha() and word.lower() not in stopwords]

    # tag
    tagged = nltk.pos_tag(words)

    # filter out everything but nouns (NN), proper nouns (NNP), and adjectives (JJ)
    keywords = [word for word, tag in tagged if tag in ("NN", "NNP", "JJ")]

    # lemmatization
    wnl = WordNetLemmatizer()
    lemmas = [wnl.lemmatize(word) for word in keywords]

    # dedup
    lemmas = list(dict.fromkeys(lemmas))
    return lemmas
    
def relevance_reorder(stories, bio):
    bio_l = lemmatize(bio)
    story_score = []
    for story in stories:
        # get common key words
        title_l = lemmatize(story.title)
        common_title = list(set(title_l) & set(bio_l))
        # title is scored higher, since title words are generally more relevant to subject matter
        score = len(common_title) * 2

        # score with text, links posts don't have text
        if story.text is not None:
            text_l = lemmatize(story.text)
            common_text = list(set(text_l) & set(bio_l))
            score += len(common_text)

        story_score.append((story, score))

    # return array sorted based on score, descending
    return [e[0] for e in sorted(story_score, key=lambda x: x[1], reverse=True)]

@flask.route('/api', methods=['POST'])
def api():
    bio = request.json['bio']
    stories = hn_parse(500)
    stories = relevance_reorder(stories, bio)
    top_stories = [{"title": story.title, "url": story.url} for story in stories]
    return jsonify(top_stories)

if __name__ == "__main__":
    flask.run(debug=True)
