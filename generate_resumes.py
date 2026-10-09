#!/usr/bin/env python3
"""Generate nine two-page public resumes from one multilingual factual source.

Run with Python 3 and ReportLab. Output names remain stable for existing links.
Historical application-specific resumes are maintained outside this repository.
"""

from html import escape
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    HRFlowable, KeepTogether, PageBreak, Paragraph, SimpleDocTemplate, Spacer,
)


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "assets" / "resumes"
ROLES = ("GameDev", "UnityDev", "SoftwareDev")
LANGS = {"EN": "en", "FR": "fr", "PT-BR": "ptbr"}
NAME = "Fernando Silva da Luz"
BLUE = colors.HexColor("#2c5aa0")
INK = colors.HexColor("#1a1a1a")
MUTED = colors.HexColor("#555555")

# Keep specialized tenure separate from the user's 13+ years in software.
TITLES = {
    "GameDev": {
        "en": "Senior Software Engineer | Game Development",
        "fr": "Développeur logiciel senior | Développement de jeux",
        "ptbr": "Desenvolvedor de Software Sênior | Jogos",
    },
    "UnityDev": {
        "en": "Senior Software Engineer | Unity & Interactive Applications",
        "fr": "Développeur logiciel senior | Unity et applications interactives",
        "ptbr": "Desenvolvedor de Software Sênior | Unity e Aplicações Interativas",
    },
    "SoftwareDev": {
        "en": "Senior Software Engineer | Applied AI & Product Engineering",
        "fr": "Développeur logiciel senior | IA appliquée et produits logiciels",
        "ptbr": "Desenvolvedor de Software Sênior | IA Aplicada e Produtos",
    },
}

PROFILES = {
    "GameDev": {
        "en": "Software engineer with 13+ years across medical software, computer vision, AR and games. Took CrimeTrip from prototype to Android and iOS release, including a shipped voice-based LLM feature. Developing VEKARRA, a solo Unity tactical roguelite, and currently building C++/Qt medical applications.",
        "fr": "Développeur logiciel avec plus de 13 ans d'expérience en logiciels médicaux, vision par ordinateur, réalité augmentée et jeux. Livraison de CrimeTrip, du prototype aux versions Android et iOS, avec une fonctionnalité vocale utilisant un LLM. Développement en solo de VEKARRA, un roguelite tactique sous Unity, et d'applications médicales en C++/Qt dans mon emploi actuel.",
        "ptbr": "Desenvolvedor com mais de 13 anos de experiência em software médico, visão computacional, realidade aumentada e jogos. Levei CrimeTrip do protótipo ao lançamento para Android e iOS, incluindo um recurso de voz com LLM. Desenvolvo VEKARRA, um roguelite tático solo em Unity, e aplicações médicas em C++/Qt no emprego atual.",
    },
    "UnityDev": {
        "en": "Software engineer with 13+ years in software, with experience delivering Unity games and interactive applications. Shipped CrimeTrip on Android and iOS, integrating Python services and a voice-based LLM feature. Previous work includes HoloLens 2 prototypes and a Unity-React Native bridge; current work includes C++/Qt medical software.",
        "fr": "Développeur logiciel avec plus de 13 ans d'expérience en logiciel, dont la livraison de jeux et d'applications interactives sous Unity. Livraison de CrimeTrip sur Android et iOS avec des services Python et une fonctionnalité vocale utilisant un LLM. Expérience avec des prototypes HoloLens 2 et une passerelle Unity-React Native; développement actuel de logiciels médicaux en C++/Qt.",
        "ptbr": "Desenvolvedor com mais de 13 anos de experiência em software, incluindo jogos e aplicações interativas em Unity. Lancei CrimeTrip para Android e iOS, integrando serviços Python e um recurso de voz com LLM. Atuei em protótipos HoloLens 2 e numa ponte Unity-React Native; atualmente desenvolvo software médico em C++/Qt.",
    },
    "SoftwareDev": {
        "en": "Software engineer with 13+ years across medical software, computer vision and interactive products. Built production computer-vision workflows, shipped a voice-based LLM feature in a mobile AR game, and currently develop C++/Qt medical applications. Experience spans Python services, computer-vision model training, inference, client integration and product delivery.",
        "fr": "Développeur logiciel avec plus de 13 ans d'expérience en logiciels médicaux, vision par ordinateur et produits interactifs. Création de pipelines de vision en production, livraison d'une fonctionnalité vocale utilisant un LLM dans un jeu mobile en RA, et développement actuel d'applications médicales en C++/Qt. Expérience en services Python, entraînement de modèles de vision, inférence, intégration client et livraison de produits.",
        "ptbr": "Desenvolvedor com mais de 13 anos de experiência em software médico, visão computacional e produtos interativos. Criei fluxos de visão computacional em produção, lancei um recurso de voz com LLM em um jogo mobile de RA e atualmente desenvolvo aplicações médicas em C++/Qt. Experiência em serviços Python, treinamento de modelos de visão computacional, inferência, integração e entrega de produtos.",
    },
}

