"""Vidéo d'introduction Manim — De l'ingestion des données au dédoublonnage (RAG).

Style aligné avec le mini-cours Bold Signal (#141414 / #FF5A1F / #F5F5F5).
Thèse visuelle : trois sources hétérogènes, bruitées et dupliquées traversent
cinq transformations jusqu'à produire des chunks propres, citables et uniques.

Smoke test :
    manim -ql videos/scene_intro_ingestion_dedup.py IntroIngestionDedup
Rendu HD + miniature :
    manim -qh videos/scene_intro_ingestion_dedup.py IntroIngestionDedup
    manim -qh -s videos/scene_intro_ingestion_dedup.py PosterIngestionDedup
"""
from __future__ import annotations

from manim import (
    DOWN,
    LEFT,
    ORIGIN,
    RIGHT,
    UP,
    Arrow,
    Cross,
    FadeIn,
    FadeOut,
    GrowArrow,
    Indicate,
    LaggedStart,
    Line,
    ReplacementTransform,
    RoundedRectangle,
    Scene,
    SurroundingRectangle,
    Text,
    VGroup,
    Write,
    config,
)

# Palette Bold Signal
BG = "#141414"
SURFACE = "#1E1E1E"
SURFACE_DARK = "#181818"
BORDER = "#3A3A3A"
INK = "#F5F5F5"
MUTED = "#A3A3A3"
SIGNAL = "#FF5A1F"
SIGNAL_INK = "#141414"
OK = "#3FB950"
DANGER = "#EF4444"

FONT_SANS = "Avenir Next"
FONT_MONO = "Menlo"

config.background_color = BG


def make_card(
    title: str,
    subtitle: str = "",
    width: float = 3.2,
    height: float = 1.1,
    fill: str = SURFACE,
    stroke: str = BORDER,
    title_color: str = INK,
    sub_color: str = MUTED,
    mono_sub: bool = False,
    title_size: int = 22,
    sub_size: int = 16,
) -> VGroup:
    """Construit une carte arrondie lisible, sans débordement de texte."""
    rect = RoundedRectangle(
        corner_radius=0.14,
        width=width,
        height=height,
        fill_color=fill,
        fill_opacity=1.0,
        stroke_color=stroke,
        stroke_width=2.0,
    )
    t = Text(title, font=FONT_SANS, weight="BOLD", font_size=title_size, color=title_color)
    max_w = width - 0.36
    if t.width > max_w:
        t.scale_to_fit_width(max_w)

    if subtitle:
        s = Text(
            subtitle,
            font=FONT_MONO if mono_sub else FONT_SANS,
            font_size=sub_size,
            color=sub_color,
        )
        if s.width > max_w:
            s.scale_to_fit_width(max_w)
        labels = VGroup(t, s).arrange(DOWN, buff=0.10)
    else:
        labels = VGroup(t)

    if labels.height > height - 0.24:
        labels.scale_to_fit_height(height - 0.24)
    labels.move_to(rect.get_center())
    return VGroup(rect, labels)


def make_pill(
    label: str,
    active: bool = False,
    done: bool = False,
    font_size: int = 16,
    pad_x: float = 0.24,
    pad_y: float = 0.12,
) -> VGroup:
    """Pastille d'étape ou de métadonnée."""
    if active:
        fill, stroke, col = SIGNAL, SIGNAL, SIGNAL_INK
    elif done:
        fill, stroke, col = "#242424", OK, OK
    else:
        fill, stroke, col = SURFACE, BORDER, MUTED

    txt = Text(
        label,
        font=FONT_SANS,
        weight="BOLD" if active else "MEDIUM",
        font_size=font_size,
        color=col,
    )
    bg = RoundedRectangle(
        corner_radius=0.16,
        width=txt.width + pad_x * 2,
        height=txt.height + pad_y * 2,
        fill_color=fill,
        fill_opacity=1.0,
        stroke_color=stroke,
        stroke_width=1.8,
    )
    txt.move_to(bg.get_center())
    return VGroup(bg, txt)


