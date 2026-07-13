# attached 3 original example posts to each bertopic topic for assigning themes
# in: bertopic_theme_descriptions.csv, jpdata_with_topics.csv, jpliwc.csv
# out: bertopic_themes_readable.csv (themes filled in manually after)

import pandas as pd
import re

def main():
    try:
        themes_df = pd.read_csv('bertopic_theme_descriptions.csv')
        topics_df = pd.read_csv('jpdata_with_topics.csv')
        original_df = pd.read_csv('jpliwc.csv')
    except FileNotFoundError as e:
        print(f"Error loading files: {e}")
        return

    # get reddit id from permalink
    topics_df['id'] = topics_df['permalink'].str.extract(r'/comments/([^/]+)')
    original_df['id'] = original_df['permalink'].str.extract(r'/comments/([^/]+)')

    original_text_df = original_df[['id', 'title', 'selftext']].copy()

    merged_df = pd.merge(topics_df, original_text_df, on='id', how='left')

    merged_df['full_text'] = "TITLE: " + merged_df['title'].fillna('[No Title]') + " \nPOST: " + merged_df['selftext'].fillna('[No Text]')

    #store example posts
    ex1_dict, ex2_dict, ex3_dict = {}, {}, {}

    for topic_id, group in merged_df.groupby('topic'):
        texts = group['full_text'].dropna().unique()
        
        ex1_dict[topic_id] = texts[0] if len(texts) > 0 else ""
        ex2_dict[topic_id] = texts[1] if len(texts) > 1 else ""
        ex3_dict[topic_id] = texts[2] if len(texts) > 2 else ""

    themes_df['Original_Post_1'] = themes_df['Topic'].map(ex1_dict)
    themes_df['Original_Post_2'] = themes_df['Topic'].map(ex2_dict)
    themes_df['Original_Post_3'] = themes_df['Topic'].map(ex3_dict)

    # clean
    cols_to_drop = ['Example_Post_1', 'Example_Post_2', 'Example_Post_3']
    themes_df = themes_df.drop(columns=[c for c in cols_to_drop if c in themes_df.columns])

    output_filename = 'bertopic_themes_readable.csv'
    themes_df.to_csv(output_filename, index=False)
    
if __name__ == "__main__":
    main()