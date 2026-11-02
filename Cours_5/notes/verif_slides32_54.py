"""Verification numerique des slides 32-54 du Cours 5 (S5 TF-IDF, S6 Word2Vec, S7, S8)."""
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

DOCS = [
    "le chat dort sur le canapé du salon",
    "le chien dort sur le tapis du salon",
    "un félin se repose sur un sofa",
    "le salon est grand et le salon est clair",
]
# variante "du" = "de" + "le" (tokenisation implicite des slides)
DOCS_SPLIT = [
    "le chat dort sur le canapé de le salon",
    "le chien dort sur le tapis de le salon",
    "un félin se repose sur un sofa",
    "le salon est grand et le salon est clair",
]

def analyse(docs, label):
    print("=" * 70)
    print(label)
    print("=" * 70)
    cv = CountVectorizer()
    X = cv.fit_transform(docs)
    vocab = cv.get_feature_names_out()
    print("vocabulaire :", len(vocab), "termes ->", list(vocab))
    print("matrice :", X.shape, "| cellules non nulles :", X.nnz,
          f"| densite : {X.nnz / (X.shape[0]*X.shape[1]):.1%}")
    df = np.asarray((X > 0).sum(axis=0)).ravel()
    print("\nterme      df  occurrences  idf_sklearn")
    for t in ["le", "salon", "dort", "chat", "félin"]:
        j = list(vocab).index(t)
        print(f"{t:8s} {df[j]:3d} {int(X[:, j].sum()):8d} {np.log((1+4)/(1+df[j]))+1:11.3f}")

    # TF-IDF reelles sklearn
    tv = TfidfVectorizer()
    T = tv.fit_transform(docs)
    print("\nidf_ scikit-learn (ordre alpha) :",
          {t: round(v, 3) for t, v in zip(tv.get_feature_names_out(), tv.idf_)
           if t in ("le", "salon", "dort", "chat", "félin")})

    for q in ["le chat", "félin salon"]:
        print(f"\n-- requete « {q} »")
        qc = cv.transform([q])
        qt = tv.transform([q])
        print("  comptages :", [round(v, 3) for v in cosine_similarity(qc, X)[0]])
        print("  tf-idf    :", [round(v, 3) for v in cosine_similarity(qt, T)[0]])

analyse(DOCS, "A. CORPUS TEL QU'IMPRIME (scikit-learn par defaut)")
analyse(DOCS_SPLIT, "B. CORPUS AVEC du -> de + le (hypothese implicite des slides)")

print("=" * 70)
print("C. ARITHMETIQUE DES ORDRES DE GRANDEUR")
print("  10 000 x 100 x 2 matrices =", 10_000 * 100 * 2)
print("  100 000 x 300 x 2 matrices =", 100_000 * 300 * 2)
print("  ratio idf(chat)/idf(le)    =", round((np.log(5/2)+1)/(np.log(5/4)+1), 3))
print("  'deux fois moins' impliquerait idf(le) =", round((np.log(5/2)+1)/2, 3))
