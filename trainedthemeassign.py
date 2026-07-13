# assigned themes to bertopic outliers using the trained classifier
# in: jpdata_merged_with_themes.csv, theme_classifier.joblib
# out: jpdata_fully_themed_0.0.csv for R

import pandas as pd
from sentence_transformers import SentenceTransformer
import joblib
import numpy as np

confidence_threshold = 0.0

def main():
    df = pd.read_csv('jpdata_merged_with_themes.csv', encoding='utf-8', encoding_errors='replace')
    df['combined'] = df['combined'].fillna('').astype(str)

    # split
    labeled_df = df[(df['topic'] != -1) & (df['Theme_Specific'].notna()) & (df['Theme_Specific'] != 'other')].copy()
    outlier_df = df[df['topic'] == -1].copy()
    
    # load embedding model and trained classifier
    model = SentenceTransformer('all-MiniLM-L6-v2')
    classifier = joblib.load('theme_classifier.joblib')

    # generate embeddings
    X_outliers = model.encode(outlier_df['combined'].tolist(), show_progress_bar=True)
    
    # predict themes and get confidence scores
    predicted_themes = classifier.predict(X_outliers)
    confidence_scores = np.max(classifier.decision_function(X_outliers), axis=1)
    
    outlier_df['Theme_Specific'] = predicted_themes
    outlier_df['Prediction_Confidence'] = confidence_scores
    
    outlier_df.loc[outlier_df['Prediction_Confidence'] < confidence_threshold, 'Theme_Specific'] = 'other'

    labeled_df['Prediction_Confidence'] = 1.0 
    final_df = pd.concat([labeled_df, outlier_df], ignore_index=True)
    
    output_filename = f'jpdata_fully_themed_{confidence_threshold}.csv'
    final_df.to_csv(output_filename, index=False)
    
if __name__ == "__main__":
    main()