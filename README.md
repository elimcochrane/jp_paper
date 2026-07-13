# JP Paper

Repository for my research project "**Masculinity, Meaning, and Modernity: Linguistic Markers of Intra- and Intergroup Identity Threat Responses in r/JordanPeterson**." Manuscript currently under review.

## To run

1. Download data from [academictorrents](https://academictorrents.com/details/ba051999301b109eab37d16f027b3f49ade2de13) (full citation in manuscript) — you'll need a torrent client. Run it through LIWC-22 and save as `jpliwc.csv`.
2. **`topicmodeling.py`** — initial topic modeling via BERTopic.
3. **`makethemes.py`** — pulls representative posts for each topic to make interpretation easier.
4. **Manual labeling** — fill in the `Theme` column of `bertopic_themes_readable.csv`. My labels are included in this repo.
5. **`mergethemes.py`** — joins manual themes onto the BERTopic topics.
6. **`trainmodel.py`** — trains a LinearSVC on embeddings of the manually labeled posts.
7. **`trainedthemeassign.py`** — embeds outlier posts and assigns themes using the trained model.
8. **`MMM_Analysis.qmd`** — switch to R; contains all analyses reported in the manuscript.

## Dependencies

**Python:** pandas, numpy, nltk, bertopic, tqdm, sentence-transformers, scikit-learn, joblib

**R:** tidyverse, tidyLPA, nlme, lubridate, scales