LABELS = {
    "en": {"profile": "PROFILE", "experience": "PROFESSIONAL EXPERIENCE", "projects": "SELECTED PROJECTS", "skills": "TECHNICAL SKILLS", "additional": "ADDITIONAL EXPERIENCE", "education": "EDUCATION", "languages": "LANGUAGES", "continued": "Selected work and technical profile", "earlier": "Earlier roles", "availability": "Open to relocation. US sponsorship required. Canada: employer-specific work permit.", "notice": "Two weeks' notice; start date subject to work authorization."},
    "fr": {"profile": "PROFIL", "experience": "EXPÉRIENCE PROFESSIONNELLE", "projects": "PROJETS SÉLECTIONNÉS", "skills": "COMPÉTENCES TECHNIQUES", "additional": "AUTRES EXPÉRIENCES", "education": "FORMATION", "languages": "LANGUES", "continued": "Projets et profil technique", "earlier": "Postes antérieurs", "availability": "Mobilité internationale. Parrainage requis aux États-Unis. Canada : permis de travail lié à un employeur.", "notice": "Préavis de deux semaines; prise de poste selon l'autorisation de travail."},
    "ptbr": {"profile": "PERFIL", "experience": "EXPERIÊNCIA PROFISSIONAL", "projects": "PROJETOS SELECIONADOS", "skills": "COMPETÊNCIAS TÉCNICAS", "additional": "EXPERIÊNCIA ADICIONAL", "education": "FORMAÇÃO", "languages": "IDIOMAS", "continued": "Projetos e perfil técnico", "earlier": "Cargos anteriores", "availability": "Disponível para mudança. Necessito de patrocínio nos EUA. Canadá: permissão de trabalho vinculada ao empregador.", "notice": "Aviso prévio de duas semanas; início sujeito à autorização de trabalho."},
}

