# runs bertopic
# in: jpliwc.csv
# out: jpdata_with_topics.csv, bertopic_theme_descriptions.csv

import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from bertopic import BERTopic
from tqdm import tqdm

nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True) 
nltk.download('stopwords', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)
nltk.download('averaged_perceptron_tagger_eng', quiet=True) 
nltk.download('wordnet', quiet=True)

stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def preprocess(text):
    tokens = word_tokenize(text.lower())
    tokens = [w for w in tokens if w.isalpha()]
    tokens = [w for w in tokens if w not in stop_words]
    tagged_tokens = nltk.pos_tag(tokens) 
    allowed_tags = ['NN', 'NNS', 'NNP', 'NNPS', 'JJ', 'JJR', 'JJS']
    filtered_tokens = [w for w, tag in tagged_tokens if tag in allowed_tags]
    final_tokens = [lemmatizer.lemmatize(w) for w in filtered_tokens]
    return final_tokens

def main():
    df = pd.read_csv('jpliwc.csv').copy() 

    # combine columns
    df['combined'] = df['title'].fillna('') + " " + df['selftext'].fillna('')
    
    tqdm.pandas(desc="preprocessing")
    
    # .progress_apply to see the bar
    df['tokens'] = df['combined'].progress_apply(preprocess)
    
    # filter and prep docs
    df = df[df['tokens'].apply(len) >= 10]
    df['bertopic_docs'] = df['tokens'].apply(lambda x: ' '.join(x))
    docs = df['bertopic_docs'].tolist()
    
    # run bertopic
    topic_model = BERTopic(language="english", verbose=True, calculate_probabilities=True)
    topics, probabilities = topic_model.fit_transform(docs)
    
    new_topics = topic_model.reduce_outliers(
        docs, 
        topics, 
        probabilities=probabilities, 
        strategy="probabilities", 
        threshold=0.10 # threshold
    )
    
    # topic info + representative posts
    topic_info = topic_model.get_topic_info()
    
    example_1, example_2, example_3 = [], [], []
    for topic_id in topic_info['Topic']:
        rep_docs = topic_model.get_representative_docs(topic_id)
        if rep_docs:
            example_1.append(rep_docs[0] if len(rep_docs) > 0 else "")
            example_2.append(rep_docs[1] if len(rep_docs) > 1 else "")
            example_3.append(rep_docs[2] if len(rep_docs) > 2 else "")
        else:
            example_1.append("")
            example_2.append("")
            example_3.append("")
            
    topic_info['Example_Post_1'] = example_1
    topic_info['Example_Post_2'] = example_2
    topic_info['Example_Post_3'] = example_3
    
    if 'Representative_Docs' in topic_info.columns:
        topic_info = topic_info.drop(columns=['Representative_Docs'])

    topic_info.to_csv('bertopic_theme_descriptions.csv', index=False)
    
    df['topic'] = new_topics 
    df = df.drop(columns=['title', 'selftext', 'tokens', 'bertopic_docs'])
    df.to_csv('jpdata_with_topics.csv', index=False)

if __name__ == "__main__":
    main()