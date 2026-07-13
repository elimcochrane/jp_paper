# trains a linearsvc on minilm embeddings of the hand labeled posts
# in: jpdata_merged_with_themes.csv
# out: theme_classifier.joblib

import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.svm import LinearSVC
import joblib

def main():
    df = pd.read_csv('jpdata_merged_with_themes.csv', encoding='utf-8', encoding_errors='replace')
    df['combined'] = df['combined'].fillna('').astype(str)
    
    labeled_df = df[(df['topic'] != -1) & (df['Theme_Specific'].notna()) & (df['Theme_Specific'] != 'other')].copy()
    
    model = SentenceTransformer('all-MiniLM-L6-v2')
    X_train = model.encode(labeled_df['combined'].tolist(), show_progress_bar=True)
    y_train = labeled_df['Theme_Specific'].tolist()

    classifier = LinearSVC(class_weight='balanced', random_state=42)
    classifier.fit(X_train, y_train)

    joblib.dump(classifier, 'theme_classifier.joblib')
    print("\nSuccess! Model saved as 'theme_classifier.joblib'")

if __name__ == "__main__":
    main()