def make_stepper(active_idx: int) -> VGroup:
    """Rail des 5 étapes fixé en bas d'écran (principe de signaling)."""
    labels = ["1 Collecte", "2 Parse", "3 Nettoyage", "4 Chunks", "5 Dédup"]
    items = []
    for i, label in enumerate(labels):
        items.append(make_pill(label, active=(i == active_idx), done=(i < active_idx), font_size=15))
        if i < len(labels) - 1:
            items.append(Text("→", font=FONT_SANS, font_size=18, color=SIGNAL if i < active_idx else BORDER))
    rail = VGroup(*items).arrange(RIGHT, buff=0.16)
    if rail.width > 12.2:
        rail.scale_to_fit_width(12.2)
    rail.to_edge(DOWN, buff=0.35)
    return rail


def make_header(eyebrow: str, headline: str) -> VGroup:
    """En-tête cohérent sur chaque scène (eyebrow orange + titre gras)."""
    eb = Text(eyebrow.upper(), font=FONT_SANS, weight="BOLD", font_size=18, color=SIGNAL)
    hl = Text(headline, font=FONT_SANS, weight="BOLD", font_size=34, color=INK)
    if hl.width > 12.4:
        hl.scale_to_fit_width(12.4)
    grp = VGroup(eb, hl).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
    grp.to_corner(UP + LEFT, buff=0.48)
    return grp