# The new details below are supplied by the user. No accuracy, scale or impact
# metrics are inferred. Medical work is described without confidential features.
EXPERIENCE = {
    "en": [
        {"company": "Zimmer Biomet / Orthosoft", "title": "Senior Software Developer", "dates": "Aug 2023 - Present", "bullets": [
            "Develop C++17/Qt medical applications for robotic-assisted surgery, contributing to medical-image processing and reconstruction workflows.",
            "Evaluate spatial registration methods through custom scripts and established libraries; work with VTK, ITK, Python, CMake and Conan.",
            "Contribute to backend integration of segmentation-model inference using models developed by other specialists; implement GitLab CI automation for inference runs and validation-data collection.",
            "Previously developed mixed-reality prototypes with Unity and HoloLens 2.",
        ]},
        {"company": "Prologue AI", "title": "Senior Software / Unity Developer", "dates": "Jun 2022 - Jul 2023", "bullets": [
            "Took CrimeTrip, a Unity AR adventure game, from prototype through release on Android and iOS.",
            "Built and shipped a voice-based character interrogation feature integrating speech recognition, OpenAI API responses and ElevenLabs speech synthesis.",
            "Implemented pre-request rules, persona context and keyword-based output checks; validated interaction flows through manual team QA.",
            "Built backend services with FastAPI, Azure Functions and PlayFab, integrated with a modular, event-driven Unity client using HTTP and WebSocket communication.",
        ]},
        {"company": "BairesDev", "title": "Software Engineer, Computer Vision", "dates": "Aug 2020 - Dec 2021", "bullets": [
            "Built production Python computer-vision workflows for annotation, augmentation, model training, retraining and inference, using Detectron2, OpenCV and TensorFlow.",
            "Combined 2D detections, 3D point-cloud data and camera geometry to estimate window dimensions and area from building-facade captures.",
            "Implemented capture-quality checks and coordinated image collection with the client and external contributors; built capture/detection interfaces and a Unity-React Native bridge.",
        ]},
    ],
    "fr": [
        {"company": "Zimmer Biomet / Orthosoft", "title": "Développeur logiciel senior", "dates": "août 2023 - Présent", "bullets": [
            "Développement d'applications médicales C++17/Qt pour la chirurgie assistée par robot, avec contribution au traitement et à la reconstruction d'images médicales.",
            "Évaluation de méthodes de recalage spatial à l'aide de scripts et de bibliothèques existantes; utilisation de VTK, ITK, Python, CMake et Conan.",
            "Contribution à l'intégration backend de l'inférence de modèles de segmentation développés par d'autres spécialistes; automatisation GitLab CI des inférences et de la collecte de données de validation.",
            "Développement antérieur de prototypes de réalité mixte avec Unity et HoloLens 2.",
        ]},
        {"company": "Prologue AI", "title": "Développeur logiciel / Unity senior", "dates": "juin 2022 - juil. 2023", "bullets": [
            "Livraison de CrimeTrip, un jeu d'aventure en réalité augmentée sous Unity, du prototype aux versions Android et iOS.",
            "Création et livraison d'interrogatoires vocaux de personnages intégrant reconnaissance vocale, réponses de l'API OpenAI et synthèse vocale ElevenLabs.",
            "Ajout de règles avant les requêtes, de contexte de personnage et de contrôles de sortie par mots-clés; validation manuelle des interactions par l'équipe.",
            "Création de services backend avec FastAPI, Azure Functions et PlayFab, intégrés à un client Unity modulaire et événementiel via HTTP et WebSocket.",
        ]},
        {"company": "BairesDev", "title": "Développeur logiciel, vision par ordinateur", "dates": "août 2020 - déc. 2021", "bullets": [
            "Création de pipelines Python de vision en production : annotation, augmentation, entraînement, réentraînement et inférence avec Detectron2, OpenCV et TensorFlow.",
            "Combinaison de détections 2D, de nuages de points 3D et de géométrie de caméra pour estimer les dimensions et la surface de fenêtres sur des façades.",
            "Contrôles de qualité des prises de vue, coordination de la collecte avec le client et des contributeurs externes, interfaces de capture/détection et passerelle Unity-React Native.",
        ]},
    ],
    "ptbr": [
        {"company": "Zimmer Biomet / Orthosoft", "title": "Desenvolvedor de Software Sênior", "dates": "ago 2023 - Atual", "bullets": [
            "Desenvolvimento de aplicações médicas C++17/Qt para cirurgia assistida por robôs, contribuindo para processamento e reconstrução de imagens médicas.",
            "Avaliação de métodos de registro espacial com scripts próprios e bibliotecas existentes; uso de VTK, ITK, Python, CMake e Conan.",
            "Contribuição à integração backend de inferência de modelos de segmentação desenvolvidos por outros especialistas; automação GitLab CI de inferências e coleta de dados de validação.",
            "Desenvolvimento anterior de protótipos de realidade mista com Unity e HoloLens 2.",
        ]},
        {"company": "Prologue AI", "title": "Desenvolvedor de Software / Unity Sênior", "dates": "jun 2022 - jul 2023", "bullets": [
            "Entrega de CrimeTrip, jogo de aventura em realidade aumentada em Unity, do protótipo ao lançamento para Android e iOS.",
            "Criação e lançamento de interrogatórios de personagens por voz, integrando reconhecimento de fala, respostas da API OpenAI e síntese de voz ElevenLabs.",
            "Implementação de regras antes das requisições, contexto de personagem e verificações de saída por palavras-chave; validação manual das interações pela equipe.",
            "Criação de serviços backend com FastAPI, Azure Functions e PlayFab, integrados a um cliente Unity modular e orientado a eventos via HTTP e WebSocket.",
        ]},
        {"company": "BairesDev", "title": "Desenvolvedor de Software, Visão Computacional", "dates": "ago 2020 - dez 2021", "bullets": [
            "Criação de fluxos Python de visão computacional em produção: anotação, aumento de dados, treinamento, retreinamento e inferência com Detectron2, OpenCV e TensorFlow.",
            "Combinação de detecções 2D, nuvens de pontos 3D e geometria de câmera para estimar dimensões e área de janelas em imagens de fachadas.",
            "Verificações de qualidade da captura, coordenação da coleta com o cliente e colaboradores externos, interfaces de captura/detecção e ponte Unity-React Native.",
        ]},
    ],
}

