# joins hand-labeled themes back onto the post-level data
# in: jpdata_with_topics.csv, bertopic_themes_readable.csv
# out: jpdata_merged_with_themes.csv

import pandas as pd

def main():
    # main_df contains posts and the 'topic' column from bertopic
    main_df = pd.read_csv('jpdata_with_topics.csv', encoding='utf-8', encoding_errors='replace')
    
    # themes_df contains the 'Topic' and 'Theme' columns 
    themes_df = pd.read_csv('bertopic_themes_readable.csv')

    theme_mapping = themes_df[['Topic', 'Theme']].copy()

    theme_mapping = theme_mapping.rename(columns={
        'Topic': 'topic', 
        'Theme': 'Theme_Specific'
    })

    merged_df = pd.merge(main_df, theme_mapping, on='topic', how='left')

    output_filename = 'jpdata_merged_with_themes.csv'
    merged_df.to_csv(output_filename, index=False)
    
if __name__ == "__main__":
    main()