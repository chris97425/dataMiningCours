"""Outils fournis aux étudiants : E/S, image et métriques, hors algorithmes à coder.

Ce fichier est volontairement distinct du corrigé src/pipeline.py et src/solution.py.
Il peut être distribué seul avec le notebook étudiant.
"""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path
from typing import Any, Iterable, Sequence

import numpy as np


def lire_jsonl(chemin):
    with Path(chemin).open(encoding="utf-8") as f:
        return [json.loads(ligne) for ligne in f if ligne.strip()]


def ecrire_jsonl(chemin, documents):
    chemin = Path(chemin)
    chemin.parent.mkdir(parents=True, exist_ok=True)
    with chemin.open("w", encoding="utf-8", newline="\n") as f:
        for doc in documents:
            f.write(json.dumps(doc, ensure_ascii=False) + "\n")


def hachage_fichier(chemin):
    digest = hashlib.sha256()
    with Path(chemin).open("rb") as f:
        for bloc in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(bloc)
    return digest.hexdigest()


def _dct(n):
    k = np.arange(n)[:, None]
    x = np.arange(n)[None, :]
    mat = np.cos(np.pi * k * (2 * x + 1) / (2 * n))
    mat[0, :] *= 1 / math.sqrt(2)
    return mat * math.sqrt(2 / n)


def phash_hex(chemin):
    """Empreinte perceptuelle 64 bits fournie : DCT 32x32, bloc 8x8."""
    from PIL import Image
    with Image.open(chemin) as im:
        pixels = np.asarray(im.convert("L").resize((32, 32), Image.Resampling.LANCZOS), dtype=float)
    dct = _dct(32)
    valeurs = (dct @ pixels @ dct.T)[:8, :8].flatten()
    mediane = np.median(valeurs[1:])
    entier = 0
    for bit in (valeurs > mediane):
        entier = (entier << 1) | int(bit)
    return f"{entier:016x}"


def distance_hamming_hex(a, b):
    if len(a) != len(b):
        raise ValueError("Empreintes de tailles différentes")
    return bin(int(a, 16) ^ int(b, 16)).count("1")


class MoteurTfidf:
    """Moteur fourni pour garantir une comparaison à paramètres identiques."""
    def __init__(self):
        from sklearn.feature_extraction.text import TfidfVectorizer
        self.vectorizer = TfidfVectorizer(lowercase=True, strip_accents="unicode", ngram_range=(1, 2), norm="l2")
        self.ids, self.entites = [], []
        self.matrice = None

    def fit(self, documents):
        self.ids = [str(x["chunk_id"]) for x in documents]
        self.entites = [str(x["entity_id"]) for x in documents]
        textes = [str(x.get("text", "")) for x in documents]
        self.matrice = self.vectorizer.fit_transform(textes) if textes else None
        return self

    def search(self, requete, k=5):
        if self.matrice is None or not str(requete).strip():
            return []
        q = self.vectorizer.transform([requete])
        if q.nnz == 0:
            return []
        scores = (self.matrice @ q.T).toarray().ravel()
        ordre = np.argsort(-scores, kind="stable")[:k]
        return [{"chunk_id": self.ids[i], "entity_id": self.entites[i], "score": float(scores[i])} for i in ordre if scores[i] > 0]


def evaluer_recherche(moteur, questions, k=5):
    """Hit@k et MRR@k au niveau entité, fournis pour le socle de l'atelier."""
    details = []
    for question in questions:
        resultats = moteur.search(question["question"], k=k)
        entites = list(dict.fromkeys(x["entity_id"] for x in resultats))
        cible = question["entity_id_cible"]
        rang = entites.index(cible) + 1 if cible in entites else None
        details.append({"question_id": question["question_id"], "cible": cible, "rang": rang, "reciproque": 1 / rang if rang else 0.0})
    return {
        "n_questions": len(details),
        "recall_at_k": sum(x["rang"] is not None for x in details) / len(details),
        "mrr_at_k": sum(x["reciproque"] for x in details) / len(details),
        "hit_at_1": sum(x["rang"] == 1 for x in details) / len(details),
        "hit_at_3": sum(x["rang"] is not None and x["rang"] <= 3 for x in details) / len(details),
        "details": details,
    }


def documents_depuis_vues(vues, variante):
    champ = {"brut": "text_brut", "nettoye": "text_nettoye", "enrichi": "text_enrichi"}[variante]
    return [{"chunk_id": x["doc_id"], "entity_id": x["entity_id"], "text": x[champ]} for x in vues]


def metriques_paires(y_vrai, y_predit):
    """TP/FP/FN/TN et P/R/F1 sur des paires effectivement annotées."""
    vrai, pred = list(map(int, y_vrai)), list(map(int, y_predit))
    assert len(vrai) == len(pred) and set(vrai + pred) <= {0, 1}
    tp = sum(y == p == 1 for y, p in zip(vrai, pred))
    fp = sum(y == 0 and p == 1 for y, p in zip(vrai, pred))
    fn = sum(y == 1 and p == 0 for y, p in zip(vrai, pred))
    tn = sum(y == p == 0 for y, p in zip(vrai, pred))
    precision = tp / (tp + fp) if tp + fp else 0
    rappel = tp / (tp + fn) if tp + fn else 0
    f1 = 2 * precision * rappel / (precision + rappel) if precision + rappel else 0
    return {"TP": tp, "FP": fp, "FN": fn, "TN": tn, "precision": precision, "rappel": rappel, "F1": f1}


def valider_export_minimal(documents: Iterable[dict[str, Any]]):
    """Contrôle de forme fourni ; les règles métier restent à justifier."""
    champs = {"chunk_id", "entity_id", "text", "source", "source_id", "url", "date_collecte", "licence", "mode_production", "est_synthetique", "hash_texte", "parents_ids"}
    ids = set()
    for doc in documents:
        assert not champs - set(doc), f"Champs manquants : {champs - set(doc)}"
        assert doc["chunk_id"] not in ids, f"chunk_id dupliqué : {doc['chunk_id']}"
        assert isinstance(doc["text"], str) and doc["text"].strip(), "Texte vide"
        assert isinstance(doc["est_synthetique"], bool), "Booléen synthétique attendu"
        assert doc["hash_texte"] == hashlib.sha256(doc["text"].encode("utf-8")).hexdigest(), "hash_texte incohérent"
        assert isinstance(doc["parents_ids"], list), "parents_ids doit être une liste"
        ids.add(doc["chunk_id"])
    return True