class IntroIngestionDedup(Scene):
    """Animation complète (~50 s) : de 3 sources brutes au corpus dédoublonné."""

    def construct(self):
        # Barre fine d'accent en haut
        top_bar = Line(LEFT * 7.11, RIGHT * 7.11, stroke_width=4, color=SIGNAL).to_edge(UP, buff=0)
        self.add(top_bar)

        self.scene_0_title()
        self.scene_1_collecte()
        self.scene_2_parse()
        self.scene_3_nettoyage()
        self.scene_4_chunks()
        self.scene_5_dedup()

    # ------------------------------------------------------------------
    # SCÈNE 0 — Titre & promesse
    # ------------------------------------------------------------------
    def scene_0_title(self):
        kicker = Text("PIPELINE RAG · PARTIE INGESTION", font=FONT_SANS, weight="BOLD", font_size=20, color=SIGNAL)
        title = Text("Ingestion → Dédoublonnage", font=FONT_SANS, weight="BOLD", font_size=56, color=INK)
        sub = Text(
            "De 3 sources brutes à des chunks propres, citables et uniques",
            font=FONT_SANS,
            font_size=24,
            color=MUTED,
        )
        header = VGroup(kicker, title, sub).arrange(DOWN, buff=0.28).shift(UP * 0.7)

        rail = make_stepper(active_idx=-1).move_to(DOWN * 1.45)

        self.play(FadeIn(kicker, shift=UP * 0.15), Write(title), run_time=1.2)
        self.play(FadeIn(sub, shift=UP * 0.15), run_time=0.7)
        self.play(LaggedStart(*[FadeIn(m, shift=UP * 0.15) for m in rail], lag_ratio=0.07), run_time=1.3)
        self.wait(1.4)
        self.play(FadeOut(header, shift=UP * 0.2), FadeOut(rail), run_time=0.7)

    # ------------------------------------------------------------------
    # SCÈNE 1 — Collecte (3 sources hétérogènes → Entrepôt)
    # ------------------------------------------------------------------
    def scene_1_collecte(self):
        header = make_header("Étape 01 · Collecte", "Un même lieu arrive éclaté en 3 sources brutes")
        rail = make_stepper(active_idx=0)
        self.play(FadeIn(header, shift=RIGHT * 0.2), FadeIn(rail), run_time=0.6)

        # 3 sources réelles du TP
        src_pop = make_card("POP / Mérimée", "CSV · ACR0001729", width=3.5, height=1.05, mono_sub=True)
        src_wiki = make_card("Wikidata / Wikipédia", "JSONL · Q3329255", width=3.5, height=1.05, mono_sub=True)
        src_img = make_card("Wikimedia Commons", "JPG · CC BY-SA 4.0", width=3.5, height=1.05, mono_sub=True)
        sources = VGroup(src_pop, src_wiki, src_img).arrange(DOWN, buff=0.35).move_to(LEFT * 3.8 + DOWN * 0.2)

        hub = make_card(
            "Entrepôt brut",
            "Musée Léon-Dierx\n3 formats + provenance",
            width=3.6,
            height=2.2,
            fill=SIGNAL,
            stroke=SIGNAL,
            title_color=SIGNAL_INK,
            sub_color=SIGNAL_INK,
            title_size=26,
            sub_size=17,
        ).move_to(RIGHT * 2.8 + DOWN * 0.2)

        arrows = VGroup(
            Arrow(src_pop.get_right(), hub.get_left() + UP * 0.55, buff=0.18, color=SIGNAL, stroke_width=3.5),
            Arrow(src_wiki.get_right(), hub.get_left(), buff=0.18, color=SIGNAL, stroke_width=3.5),
            Arrow(src_img.get_right(), hub.get_left() + DOWN * 0.55, buff=0.18, color=SIGNAL, stroke_width=3.5),
        )

        self.play(LaggedStart(*[FadeIn(s, shift=RIGHT * 0.4) for s in sources], lag_ratio=0.18), run_time=1.3)
        self.play(FadeIn(hub, scale=0.92), run_time=0.6)
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.15), run_time=1.0)

        note = Text(
            "Impossible de donner ces fichiers bruts directement au LLM.",
            font=FONT_SANS,
            font_size=20,
            color=MUTED,
        ).next_to(rail, UP, buff=0.35)
        self.play(FadeIn(note), run_time=0.5)
        self.wait(1.8)

        self.play(FadeOut(VGroup(header, sources, hub, arrows, note, rail)), run_time=0.6)

    # ------------------------------------------------------------------
    # SCÈNE 2 — Parse (Extraire texte + structure)
    # ------------------------------------------------------------------
    def scene_2_parse(self):
        header = make_header("Étape 02 · Parse", "Extraire le texte sans perdre la structure")
        rail = make_stepper(active_idx=1)
        self.play(FadeIn(header, shift=RIGHT * 0.2), FadeIn(rail), run_time=0.6)

        raw_box = RoundedRectangle(
            corner_radius=0.14, width=3.95, height=3.1, fill_color=SURFACE_DARK, fill_opacity=1, stroke_color=BORDER, stroke_width=2
        ).move_to(LEFT * 4.35 + DOWN * 0.15)
        raw_title = Text("Brut (HTML / JSON / PDF)", font=FONT_SANS, weight="BOLD", font_size=18, color=MUTED)
        raw_code = Text(
            'REF: "ACR0001729"\nTICO: "Musée Léon-Dierx"\nCOM: ["Saint-Denis"]\n== Histoire du musée ==\nLe musée est situé...',
            font=FONT_MONO,
            font_size=14,
            color=INK,
            line_spacing=1.25,
        )
        raw_content = VGroup(raw_title, raw_code).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        if raw_content.width > 3.55:
            raw_content.scale_to_fit_width(3.55)
        raw_content.move_to(raw_box.get_center())
        raw_grp = VGroup(raw_box, raw_content)

        parser = make_card(
            "Parseur",
            "HTML · JSON · PDF · OCR",
            width=2.65,
            height=1.25,
            fill=SIGNAL,
            stroke=SIGNAL,
            title_color=SIGNAL_INK,
            sub_color=SIGNAL_INK,
            title_size=24,
            sub_size=14,
        ).move_to(LEFT * 0.05 + DOWN * 0.15)

        out_1 = make_card("Titre & commune", "Musée Léon-Dierx · Saint-Denis", width=3.85, height=0.88, sub_size=15)
        out_2 = make_card("Sections conservées", "Histoire du musée · Architecture", width=3.85, height=0.88, sub_size=15)
        out_3 = make_card("Provenance gardée", "url · date_collecte · CC BY-SA", width=3.85, height=0.88, mono_sub=True, sub_size=14)
        outputs = VGroup(out_1, out_2, out_3).arrange(DOWN, buff=0.22).move_to(RIGHT * 4.3 + DOWN * 0.15)

        a_in = Arrow(raw_box.get_right(), parser.get_left(), buff=0.16, color=SIGNAL, stroke_width=3.5)
        a_out = VGroup(
            Arrow(parser.get_right(), out_1.get_left(), buff=0.16, color=SIGNAL, stroke_width=3),
            Arrow(parser.get_right(), out_2.get_left(), buff=0.16, color=SIGNAL, stroke_width=3),
            Arrow(parser.get_right(), out_3.get_left(), buff=0.16, color=SIGNAL, stroke_width=3),
        )

        self.play(FadeIn(raw_grp, shift=RIGHT * 0.3), run_time=0.8)
        self.play(GrowArrow(a_in), FadeIn(parser, scale=0.9), run_time=0.8)
        self.play(LaggedStart(*[GrowArrow(a) for a in a_out], lag_ratio=0.12), run_time=0.7)
        self.play(LaggedStart(*[FadeIn(o, shift=RIGHT * 0.25) for o in outputs], lag_ratio=0.16), run_time=1.0)
        self.wait(2.3)

        self.play(FadeOut(VGroup(header, raw_grp, parser, a_in, a_out, outputs, rail)), run_time=0.6)

    # ------------------------------------------------------------------
    # SCÈNE 3 — Nettoyage & Normalisation (sans détruire l'affichage)
    # ------------------------------------------------------------------
    def scene_3_nettoyage(self):
        header = make_header("Étape 03 · Nettoyage", "Retirer le bruit, normaliser sans effacer le sens")
        rail = make_stepper(active_idx=2)
        self.play(FadeIn(header, shift=RIGHT * 0.2), FadeIn(rail), run_time=0.6)

        noise_1 = make_card("Bruit répétitif", "« Confidentiel · Page 12 »", width=4.0, height=0.95, stroke=DANGER, sub_color=DANGER, mono_sub=True)
        noise_2 = make_card("Unicode décomposé", "e\\u0301glise  +  espaces\\u00a0", width=4.0, height=0.95, stroke=SIGNAL, sub_color=INK, mono_sub=True)
        noise_3 = make_card("Commune inversée", "Tampon (Le)", width=4.0, height=0.95, stroke=SIGNAL, sub_color=INK, mono_sub=True)
        left_col = VGroup(noise_1, noise_2, noise_3).arrange(DOWN, buff=0.28).move_to(LEFT * 3.7 + DOWN * 0.15)

        self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.3) for c in left_col], lag_ratio=0.16), run_time=1.0)
        self.wait(0.5)

        # Barrer le bruit
        cross = Cross(noise_1, stroke_color=DANGER, stroke_width=5)
        self.play(Write(cross), run_time=0.6)
        self.play(noise_1.animate.set_opacity(0.28), cross.animate.set_opacity(0.55), run_time=0.5)

        # Deux sorties propres à droite
        out_disp = make_card(
            "Affichage propre (NFC)",
            "église  ·  Le Tampon",
            width=4.6,
            height=1.25,
            fill=SURFACE,
            stroke=OK,
            title_color=OK,
            sub_color=INK,
            title_size=22,
            sub_size=20,
        )
        out_key = make_card(
            "Clé de comparaison",
            "eglise  ·  le tampon",
            width=4.6,
            height=1.25,
            fill=SURFACE,
            stroke=SIGNAL,
            title_color=SIGNAL,
            sub_color=INK,
            mono_sub=True,
            title_size=22,
            sub_size=19,
        )
        right_col = VGroup(out_disp, out_key).arrange(DOWN, buff=0.4).move_to(RIGHT * 3.2 + DOWN * 0.15)

        a1 = Arrow(noise_2.get_right(), out_disp.get_left(), buff=0.2, color=OK, stroke_width=3.5)
        a2 = Arrow(noise_3.get_right(), out_key.get_left(), buff=0.2, color=SIGNAL, stroke_width=3.5)

        self.play(GrowArrow(a1), FadeIn(out_disp, shift=RIGHT * 0.25), run_time=0.9)
        self.play(GrowArrow(a2), FadeIn(out_key, shift=RIGHT * 0.25), run_time=0.9)
        self.wait(2.3)

        self.play(FadeOut(VGroup(header, left_col, cross, right_col, a1, a2, rail)), run_time=0.6)

    # ------------------------------------------------------------------
    # SCÈNE 4 — Chunks & Métadonnées (chevauchement + carte d'identité)
    # ------------------------------------------------------------------
    def scene_4_chunks(self):
        header = make_header("Étape 04 · Chunks & Métadonnées", "Découper sans couper une idée, garder la source")
        rail = make_stepper(active_idx=3)
        self.play(FadeIn(header, shift=RIGHT * 0.2), FadeIn(rail), run_time=0.6)

        # Long texte continu qui se découpe
        doc_bar = make_card(
            "Article Wikipédia propre · Musée Léon-Dierx",
            "8 212 caractères — trop long pour un seul vecteur précis",
            width=10.6,
            height=1.15,
            fill=SURFACE,
            stroke=BORDER,
            title_size=23,
            sub_size=17,
        ).move_to(UP * 1.1)
        self.play(FadeIn(doc_bar, shift=DOWN * 0.2), run_time=0.8)
        self.wait(0.6)

        # 3 blocs : Chunk A | Overlap | Chunk B
        ch_a = make_card("Chunk A", "mots 1 → 90", width=3.7, height=1.35, fill=SURFACE, stroke=SIGNAL, sub_color=INK)
        ov = make_card(
            "Overlap 15 %",
            "contexte partagé",
            width=2.7,
            height=1.35,
            fill=SIGNAL,
            stroke=SIGNAL,
            title_color=SIGNAL_INK,
            sub_color=SIGNAL_INK,
            title_size=20,
            sub_size=15,
        )
        ch_b = make_card("Chunk B", "mots 76 → 165", width=3.7, height=1.35, fill=SURFACE, stroke=SIGNAL, sub_color=INK)
        chunks_row = VGroup(ch_a, ov, ch_b).arrange(RIGHT, buff=0.22).move_to(DOWN * 0.55)

        self.play(ReplacementTransform(doc_bar.copy(), chunks_row), doc_bar.animate.set_opacity(0.32), run_time=1.1)
        self.play(Indicate(ov, color=INK, scale_factor=1.06), run_time=0.8)

        # Métadonnées attachées
        meta_label = Text("Carte d'identité attachée à chaque chunk :", font=FONT_SANS, font_size=18, color=MUTED)
        tags = VGroup(
            make_pill("entity_id: Q3329255", font_size=15),
            make_pill("source: Wikipédia", font_size=15),
            make_pill("url + date", font_size=15),
            make_pill("licence: CC BY-SA", font_size=15),
        ).arrange(RIGHT, buff=0.18)
        meta_grp = VGroup(meta_label, tags).arrange(DOWN, buff=0.18).move_to(DOWN * 2.1)
        if meta_grp.width > 12.2:
            meta_grp.scale_to_fit_width(12.2)

        self.play(FadeIn(meta_label), LaggedStart(*[FadeIn(t, shift=UP * 0.15) for t in tags], lag_ratio=0.12), run_time=1.1)
        self.wait(2.3)

        self.play(FadeOut(VGroup(header, doc_bar, chunks_row, meta_grp, rail)), run_time=0.6)

    # ------------------------------------------------------------------
    # SCÈNE 5 — Dédoublonnage & ID stable (fin de chaîne)
    # ------------------------------------------------------------------
    def scene_5_dedup(self):
        header = make_header("Étape 05 · Dédoublonnage", "Supprimer les copies, attribuer un ID stable")
        rail = make_stepper(active_idx=4)
        self.play(FadeIn(header, shift=RIGHT * 0.2), FadeIn(rail), run_time=0.6)

        # Gauche : 2 types de doublons réels du TP
        pair1_a = make_card("PA97400011 : original", "sha256: a91f…c3", width=3.45, height=0.80, mono_sub=True, title_size=17, sub_size=14)
        pair1_b = make_card("PA97400011 : copie_1", "sha256: a91f…c3", width=3.45, height=0.80, stroke=DANGER, mono_sub=True, title_size=17, sub_size=14)

        pair2_a = make_card("photo.jpg (original)", "pHash: f08c… · d = 0", width=3.45, height=0.80, mono_sub=True, title_size=17, sub_size=14)
        pair2_b = make_card("variante_08.jpg", "SHA ≠ · pHash d = 0", width=3.45, height=0.80, stroke=DANGER, mono_sub=True, title_size=17, sub_size=14)

        left_items = VGroup(pair1_a, pair1_b, pair2_a, pair2_b).arrange(DOWN, buff=0.22).move_to(LEFT * 4.55 + DOWN * 0.05)

        dedup = make_card(
            "Dédoublonneur",
            "SHA-256 · Levenshtein\nJaccard · pHash",
            width=2.7,
            height=1.75,
            fill=SIGNAL,
            stroke=SIGNAL,
            title_color=SIGNAL_INK,
            sub_color=SIGNAL_INK,
            title_size=21,
            sub_size=13,
        ).move_to(LEFT * 0.15 + DOWN * 0.05)

        out_box = make_card(
            "Corpus RAG unique",
            "chunk_id stable (sha256)\n0 doublon · provenance OK\n→ Prêt pour embeddings",
            width=3.85,
            height=2.15,
            fill=SURFACE,
            stroke=OK,
            title_color=OK,
            sub_color=INK,
            title_size=23,
            sub_size=15,
        ).move_to(RIGHT * 4.35 + DOWN * 0.05)

        arr_mid = Arrow(dedup.get_right(), out_box.get_left(), buff=0.18, color=OK, stroke_width=4)
        arr_in1 = Arrow(pair1_a.get_right(), dedup.get_left() + UP * 0.45, buff=0.16, color=SIGNAL, stroke_width=3.2)
        arr_in2 = Arrow(pair2_a.get_right(), dedup.get_left() + DOWN * 0.45, buff=0.16, color=SIGNAL, stroke_width=3.2)

        self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.25) for c in left_items], lag_ratio=0.12), run_time=1.1)
        self.play(FadeIn(dedup, scale=0.92), run_time=0.6)

        # Éliminer les 2 doublons visuellement
        c1 = Cross(pair1_b, stroke_color=DANGER, stroke_width=4.5)
        c2 = Cross(pair2_b, stroke_color=DANGER, stroke_width=4.5)
        self.play(Write(c1), Write(c2), run_time=0.7)
        self.play(
            pair1_b.animate.set_opacity(0.22),
            pair2_b.animate.set_opacity(0.22),
            c1.animate.set_opacity(0.55),
            c2.animate.set_opacity(0.55),
            run_time=0.5,
        )

        # Faire passer les représentants vers le corpus unique
        self.play(GrowArrow(arr_in1), GrowArrow(arr_in2), run_time=0.7)
        self.play(GrowArrow(arr_mid), FadeIn(out_box, scale=0.94), run_time=0.9)
        self.play(Indicate(out_box[0], color=OK, scale_factor=1.03), run_time=0.7)

        outro = Text(
            "Suite du pipeline : Embeddings → Index vectoriel → Recherche hybride",
            font=FONT_SANS,
            font_size=19,
            color=MUTED,
        ).next_to(rail, UP, buff=0.28)
        self.play(FadeIn(outro, shift=UP * 0.1), run_time=0.6)
        self.wait(2.8)


