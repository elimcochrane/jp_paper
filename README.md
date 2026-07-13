# jp_paper
Repository for my research project "**Masculinity, Meaning, and Modernity: Linguistic Markers of Intra- and Intergroup Identity Threat Responses in r/JordanPeterson"**. Manuscript currently under review.

**To run:**
1. Download data from https://academictorrents.com/details/ba051999301b109eab37d16f027b3f49ade2de13 (full citation in manuscript) - you'll need a torrent client - run it through liwc and call that jpliwc.csv
2. Run topicmodeling.py for initial topic modeling via bertopic
3. Run makethemes.py to find some representative posts for each topic
4. Manual labeling update bertopic_themes_readable.py - my manual ones are in the data file
5. Run mergethemes.py to join manual themes onto bertopic output topics
6. Run trainmodel.py to train a linearsvc on embeddings of manual themes
7. Run trainedthemeassign.py to embed outlier posts and assign more themes using the new model
8. Switch to R and run MMM_Analysis.qmd for all analyses used in the manuscript

**Dependencies:** pandas, numpy, nltk, bertopic, tqdm, sentence-transformers, scikit-learn, joblib