PROJECTS = {
    "VEKARRA": {"tech": "Unity / C#", "url": "https://store.steampowered.com/app/5009280/", "label": "Steam", "desc": {
        "en": "Solo tactical roguelite in development: seeded maps, active-time combat, skill drafting, saves and run-based permadeath. Upcoming on Steam.",
        "fr": "Roguelite tactique développé en solo : cartes générées à partir de graines, combat en temps actif, sélection de compétences, sauvegardes et mort permanente par partie. À venir sur Steam.",
        "ptbr": "Roguelite tático solo em desenvolvimento: mapas com sementes, combate em tempo ativo, seleção de habilidades, salvamento e morte permanente por partida. Futuro lançamento no Steam.",
    }},
    "AI-Pulse": {"tech": "TypeScript / Node.js / Electron", "url": "https://github.com/FernandoSLuz/ai-pulse", "label": "github.com/FernandoSLuz/ai-pulse", "desc": {
        "en": "Desktop application in development with local GGUF-model inference, a background service, REST/WebSocket APIs and SQLite.",
        "fr": "Application de bureau en développement avec inférence locale de modèles GGUF, service en arrière-plan, API REST/WebSocket et SQLite.",
        "ptbr": "Aplicação desktop em desenvolvimento com inferência local de modelos GGUF, serviço em segundo plano, APIs REST/WebSocket e SQLite.",
    }},
    "AgentFare": {"tech": "Python CLI / Alpha", "url": "https://github.com/FernandoSLuz/agentfare", "label": "github.com/FernandoSLuz/agentfare", "desc": {
        "en": "Alpha CLI for local analysis of coding-agent costs and rule-based model routing.",
        "fr": "CLI en version alpha pour l'analyse locale des coûts d'agents de programmation et le routage de modèles selon des règles.",
        "ptbr": "CLI em versão alfa para análise local de custos de agentes de programação e roteamento de modelos por regras.",
    }},
}

SKILLS = {
    "en": [
        ("Languages", "C++17, C#, Python, TypeScript"),
        ("Applications", "Qt 5/6, Unity, Electron; Android/iOS delivery, AR, HoloLens 2"),
        ("AI and vision", "Detectron2, OpenCV, TensorFlow, OpenAI API, ElevenLabs, VTK, ITK"),
        ("Services and data", "FastAPI, Azure Functions, PlayFab, REST, WebSocket, SQLite"),
        ("Engineering", "Git, GitLab CI, CMake, Conan; modular and event-driven software"),
    ],
    "fr": [
        ("Langages", "C++17, C#, Python, TypeScript"),
        ("Applications", "Qt 5/6, Unity, Electron; livraison Android/iOS, RA, HoloLens 2"),
        ("IA et vision", "Detectron2, OpenCV, TensorFlow, API OpenAI, ElevenLabs, VTK, ITK"),
        ("Services et données", "FastAPI, Azure Functions, PlayFab, REST, WebSocket, SQLite"),
        ("Développement", "Git, GitLab CI, CMake, Conan; logiciels modulaires et événementiels"),
    ],
    "ptbr": [
        ("Linguagens", "C++17, C#, Python, TypeScript"),
        ("Aplicações", "Qt 5/6, Unity, Electron; entrega Android/iOS, RA, HoloLens 2"),
        ("IA e visão", "Detectron2, OpenCV, TensorFlow, API OpenAI, ElevenLabs, VTK, ITK"),
        ("Serviços e dados", "FastAPI, Azure Functions, PlayFab, REST, WebSocket, SQLite"),
        ("Engenharia", "Git, GitLab CI, CMake, Conan; software modular e orientado a eventos"),
    ],
}