class PosterIngestionDedup(Scene):
    """Frame statique 16:9 propre servant de miniature / poster vidéo."""

    def construct(self):
        top_bar = Line(LEFT * 7.11, RIGHT * 7.11, stroke_width=5, color=SIGNAL).to_edge(UP, buff=0)
        kicker = Text("MINI-COURS · PIPELINE RAG", font=FONT_SANS, weight="BOLD", font_size=22, color=SIGNAL)
        title = Text("Ingestion → Dédoublonnage", font=FONT_SANS, weight="BOLD", font_size=60, color=INK)
        sub = Text(
            "Comment passer de 3 sources brutes à un corpus RAG propre, citable et unique",
            font=FONT_SANS,
            font_size=23,
            color=MUTED,
        )
        head = VGroup(kicker, title, sub).arrange(DOWN, buff=0.25).shift(UP * 1.15)

        steps = VGroup(
            make_card("01 Collecte", "POP · Wiki · Commons", width=2.05, height=1.25, title_size=18, sub_size=13),
            make_card("02 Parse", "Texte + structure", width=2.05, height=1.25, title_size=18, sub_size=13),
            make_card("03 Nettoyage", "NFC + clé", width=2.05, height=1.25, title_size=18, sub_size=13),
            make_card("04 Chunks", "Overlap + source", width=2.05, height=1.25, title_size=18, sub_size=13),
            make_card(
                "05 Dédup",
                "SHA · pHash · ID",
                width=2.05,
                height=1.25,
                fill=SIGNAL,
                stroke=SIGNAL,
                title_color=SIGNAL_INK,
                sub_color=SIGNAL_INK,
                title_size=18,
                sub_size=13,
            ),
        ).arrange(RIGHT, buff=0.46).move_to(DOWN * 1.25)

        arrows = VGroup(
            *[
                Arrow(steps[i].get_right(), steps[i + 1].get_left(), buff=0.07, color=SIGNAL, stroke_width=3.5)
                for i in range(4)
            ]
        )

        self.add(top_bar, head, steps, arrows)