ADDITIONAL = {
    "en": ("Founder and Tech Lead | Down Below", "Sep 2021 - May 2022", "Independent JRPG project: gameplay systems, production scope, art direction and marketing as a solo founder.", "IT Director, RSTcom; Senior Unity Developer, Expansão; Developer, TeleIDEA."),
    "fr": ("Fondateur et responsable technique | Down Below", "sept. 2021 - mai 2022", "Projet indépendant de JRPG : systèmes de jeu, périmètre de production, direction artistique et marketing en tant que fondateur solo.", "Directeur TI, RSTcom; développeur Unity senior, Expansão; développeur, TeleIDEA."),
    "ptbr": ("Fundador e Líder Técnico | Down Below", "set 2021 - mai 2022", "Projeto independente de JRPG: sistemas de gameplay, escopo de produção, direção de arte e marketing como fundador solo.", "Diretor de TI, RSTcom; desenvolvedor Unity sênior, Expansão; desenvolvedor, TeleIDEA."),
}

EDUCATION = {
    "en": ["Bachelor's degree in Computer Science | FMU | Completed June 2024", "Game Design studies | Universidade Anhembi Morumbi | Degree not completed"],
    "fr": ["Baccalauréat en informatique | FMU | Obtenu en juin 2024", "Études en game design | Universidade Anhembi Morumbi | Diplôme non obtenu"],
    "ptbr": ["Bacharelado em Ciência da Computação | FMU | Concluído em junho de 2024", "Estudos em Game Design | Universidade Anhembi Morumbi | Graduação não concluída"],
}
LANGUAGES = {
    "en": "Portuguese: native | English: fluent | French: intermediate",
    "fr": "Portugais : langue maternelle | Anglais : courant | Français : intermédiaire",
    "ptbr": "Português: nativo | Inglês: fluente | Francês: intermediário",
}


def register_fonts():
    """Use embedded fonts for consistent Portuguese/French glyphs."""
    fonts = Path("/usr/share/fonts/truetype/dejavu")
    if (fonts / "DejaVuSans.ttf").exists():
        pdfmetrics.registerFont(TTFont("Resume", str(fonts / "DejaVuSans.ttf")))
        pdfmetrics.registerFont(TTFont("Resume-Bold", str(fonts / "DejaVuSans-Bold.ttf")))
        pdfmetrics.registerFontFamily("Resume", normal="Resume", bold="Resume-Bold", italic="Resume", boldItalic="Resume-Bold")
        return "Resume", "Resume-Bold"
    return "Helvetica", "Helvetica-Bold"


def make_styles(normal, bold):
    base = dict(fontName=normal, textColor=INK, fontSize=9.3, leading=12.5, spaceAfter=4)
    return {
        "body": ParagraphStyle("body", **base),
        "bullet": ParagraphStyle("bullet", **base, leftIndent=11, firstLineIndent=0, bulletIndent=0),
        "small": ParagraphStyle("small", fontName=normal, textColor=MUTED, fontSize=8.6, leading=11.8, spaceAfter=4),
        "name": ParagraphStyle("name", fontName=bold, fontSize=21, leading=25, alignment=TA_CENTER, textColor=INK, spaceAfter=4),
        "title": ParagraphStyle("title", fontName=normal, fontSize=10.5, leading=14, alignment=TA_CENTER, textColor=BLUE, spaceAfter=6),
        "contact": ParagraphStyle("contact", fontName=normal, fontSize=8.1, leading=11, alignment=TA_CENTER, textColor=MUTED, spaceAfter=8),
        "section": ParagraphStyle("section", fontName=bold, fontSize=10.3, leading=13, textColor=BLUE, spaceBefore=10, spaceAfter=6, keepWithNext=True),
        "job": ParagraphStyle("job", fontName=bold, fontSize=10, leading=13, textColor=INK, spaceAfter=2, keepWithNext=True),
        "company": ParagraphStyle("company", fontName=normal, fontSize=9, leading=12, textColor=BLUE, spaceAfter=5, keepWithNext=True),
        "continuation": ParagraphStyle("continuation", fontName=bold, fontSize=15, leading=19, textColor=INK, spaceAfter=3),
    }


def para(text, style):
    return Paragraph(escape(text), style)


def section(text, styles):
    return Paragraph(escape(text), styles["section"])


def build_story(role, lang, styles):
    labels = LABELS[lang]
    story = [para(NAME, styles["name"]), para(TITLES[role][lang], styles["title"])]
    contact = 'Montréal, QC, Canada | +1 438 778 1394 | <link href="mailto:fernandosilvadaluz@gmail.com" color="#2c5aa0">fernandosilvadaluz@gmail.com</link><br/><link href="https://www.linkedin.com/in/fernandosilvadaluz" color="#2c5aa0">linkedin.com/in/fernandosilvadaluz</link> | <link href="https://github.com/FernandoSLuz" color="#2c5aa0">github.com/FernandoSLuz</link> | <link href="https://fernandosluz.github.io" color="#2c5aa0">fernandosluz.github.io</link>'
    story += [Paragraph(contact, styles["contact"]), HRFlowable(width="100%", thickness=1.2, color=BLUE), section(labels["profile"], styles), para(PROFILES[role][lang], styles["body"]), section(labels["experience"], styles)]
    for item in EXPERIENCE[lang]:
        block = [para(item["company"], styles["job"]), para(f'{item["title"]} | {item["dates"]}', styles["company"])]
        block += [Paragraph(escape(b), styles["bullet"], bulletText="•") for b in item["bullets"]]
        story += [KeepTogether(block), Spacer(1, 5)]

    story += [PageBreak(), para(NAME, styles["continuation"]), para(labels["continued"], styles["small"]), HRFlowable(width="100%", thickness=0.8, color=BLUE), section(labels["projects"], styles)]
    order = ("AI-Pulse", "AgentFare", "VEKARRA") if role == "SoftwareDev" else ("VEKARRA", "AI-Pulse", "AgentFare")
    for name in order:
        project = PROJECTS[name]
        block = [para(f'{name} | {project["tech"]}', styles["job"]), para(project["desc"][lang], styles["body"]), Paragraph(f'<link href="{project["url"]}" color="#2c5aa0">{escape(project["label"])}</link>', styles["small"])]
        story += [KeepTogether(block), Spacer(1, 3)]

    story += [section(labels["skills"], styles)]
    order_skills = (0, 2, 3, 1, 4) if role == "SoftwareDev" else (1, 0, 3, 2, 4)
    for idx in order_skills:
        label, value = SKILLS[lang][idx]
        story.append(Paragraph(f'<b>{escape(label)}:</b> {escape(value)}', styles["body"]))

    title, dates, description, earlier = ADDITIONAL[lang]
    story += [section(labels["additional"], styles), para(f"{title} | {dates}", styles["job"]), para(description, styles["body"]), para(f'{labels["earlier"]}: {earlier}', styles["small"]), section(labels["education"], styles)]
    story += [para(line, styles["body"]) for line in EDUCATION[lang]]
    story += [section(labels["languages"], styles), para(LANGUAGES[lang], styles["body"]), para(labels["availability"], styles["small"]), para(labels["notice"], styles["small"])]
    return story


def generate_pdf(role, code, lang, styles, font):
    output = OUTPUT / f"Fernando_Silva_da_Luz_{role}_{code}.pdf"
    document = SimpleDocTemplate(str(output), pagesize=letter, rightMargin=42, leftMargin=42, topMargin=32, bottomMargin=35, title=f"{NAME} - {TITLES[role][lang]}", author=NAME, subject="Professional resume", pageCompression=1)

    def footer(canvas, doc):
        canvas.saveState()
        canvas.setStrokeColor(colors.HexColor("#dddddd"))
        canvas.setLineWidth(0.5)
        canvas.line(42, 28, letter[0] - 42, 28)
        canvas.setFont(font, 7.3)
        canvas.setFillColor(MUTED)
        canvas.drawString(42, 17, NAME)
        canvas.drawRightString(letter[0] - 42, 17, f"{doc.page}/2")
        canvas.restoreState()

    document.build(build_story(role, lang, styles), onFirstPage=footer, onLaterPages=footer)
    return output


def main():
    normal, bold = register_fonts()
    styles = make_styles(normal, bold)
    OUTPUT.mkdir(parents=True, exist_ok=True)
    for role in ROLES:
        for code, lang in LANGS.items():
            output = generate_pdf(role, code, lang, styles, normal)
            print(output.relative_to(ROOT))


if __name__ == "__main__":
    main()
