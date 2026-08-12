#!/usr/bin/env python3
"""
Generate all 9 résumé PDFs for Fernando Silva da Luz.
3 roles × 3 languages = 9 PDFs

Usage: python3 generate_resumes.py
Output: assets/resumes/Fernando_Silva_da_Luz_{role}_{lang}.pdf
"""

from weasyprint import HTML, CSS
import os

# Resume types and language codes
ROLES = ["GameDev", "UnityDev", "SoftwareDev"]
LANGS = {
    "EN": "en",
    "FR": "fr", 
    "PT-BR": "ptbr"
}

# Common contact info
CONTACT = {
    "name": "Fernando Silva da Luz",
    "location": {
        "en": "Montréal, QC, Canada",
        "fr": "Montréal, QC, Canada",
        "ptbr": "Montréal, QC, Canadá"
    },
    "phone": "+1 438 778 1394",
    "email": "fernandosilvadaluz@gmail.com",
    "linkedin": "linkedin.com/in/fernandosilvadaluz",
    "github": "github.com/FernandoSLuz",
    "website": "fernandosluz.github.io"
}

# Titles by role and language
TITLES = {
    "GameDev": {
        "en": "Game Developer · Gameplay Engineer",
        "fr": "Développeur de jeux · Programmeur gameplay",
        "ptbr": "Desenvolvedor de Jogos · Programador de Gameplay"
    },
    "UnityDev": {
        "en": "Unity Developer · C# Engineer",
        "fr": "Développeur Unity · Ingénieur C#",
        "ptbr": "Desenvolvedor Unity · Engenheiro C#"
    },
    "SoftwareDev": {
        "en": "Software Developer · Full-Stack & Gameplay",
        "fr": "Développeur logiciel · Full-stack et gameplay",
        "ptbr": "Desenvolvedor de Software · Full-Stack e Gameplay"
    }
}

# Section headers
HEADERS = {
    "profile": {"en": "PROFILE", "fr": "PROFIL", "ptbr": "PERFIL"},
    "skills": {"en": "CORE SKILLS", "fr": "COMPÉTENCES CLÉS", "ptbr": "PRINCIPAIS COMPETÊNCIAS"},
    "experience": {"en": "EXPERIENCE", "fr": "EXPÉRIENCE", "ptbr": "EXPERIÊNCIA"},
    "projects": {"en": "SELECTED GAMES & PROJECTS", "fr": "JEUX ET PROJETS SÉLECTIONNÉS", "ptbr": "JOGOS E PROJETOS SELECIONADOS"},
    "hackathons": {"en": "HACKATHONS", "fr": "HACKATHONS", "ptbr": "HACKATHONS"},
    "education": {"en": "EDUCATION", "fr": "FORMATION", "ptbr": "FORMAÇÃO"},
    "certifications": {"en": "CERTIFICATIONS", "fr": "CERTIFICATIONS", "ptbr": "CERTIFICAÇÕES"},
    "languages": {"en": "LANGUAGES", "fr": "LANGUES", "ptbr": "IDIOMAS"}
}

# Profile text by role
PROFILES = {
    "GameDev": {
        "en": "Game developer with 13+ years shipping games and interactive experiences across mobile, PC and XR. Unity & C# specialist, now also building in Godot, with a Game Design degree and a Computer Science degree. One of the world's first Unity Certified Developers and a 7× hackathon winner. I love turning concepts into shipped games — gameplay systems, tools, and the polish that makes them feel great.",
        "fr": "Développeur de jeux avec plus de 13 ans d'expérience à livrer des jeux et des expériences interactives sur mobile, PC et RX. Spécialiste Unity et C#, je développe désormais aussi sous Godot ; titulaire d'un diplôme en game design et d'un diplôme en informatique. L'un des premiers développeurs certifiés Unity au monde et lauréat de 7 hackathons. J'aime transformer des concepts en jeux livrés — systèmes de gameplay, outils et la finition qui fait toute la différence.",
        "ptbr": "Desenvolvedor de jogos com mais de 13 anos entregando jogos e experiências interativas em mobile, PC e RX. Especialista em Unity e C#, hoje também desenvolvendo em Godot, com formação em Game Design e em Ciência da Computação. Um dos primeiros desenvolvedores certificados Unity do mundo e vencedor de 7 hackathons. Gosto de transformar conceitos em jogos entregues — sistemas de gameplay, ferramentas e o polimento que faz tudo funcionar bem."
    },
    "UnityDev": {
        "en": "Senior Unity developer with 10+ years in Unity and C#, and one of the first Unity Certified Developers worldwide. I build games, tools and real-time 3D / XR applications — from gameplay systems and shaders to modular architectures and cloud backends. Game Design and Computer Science degrees, 7× hackathon winner, now focused on game development.",
        "fr": "Développeur Unity senior avec plus de 10 ans en Unity et C#, et l'un des premiers développeurs certifiés Unity au monde. Je crée des jeux, des outils et des applications 3D temps réel / RX — des systèmes de gameplay et shaders aux architectures modulaires et backends cloud. Diplômé en game design et informatique, lauréat de 7 hackathons, actuellement axé sur le développement de jeux.",
        "ptbr": "Desenvolvedor Unity sênior com mais de 10 anos em Unity e C#, e um dos primeiros desenvolvedores certificados Unity do mundo. Crio jogos, ferramentas e aplicações 3D em tempo real / RX — de sistemas de gameplay e shaders a arquiteturas modulares e backends na nuvem. Formado em Game Design e Ciência da Computação, vencedor de 7 hackathons, atualmente focado em desenvolvimento de jogos."
    },
    "SoftwareDev": {
        "en": "Software engineer with 13+ years across full-stack, backend, computer vision and game development. I ship production systems in C#, Python and TypeScript — serverless backends (FastAPI / Azure), real-time computer-vision pipelines (Detectron2 / OpenCV / TensorFlow) and interactive 3D applications. B.Sc. Computer Science, 7× hackathon winner, and a Unity specialist who enjoys building games as much as the systems behind them.",
        "fr": "Ingénieur logiciel avec plus de 13 ans d'expérience en full-stack, backend, vision par ordinateur et développement de jeux. Je livre des systèmes en production en C#, Python et TypeScript — backends serverless (FastAPI / Azure), pipelines de vision par ordinateur en temps réel (Detectron2 / OpenCV / TensorFlow) et applications 3D interactives. Baccalauréat en informatique, lauréat de 7 hackathons, et spécialiste Unity qui aime autant créer des jeux que les systèmes qui les font fonctionner.",
        "ptbr": "Engenheiro de software com mais de 13 anos em full-stack, backend, visão computacional e desenvolvimento de jogos. Entrego sistemas em produção em C#, Python e TypeScript — backends serverless (FastAPI / Azure), pipelines de visão computacional em tempo real (Detectron2 / OpenCV / TensorFlow) e aplicações 3D interativas. Bacharel em Ciência da Computação, vencedor de 7 hackathons, e especialista Unity que gosta tanto de criar jogos quanto dos sistemas por trás deles."
    }
}

# Skills by role
SKILLS = {
    "GameDev": {
        "en": """<b>Engines & Languages:</b> Unity3D, C#, C++, Godot, GDScript, Python, TypeScript<br>
<b>Gameplay:</b> Game design, turn-based / JRPG systems, multiplayer, tools, event-driven & ScriptableObject architecture, shaders & post-processing, profiling & optimization<br>
<b>XR:</b> AR / VR / MR — HoloLens 2, Meta Quest, HTC Vive<br>
<b>Backend & Live Ops:</b> FastAPI, Azure Functions, PlayFab, REST, SocketIO, MySQL, MongoDB<br>
<b>Practice:</b> Game jams (Global Game Jam, SPJam), Git, Agile, CI/CD""",
        "fr": """<b>Moteurs et langages:</b> Unity3D, C#, C++, Godot, GDScript, Python, TypeScript<br>
<b>Gameplay:</b> Game design, systèmes tour par tour / JRPG, multijoueur, outils, architecture événementielle et ScriptableObject, shaders et post-traitement, profilage et optimisation<br>
<b>RX:</b> RA / RV / RM — HoloLens 2, Meta Quest, HTC Vive<br>
<b>Backend et Live Ops:</b> FastAPI, Azure Functions, PlayFab, REST, SocketIO, MySQL, MongoDB<br>
<b>Pratique:</b> Game jams (Global Game Jam, SPJam), Git, Agile, CI/CD""",
        "ptbr": """<b>Engines e Linguagens:</b> Unity3D, C#, C++, Godot, GDScript, Python, TypeScript<br>
<b>Gameplay:</b> Game design, sistemas por turnos / JRPG, multiplayer, ferramentas, arquitetura orientada a eventos e ScriptableObject, shaders e pós-processamento, profiling e otimização<br>
<b>RX:</b> RA / RV / RM — HoloLens 2, Meta Quest, HTC Vive<br>
<b>Backend e Live Ops:</b> FastAPI, Azure Functions, PlayFab, REST, SocketIO, MySQL, MongoDB<br>
<b>Prática:</b> Game jams (Global Game Jam, SPJam), Git, Agile, CI/CD"""
    },
    "UnityDev": {
        "en": """<b>Unity:</b> Gameplay & tools programming, URP / shaders & post-processing, ScriptableObjects, Addressables, profiling & optimization, multiplayer / netcode, AR Foundation, XR Interaction Toolkit<br>
<b>Languages:</b> C#, C++, Python, TypeScript, GDScript<br>
<b>XR & Platforms:</b> HoloLens 2, Meta Quest, HTC Vive · Android, iOS, PC<br>
<b>Backend:</b> FastAPI, Azure Functions, PlayFab, REST, SocketIO<br>
<b>Tools:</b> Git, CMake, Conan, Docker, Azure DevOps, Agile""",
        "fr": """<b>Unity:</b> Programmation gameplay et outils, URP / shaders et post-traitement, ScriptableObjects, Addressables, profilage et optimisation, multijoueur / netcode, AR Foundation, XR Interaction Toolkit<br>
<b>Langages:</b> C#, C++, Python, TypeScript, GDScript<br>
<b>RX et plateformes:</b> HoloLens 2, Meta Quest, HTC Vive · Android, iOS, PC<br>
<b>Backend:</b> FastAPI, Azure Functions, PlayFab, REST, SocketIO<br>
<b>Outils:</b> Git, CMake, Conan, Docker, Azure DevOps, Agile""",
        "ptbr": """<b>Unity:</b> Programação de gameplay e ferramentas, URP / shaders e pós-processamento, ScriptableObjects, Addressables, profiling e otimização, multiplayer / netcode, AR Foundation, XR Interaction Toolkit<br>
<b>Linguagens:</b> C#, C++, Python, TypeScript, GDScript<br>
<b>RX e Plataformas:</b> HoloLens 2, Meta Quest, HTC Vive · Android, iOS, PC<br>
<b>Backend:</b> FastAPI, Azure Functions, PlayFab, REST, SocketIO<br>
<b>Ferramentas:</b> Git, CMake, Conan, Docker, Azure DevOps, Agile"""
    },
    "SoftwareDev": {
        "en": """<b>Languages:</b> C#, C++, Python, TypeScript, JavaScript, GDScript, PHP, SQL<br>
<b>Backend & Cloud:</b> FastAPI, Flask, Azure Functions, PlayFab, REST, SocketIO, Docker, Kubernetes, Azure, GCP, AWS<br>
<b>Data & Computer Vision:</b> OpenCV, Detectron2, TensorFlow, MySQL, MongoDB<br>
<b>Game, 3D & Systems:</b> Unity3D, C#, Godot, real-time 3D, AR / VR / MR, C++ / Qt desktop apps, CMake, Conan<br>
<b>Practice:</b> Git, CI/CD, Agile · 7× hackathon winner""",
        "fr": """<b>Langages:</b> C#, C++, Python, TypeScript, JavaScript, GDScript, PHP, SQL<br>
<b>Backend et cloud:</b> FastAPI, Flask, Azure Functions, PlayFab, REST, SocketIO, Docker, Kubernetes, Azure, GCP, AWS<br>
<b>Données et vision par ordinateur:</b> OpenCV, Detectron2, TensorFlow, MySQL, MongoDB<br>
<b>Jeux, 3D et systèmes:</b> Unity3D, C#, Godot, 3D temps réel, RA / RV / RM, apps desktop C++ / Qt, CMake, Conan<br>
<b>Pratique:</b> Git, CI/CD, Agile · Lauréat de 7 hackathons""",
        "ptbr": """<b>Linguagens:</b> C#, C++, Python, TypeScript, JavaScript, GDScript, PHP, SQL<br>
<b>Backend e Cloud:</b> FastAPI, Flask, Azure Functions, PlayFab, REST, SocketIO, Docker, Kubernetes, Azure, GCP, AWS<br>
<b>Dados e Visão Computacional:</b> OpenCV, Detectron2, TensorFlow, MySQL, MongoDB<br>
<b>Jogos, 3D e Sistemas:</b> Unity3D, C#, Godot, 3D em tempo real, RA / RV / RM, apps desktop C++ / Qt, CMake, Conan<br>
<b>Prática:</b> Git, CI/CD, Agile · Vencedor de 7 hackathons"""
    }
}

# Experience entries (different per role type)
EXPERIENCE = {
    "GameDev": {
        "en": [
            {"title": "Senior Unity Developer", "company": "Prologue AI", "location": "Montréal, QC", "dates": "Jun 2022 – Jul 2023",
             "bullets": [
                 "Shipped CrimeTrip, an AR true-crime adventure game, from prototype to store release on Android and iOS (Unity, C#).",
                 "Built a modular, event-driven gameplay architecture and an extensible real-time co-creation system reused across projects.",
                 "Owned graphics work — custom shaders and post-processing — and performance optimization for mobile AR.",
                 "Mentored an intern and ran internal tech talks and training for the studio and partner teams."
             ]},
            {"title": "Founder & Tech Lead", "company": "Down Below — Indie Game Studio", "location": "Remote", "dates": "Sep 2021 – May 2022",
             "bullets": [
                 "Led design and production of Down Below, a turn-based JRPG inspired by Darkest Dungeon (Unity3D, C#).",
                 "Built core gameplay systems: party builder, turn-based combat, encounters and loot.",
                 "Drove the project across disciplines — design, art direction, marketing and development."
             ]},
            {"title": "Freelance Game & Interactive Developer", "company": "Freelance", "location": "Montréal / Remote", "dates": "Nov 2019 – Present",
             "bullets": [
                 "Design and ship games and interactive experiences for studios and brands on contract.",
                 "Recent: Viva La Execution!, a comedic narrative game with dynamic AI dialogue (Unity, FastAPI, OpenAI, ElevenLabs)."
             ]},
            {"title": "Senior Software Developer", "company": "Zimmer Biomet", "location": "Montréal, QC", "dates": "Aug 2023 – Present",
             "bullets": [
                 "Build applications for robotic-assisted surgery — knee, hip, shoulder and brain — in C++, Qt (5/6), Python, CMake and Conan.",
                 "Deliver performance-critical, regulated-quality software; started on the HoloLens 2 / Unity mixed-reality team, then moved into surgical robotics."
             ]},
            {"title": "Senior Unity Developer", "company": "Expansão Consultoria", "location": "São Paulo, BR", "dates": "Feb 2016 – Apr 2017",
             "bullets": [
                 "Built interactive and gamified experiences in Unity3D for live events and corporate training."
             ]},
        ],
        "fr": [
            {"title": "Développeur Unity senior", "company": "Prologue AI", "location": "Montréal, QC", "dates": "juin 2022 – juil. 2023",
             "bullets": [
                 "Livraison de CrimeTrip, un jeu d'aventure policière en RA, du prototype à la mise en marché sur Android et iOS (Unity, C#).",
                 "Conception d'une architecture de gameplay modulaire et événementielle, ainsi que d'un système de co-création en temps réel réutilisé sur plusieurs projets.",
                 "Responsable du volet graphique — shaders personnalisés et post-traitement — et de l'optimisation des performances pour la RA mobile.",
                 "Encadrement d'un stagiaire et animation de conférences techniques et de formations pour le studio et les partenaires."
             ]},
            {"title": "Fondateur et responsable technique", "company": "Down Below — Studio de jeux indépendant", "location": "À distance", "dates": "sept. 2021 – mai 2022",
             "bullets": [
                 "Direction de la conception et de la production de Down Below, un JRPG au tour par tour inspiré de Darkest Dungeon (Unity3D, C#).",
                 "Développement des systèmes de gameplay : création d'équipe, combat au tour par tour, rencontres et butin.",
                 "Pilotage du projet dans tous les domaines — design, direction artistique, marketing et développement."
             ]},
            {"title": "Développeur de jeux et d'expériences interactives (freelance)", "company": "Freelance", "location": "Montréal / À distance", "dates": "nov. 2019 – Présent",
             "bullets": [
                 "Conception et livraison de jeux et d'expériences interactives pour des studios et des marques en contrat.",
                 "Récemment : Viva La Execution!, un jeu narratif humoristique aux dialogues IA dynamiques (Unity, FastAPI, OpenAI, ElevenLabs)."
             ]},
            {"title": "Développeur logiciel senior", "company": "Zimmer Biomet", "location": "Montréal, QC", "dates": "août 2023 – Présent",
             "bullets": [
                 "Je développe des applications pour la chirurgie assistée par robot — genou, hanche, épaule et cerveau — en C++, Qt (5/6), Python, CMake et Conan.",
                 "Livraison de logiciels critiques en performance et de qualité réglementée ; d'abord dans l'équipe réalité mixte HoloLens 2 / Unity, puis en robotique chirurgicale."
             ]},
            {"title": "Développeur Unity senior", "company": "Expansão Consultoria", "location": "São Paulo, Brésil", "dates": "févr. 2016 – avr. 2017",
             "bullets": [
                 "Création d'expériences interactives et ludifiées sous Unity3D pour des événements et de la formation en entreprise."
             ]},
        ],
        "ptbr": [
            {"title": "Desenvolvedor Unity Sênior", "company": "Prologue AI", "location": "Montréal, QC", "dates": "jun 2022 – jul 2023",
             "bullets": [
                 "Entrega do CrimeTrip, um jogo de aventura de true crime em RA, do protótipo ao lançamento nas lojas Android e iOS (Unity, C#).",
                 "Construção de uma arquitetura de gameplay modular e orientada a eventos e de um sistema de cocriação em tempo real reutilizado em vários projetos.",
                 "Responsável pela parte gráfica — shaders personalizados e pós-processamento — e pela otimização de desempenho para RA mobile.",
                 "Mentoria de um estagiário e condução de palestras técnicas e treinamentos para o estúdio e parceiros."
             ]},
            {"title": "Fundador e Líder Técnico", "company": "Down Below — Estúdio de jogos independente", "location": "Remoto", "dates": "set 2021 – mai 2022",
             "bullets": [
                 "Direção da concepção e produção de Down Below, um JRPG por turnos inspirado em Darkest Dungeon (Unity3D, C#).",
                 "Desenvolvimento dos sistemas de gameplay: montagem de grupo, combate por turnos, encontros e recompensas.",
                 "Condução do projeto em todas as áreas — design, direção de arte, marketing e desenvolvimento."
             ]},
            {"title": "Desenvolvedor de Jogos e Experiências Interativas (freelance)", "company": "Freelance", "location": "Montréal / Remoto", "dates": "nov 2019 – Atual",
             "bullets": [
                 "Concepção e entrega de jogos e experiências interativas para estúdios e marcas sob contrato.",
                 "Recente: Viva La Execution!, um jogo narrativo de humor com diálogos dinâmicos por IA (Unity, FastAPI, OpenAI, ElevenLabs)."
             ]},
            {"title": "Desenvolvedor de Software Sênior", "company": "Zimmer Biomet", "location": "Montréal, QC", "dates": "ago 2023 – Atual",
             "bullets": [
                 "Desenvolvo aplicações para cirurgia assistida por robôs — joelho, quadril, ombro e cérebro — em C++, Qt (5/6), Python, CMake e Conan.",
                 "Entrega de software crítico em desempenho e de qualidade regulamentada; comecei no time de realidade mista HoloLens 2 / Unity e depois fui para robótica cirúrgica."
             ]},
            {"title": "Desenvolvedor Unity Sênior", "company": "Expansão Consultoria", "location": "São Paulo, BR", "dates": "fev 2016 – abr 2017",
             "bullets": [
                 "Criação de experiências interativas e gamificadas em Unity3D para eventos e treinamento corporativo."
             ]},
        ]
    },
    "UnityDev": {
        "en": [
            {"title": "Senior Unity Developer", "company": "Prologue AI", "location": "Montréal, QC", "dates": "Jun 2022 – Jul 2023",
             "bullets": [
                 "Delivered CrimeTrip, an AR game, in Unity / C# — gameplay, AR foundation and PlayFab-backed live content.",
                 "Architected modular event-driven systems and an extensible real-time collaboration framework.",
                 "Authored custom shaders and post-processing; profiled and optimized to mobile GPU/CPU budgets.",
                 "Mentored an intern and led Unity best-practice training sessions."
             ]},
            {"title": "Senior Software Developer", "company": "Zimmer Biomet", "location": "Montréal, QC", "dates": "Aug 2023 – Present",
             "bullets": [
                 "Build applications for robotic-assisted surgery — knee, hip, shoulder and brain — in C++, Qt (5/6), Python, CMake and Conan.",
                 "Deliver performance-critical, regulated-quality software; started on the HoloLens 2 / Unity mixed-reality team, then moved into surgical robotics."
             ]},
            {"title": "Founder & Tech Lead", "company": "Down Below — Indie Game Studio", "location": "Remote", "dates": "Sep 2021 – May 2022",
             "bullets": [
                 "Led Unity3D development of a turn-based JRPG — combat, party and progression systems."
             ]},
            {"title": "Freelance Unity Developer", "company": "Freelance", "location": "Montréal / Remote", "dates": "Nov 2019 – Present",
             "bullets": [
                 "Build Unity games, tools and AR/VR/MR apps for clients on Meta Quest, HoloLens and HTC Vive."
             ]},
            {"title": "Senior Unity Developer", "company": "Expansão Consultoria", "location": "São Paulo, BR", "dates": "Feb 2016 – Apr 2017",
             "bullets": [
                 "Built VR/AR/MR and gamified Unity experiences for live events and corporate training."
             ]},
        ],
        "fr": [
            {"title": "Développeur Unity senior", "company": "Prologue AI", "location": "Montréal, QC", "dates": "juin 2022 – juil. 2023",
             "bullets": [
                 "Livraison de CrimeTrip, un jeu RA, en Unity / C# — gameplay, AR Foundation et contenu live via PlayFab.",
                 "Conception d'une architecture modulaire événementielle et d'un framework de collaboration temps réel extensible.",
                 "Création de shaders personnalisés et post-traitement ; profilage et optimisation pour les budgets GPU/CPU mobiles.",
                 "Encadrement d'un stagiaire et animation de formations sur les bonnes pratiques Unity."
             ]},
            {"title": "Développeur logiciel senior", "company": "Zimmer Biomet", "location": "Montréal, QC", "dates": "août 2023 – Présent",
             "bullets": [
                 "Je développe des applications pour la chirurgie assistée par robot — genou, hanche, épaule et cerveau — en C++, Qt (5/6), Python, CMake et Conan.",
                 "Livraison de logiciels critiques en performance et de qualité réglementée ; d'abord dans l'équipe réalité mixte HoloLens 2 / Unity, puis en robotique chirurgicale."
             ]},
            {"title": "Fondateur et responsable technique", "company": "Down Below — Studio de jeux indépendant", "location": "À distance", "dates": "sept. 2021 – mai 2022",
             "bullets": [
                 "Direction du développement Unity3D d'un JRPG au tour par tour — combat, équipe et progression."
             ]},
            {"title": "Développeur Unity (freelance)", "company": "Freelance", "location": "Montréal / À distance", "dates": "nov. 2019 – Présent",
             "bullets": [
                 "Création de jeux, outils et applications RA/RV/RM Unity pour des clients sur Meta Quest, HoloLens et HTC Vive."
             ]},
            {"title": "Développeur Unity senior", "company": "Expansão Consultoria", "location": "São Paulo, Brésil", "dates": "févr. 2016 – avr. 2017",
             "bullets": [
                 "Création d'expériences RV/RA/RM et ludifiées sous Unity pour des événements et de la formation en entreprise."
             ]},
        ],
        "ptbr": [
            {"title": "Desenvolvedor Unity Sênior", "company": "Prologue AI", "location": "Montréal, QC", "dates": "jun 2022 – jul 2023",
             "bullets": [
                 "Entrega do CrimeTrip, um jogo RA, em Unity / C# — gameplay, AR Foundation e conteúdo live via PlayFab.",
                 "Arquitetura de sistemas modulares orientados a eventos e framework de colaboração em tempo real extensível.",
                 "Criação de shaders personalizados e pós-processamento; profiling e otimização para orçamentos de GPU/CPU mobile.",
                 "Mentoria de um estagiário e condução de treinamentos sobre boas práticas Unity."
             ]},
            {"title": "Desenvolvedor de Software Sênior", "company": "Zimmer Biomet", "location": "Montréal, QC", "dates": "ago 2023 – Atual",
             "bullets": [
                 "Desenvolvo aplicações para cirurgia assistida por robôs — joelho, quadril, ombro e cérebro — em C++, Qt (5/6), Python, CMake e Conan.",
                 "Entrega de software crítico em desempenho e de qualidade regulamentada; comecei no time de realidade mista HoloLens 2 / Unity e depois fui para robótica cirúrgica."
             ]},
            {"title": "Fundador e Líder Técnico", "company": "Down Below — Estúdio de jogos independente", "location": "Remoto", "dates": "set 2021 – mai 2022",
             "bullets": [
                 "Liderança do desenvolvimento Unity3D de um JRPG por turnos — combate, grupo e progressão."
             ]},
            {"title": "Desenvolvedor Unity (freelance)", "company": "Freelance", "location": "Montréal / Remoto", "dates": "nov 2019 – Atual",
             "bullets": [
                 "Criação de jogos, ferramentas e apps RA/RV/RM Unity para clientes em Meta Quest, HoloLens e HTC Vive."
             ]},
            {"title": "Desenvolvedor Unity Sênior", "company": "Expansão Consultoria", "location": "São Paulo, BR", "dates": "fev 2016 – abr 2017",
             "bullets": [
                 "Criação de experiências RV/RA/RM e gamificadas em Unity para eventos e treinamento corporativo."
             ]},
        ]
    },
    "SoftwareDev": {
        "en": [
            {"title": "Senior Software Developer", "company": "Zimmer Biomet", "location": "Montréal, QC", "dates": "Aug 2023 – Present",
             "bullets": [
                 "Build applications for robotic-assisted surgery — knee, hip, shoulder and brain — in C++, Qt (5/6), Python, CMake and Conan.",
                 "Deliver performance-critical, regulated-quality software across the product lifecycle; started on the HoloLens 2 / Unity mixed-reality team, then moved into surgical robotics."
             ]},
            {"title": "Senior Software / Unity Developer", "company": "Prologue AI", "location": "Montréal, QC", "dates": "Jun 2022 – Jul 2023",
             "bullets": [
                 "Built the serverless backend for CrimeTrip — FastAPI, Azure Functions and PlayFab for players and content.",
                 "Designed modular, event-driven client architecture and real-time collaboration services.",
                 "Optimized performance and cloud costs across the stack."
             ]},
            {"title": "Software Engineer — Computer Vision", "company": "BairesDev", "location": "Remote", "dates": "Aug 2020 – Dec 2021",
             "bullets": [
                 "Built deep-learning pipelines for real-time detection, measurement and classification of physical objects for the real-estate market.",
                 "Stack: Python, Detectron2, OpenCV, TensorFlow."
             ]},
            {"title": "IT Director / Developer", "company": "RSTcom Comunicação Estratégica", "location": "São Paulo, BR", "dates": "Mar 2018 – Nov 2019",
             "bullets": [
                 "Led a development team; owned budgets, schedules and delivery for the events market.",
                 "Shipped 12+ mobile apps to the App Store and Google Play."
             ]},
            {"title": "Freelance Software Developer", "company": "Freelance", "location": "Montréal / Remote", "dates": "Nov 2019 – Present",
             "bullets": [
                 "Deliver full-stack and backend systems, APIs and interactive apps (Python, C#, TypeScript)."
             ]},
        ],
        "fr": [
            {"title": "Développeur logiciel senior", "company": "Zimmer Biomet", "location": "Montréal, QC", "dates": "août 2023 – Présent",
             "bullets": [
                 "Je développe des applications pour la chirurgie assistée par robot — genou, hanche, épaule et cerveau — en C++, Qt (5/6), Python, CMake et Conan.",
                 "Livraison de logiciels critiques en performance et de qualité réglementée sur tout le cycle de vie du produit ; d'abord dans l'équipe réalité mixte HoloLens 2 / Unity, puis en robotique chirurgicale."
             ]},
            {"title": "Développeur logiciel / Unity senior", "company": "Prologue AI", "location": "Montréal, QC", "dates": "juin 2022 – juil. 2023",
             "bullets": [
                 "Création du backend serverless de CrimeTrip — FastAPI, Azure Functions et PlayFab pour les joueurs et le contenu.",
                 "Conception d'une architecture client modulaire et événementielle et de services de collaboration temps réel.",
                 "Optimisation des performances et des coûts cloud sur toute la stack."
             ]},
            {"title": "Ingénieur logiciel — Vision par ordinateur", "company": "BairesDev", "location": "À distance", "dates": "août 2020 – déc. 2021",
             "bullets": [
                 "Création de pipelines de deep learning pour la détection, mesure et classification en temps réel d'objets physiques pour le marché immobilier.",
                 "Stack : Python, Detectron2, OpenCV, TensorFlow."
             ]},
            {"title": "Directeur TI / Développeur", "company": "RSTcom Comunicação Estratégica", "location": "São Paulo, Brésil", "dates": "mars 2018 – nov. 2019",
             "bullets": [
                 "Direction d'une équipe de développement ; responsable des budgets, des calendriers et des livraisons pour le marché événementiel.",
                 "Livraison de plus de 12 applis mobiles sur l'App Store et Google Play."
             ]},
            {"title": "Développeur logiciel (freelance)", "company": "Freelance", "location": "Montréal / À distance", "dates": "nov. 2019 – Présent",
             "bullets": [
                 "Livraison de systèmes full-stack et backend, APIs et applications interactives (Python, C#, TypeScript)."
             ]},
        ],
        "ptbr": [
            {"title": "Desenvolvedor de Software Sênior", "company": "Zimmer Biomet", "location": "Montréal, QC", "dates": "ago 2023 – Atual",
             "bullets": [
                 "Desenvolvo aplicações para cirurgia assistida por robôs — joelho, quadril, ombro e cérebro — em C++, Qt (5/6), Python, CMake e Conan.",
                 "Entrega de software crítico em desempenho e de qualidade regulamentada em todo o ciclo de vida do produto; comecei no time de realidade mista HoloLens 2 / Unity e depois fui para robótica cirúrgica."
             ]},
            {"title": "Desenvolvedor de Software / Unity Sênior", "company": "Prologue AI", "location": "Montréal, QC", "dates": "jun 2022 – jul 2023",
             "bullets": [
                 "Criação do backend serverless do CrimeTrip — FastAPI, Azure Functions e PlayFab para jogadores e conteúdo.",
                 "Projeto de arquitetura cliente modular e orientada a eventos e serviços de colaboração em tempo real.",
                 "Otimização de desempenho e custos de cloud em toda a stack."
             ]},
            {"title": "Engenheiro de Software — Visão Computacional", "company": "BairesDev", "location": "Remoto", "dates": "ago 2020 – dez 2021",
             "bullets": [
                 "Criação de pipelines de deep learning para detecção, medição e classificação em tempo real de objetos físicos para o mercado imobiliário.",
                 "Stack: Python, Detectron2, OpenCV, TensorFlow."
             ]},
            {"title": "Diretor de TI / Desenvolvedor", "company": "RSTcom Comunicação Estratégica", "location": "São Paulo, BR", "dates": "mar 2018 – nov 2019",
             "bullets": [
                 "Liderança de equipe de desenvolvimento; responsável por orçamentos, cronogramas e entregas para o mercado de eventos.",
                 "Entrega de mais de 12 apps mobile na App Store e Google Play."
             ]},
            {"title": "Desenvolvedor de Software (freelance)", "company": "Freelance", "location": "Montréal / Remoto", "dates": "nov 2019 – Atual",
             "bullets": [
                 "Entrega de sistemas full-stack e backend, APIs e apps interativos (Python, C#, TypeScript)."
             ]},
        ]
    }
}

# Earlier experience text (different per role)
EARLIER_EXP = {
    "GameDev": {
        "en": "Earlier experience: Computer-vision engineer @ BairesDev · IT Director @ RSTcom (12+ shipped apps) · Founder @ Virtual Light (VR startup) · Developer @ TeleIDEA · Bilingual tech support @ Hewlett-Packard.",
        "fr": "Expérience antérieure: Ingénieur vision par ordinateur @ BairesDev · Directeur TI @ RSTcom (plus de 12 applis livrées) · Fondateur @ Virtual Light (startup RV) · Développeur @ TeleIDEA · Support technique bilingue @ Hewlett-Packard.",
        "ptbr": "Experiência anterior: Engenheiro de visão computacional @ BairesDev · Diretor de TI @ RSTcom (mais de 12 apps entregues) · Fundador @ Virtual Light (startup de RV) · Desenvolvedor @ TeleIDEA · Suporte técnico bilíngue @ Hewlett-Packard."
    },
    "UnityDev": {
        "en": "Earlier experience: Founder @ Virtual Light (Unity VR for real estate) · IT Director @ RSTcom · Computer vision @ BairesDev · Developer @ TeleIDEA · Bilingual tech support @ Hewlett-Packard.",
        "fr": "Expérience antérieure: Fondateur @ Virtual Light (Unity RV pour l'immobilier) · Directeur TI @ RSTcom · Vision par ordinateur @ BairesDev · Développeur @ TeleIDEA · Support technique bilingue @ Hewlett-Packard.",
        "ptbr": "Experiência anterior: Fundador @ Virtual Light (Unity RV para imobiliário) · Diretor de TI @ RSTcom · Visão computacional @ BairesDev · Desenvolvedor @ TeleIDEA · Suporte técnico bilíngue @ Hewlett-Packard."
    },
    "SoftwareDev": {
        "en": "Earlier experience: Founder @ Virtual Light · Senior Unity developer @ Expansão · Developer / test analyst @ TeleIDEA · Bilingual technical support @ Hewlett-Packard (19 enterprise clients).",
        "fr": "Expérience antérieure: Fondateur @ Virtual Light · Développeur Unity senior @ Expansão · Développeur / analyste de tests @ TeleIDEA · Support technique bilingue @ Hewlett-Packard (19 clients entreprise).",
        "ptbr": "Experiência anterior: Fundador @ Virtual Light · Desenvolvedor Unity sênior @ Expansão · Desenvolvedor / analista de testes @ TeleIDEA · Suporte técnico bilíngue @ Hewlett-Packard (19 clientes corporativos)."
    }
}

# Projects - NOW INCLUDING VEKARRA
PROJECTS = {
    "en": [
        {"name": "VEKARRA", "tech": "Unity · Roguelite · Local Co-op",
         "desc": "Group expedition roguelite: four heroes, procedural maps, active-time combat. Playable demo on itch.io.",
         "link": "fernandoluz.itch.io/vekarra"},
        {"name": "CrimeTrip", "tech": "Unity · AR · FastAPI · Azure · PlayFab",
         "desc": "AR true-crime adventure game — investigate six cold cases inside augmented-reality crime scenes.",
         "link": "prologuexr.com/crimetrip"},
        {"name": "Viva La Execution!", "tech": "Unity · FastAPI · OpenAI · ElevenLabs",
         "desc": "Comedic narrative game set in the French Revolution, with dynamic AI-driven dialogue.",
         "link": "danyboyyy.itch.io/viva-la-execution"},
        {"name": "Down Below", "tech": "Unity3D · C# · Turn-based combat",
         "desc": "Turn-based JRPG inspired by Darkest Dungeon — party builder, combat and loot systems.",
         "link": "vimeo.com/697498158"},
        {"name": "Janos", "tech": "Unity · Oculus Rift · Game Jam",
         "desc": "VR puzzle game built comfort-first to prevent motion sickness — a two-headed robot escape room. Made at SPJam.",
         "link": "youtube.com/watch?v=eFgFCMwm-5U"},
        {"name": "Missão Fundo do Mar", "tech": "Unity · Computer Vision · Video-mapping",
         "desc": "Interactive projection wall using AI image recognition to bring children's drawings to life (Monica's Park).",
         "link": "vimeo.com/359048835"},
    ],
    "fr": [
        {"name": "VEKARRA", "tech": "Unity · Roguelite · Co-op local",
         "desc": "Roguelite d'expédition en groupe : quatre héros, cartes procédurales, combat en temps actif. Démo jouable sur itch.io.",
         "link": "fernandoluz.itch.io/vekarra"},
        {"name": "CrimeTrip", "tech": "Unity · RA · FastAPI · Azure · PlayFab",
         "desc": "Jeu d'aventure policière en réalité augmentée — enquêtez sur six affaires non résolues au cœur de scènes de crime en RA.",
         "link": "prologuexr.com/crimetrip"},
        {"name": "Viva La Execution!", "tech": "Unity · FastAPI · OpenAI · ElevenLabs",
         "desc": "Jeu narratif humoristique se déroulant pendant la Révolution française, avec des dialogues générés dynamiquement par IA.",
         "link": "danyboyyy.itch.io/viva-la-execution"},
        {"name": "Down Below", "tech": "Unity3D · C# · Combat au tour par tour",
         "desc": "JRPG au tour par tour inspiré de Darkest Dungeon — création d'équipe, combat et système de butin.",
         "link": "vimeo.com/697498158"},
        {"name": "Janos", "tech": "Unity · Oculus Rift · Game Jam",
         "desc": "Jeu de réflexion en RV conçu pour éviter le mal des transports — un robot à deux têtes dans un escape room. Réalisé au SPJam.",
         "link": "youtube.com/watch?v=eFgFCMwm-5U"},
        {"name": "Missão Fundo do Mar", "tech": "Unity · Vision par ordinateur · Vidéomapping",
         "desc": "Mur de projection interactif utilisant la reconnaissance d'images par IA pour donner vie aux dessins d'enfants (Parc de la Monica).",
         "link": "vimeo.com/359048835"},
    ],
    "ptbr": [
        {"name": "VEKARRA", "tech": "Unity · Roguelite · Co-op Local",
         "desc": "Roguelite de expedição em grupo: quatro heróis, mapas procedurais, combate em tempo ativo. Demo jogável no itch.io.",
         "link": "fernandoluz.itch.io/vekarra"},
        {"name": "CrimeTrip", "tech": "Unity · RA · FastAPI · Azure · PlayFab",
         "desc": "Jogo de aventura de true crime em realidade aumentada — investigue seis casos arquivados dentro de cenas de crime em RA.",
         "link": "prologuexr.com/crimetrip"},
        {"name": "Viva La Execution!", "tech": "Unity · FastAPI · OpenAI · ElevenLabs",
         "desc": "Jogo narrativo de humor ambientado na Revolução Francesa, com diálogos gerados dinamicamente por IA.",
         "link": "danyboyyy.itch.io/viva-la-execution"},
        {"name": "Down Below", "tech": "Unity3D · C# · Combate por turnos",
         "desc": "JRPG por turnos inspirado em Darkest Dungeon — montagem de grupo, combate e sistema de recompensas.",
         "link": "vimeo.com/697498158"},
        {"name": "Janos", "tech": "Unity · Oculus Rift · Game Jam",
         "desc": "Jogo de puzzle em RV feito com foco em conforto para evitar enjoo — um robô de duas cabeças em um escape room. Criado no SPJam.",
         "link": "youtube.com/watch?v=eFgFCMwm-5U"},
        {"name": "Missão Fundo do Mar", "tech": "Unity · Visão computacional · Videomapping",
         "desc": "Parede de projeção interativa usando reconhecimento de imagem por IA para dar vida aos desenhos das crianças (Parque da Mônica).",
         "link": "vimeo.com/359048835"},
    ]
}

# Hackathons
HACKATHONS = {
    "en": [
        "1st place — EIT Digital DeepHack (Olivetti) — Trento, Italy (2019)",
        "1st place — HackaEngage — Campus Party (2019)",
        "1st place — FIESP Hackathon — Digital Government (2019)",
        "1st place — VISA Hackathon — Agitech (2017)",
        "2nd place — IBM BlueHack (2017)",
        "2nd place — Synvia Hackathon (2019)",
        "2nd place — Uber Hack (2019)",
    ],
    "fr": [
        "1re place — EIT Digital DeepHack (Olivetti) — Trente, Italie (2019)",
        "1re place — HackaEngage — Campus Party (2019)",
        "1re place — FIESP Hackathon — Gouvernement numérique (2019)",
        "1re place — VISA Hackathon — Agitech (2017)",
        "2e place — IBM BlueHack (2017)",
        "2e place — Synvia Hackathon (2019)",
        "2e place — Uber Hack (2019)",
    ],
    "ptbr": [
        "1º lugar — EIT Digital DeepHack (Olivetti) — Trento, Itália (2019)",
        "1º lugar — HackaEngage — Campus Party (2019)",
        "1º lugar — FIESP Hackathon — Governo Digital (2019)",
        "1º lugar — VISA Hackathon — Agitech (2017)",
        "2º lugar — IBM BlueHack (2017)",
        "2º lugar — Synvia Hackathon (2019)",
        "2º lugar — Uber Hack (2019)",
    ]
}

# Education
EDUCATION = {
    "en": [
        {"degree": "B.Sc. Computer Science", "school": "Faculdades Metropolitanas Unidas (FMU)", "years": "2020 – 2023"},
        {"degree": "B.A. Game Design", "school": "Universidade Anhembi Morumbi", "years": "2012 – 2016"},
    ],
    "fr": [
        {"degree": "Baccalauréat en informatique", "school": "Faculdades Metropolitanas Unidas (FMU)", "years": "2020 – 2023"},
        {"degree": "Baccalauréat en game design", "school": "Universidade Anhembi Morumbi", "years": "2012 – 2016"},
    ],
    "ptbr": [
        {"degree": "Bacharelado em Ciência da Computação", "school": "Faculdades Metropolitanas Unidas (FMU)", "years": "2020 – 2023"},
        {"degree": "Bacharelado em Game Design", "school": "Universidade Anhembi Morumbi", "years": "2012 – 2016"},
    ]
}

# Certifications
CERTIFICATIONS = {
    "en": [
        {"name": "Unity Certified Developer (2016)", "note": "among the first in the world"},
        {"name": "Python Programming for SysAdmins", "note": "4Linux (2019)"},
        {"name": "Python Fundamentals", "note": "4Linux (2019)"},
    ],
    "fr": [
        {"name": "Unity Certified Developer (2016)", "note": "parmi les premiers au monde"},
        {"name": "Python Programming for SysAdmins", "note": "4Linux (2019)"},
        {"name": "Python Fundamentals", "note": "4Linux (2019)"},
    ],
    "ptbr": [
        {"name": "Unity Certified Developer (2016)", "note": "entre os primeiros do mundo"},
        {"name": "Python Programming for SysAdmins", "note": "4Linux (2019)"},
        {"name": "Python Fundamentals", "note": "4Linux (2019)"},
    ]
}

# Languages spoken
LANGUAGES_SPOKEN = {
    "en": [
        {"lang": "Portuguese", "level": "Native"},
        {"lang": "English", "level": "Fluent (bilingual)"},
        {"lang": "French", "level": "Intermediate (improving)"},
    ],
    "fr": [
        {"lang": "Portugais", "level": "Langue maternelle"},
        {"lang": "Anglais", "level": "Courant (bilingue)"},
        {"lang": "Français", "level": "Intermédiaire (en progression)"},
    ],
    "ptbr": [
        {"lang": "Português", "level": "Nativo"},
        {"lang": "Inglês", "level": "Fluente (bilíngue)"},
        {"lang": "Francês", "level": "Intermediário (em evolução)"},
    ]
}

# CSS styling for PDFs
CSS_STYLE = """
@page {
    size: letter;
    margin: 0.5in 0.6in 0.5in 0.6in;
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    font-size: 10pt;
    line-height: 1.35;
    color: #1a1a1a;
}

.header {
    text-align: center;
    margin-bottom: 12pt;
    border-bottom: 1.5pt solid #2c5aa0;
    padding-bottom: 10pt;
}

.name {
    font-size: 22pt;
    font-weight: bold;
    color: #1a1a1a;
    margin-bottom: 3pt;
}

.title {
    font-size: 12pt;
    color: #2c5aa0;
    margin-bottom: 6pt;
}

.contact-line {
    font-size: 9pt;
    color: #444;
}

.contact-line a {
    color: #2c5aa0;
    text-decoration: none;
}

.section {
    margin-bottom: 10pt;
}

.section-title {
    font-size: 11pt;
    font-weight: bold;
    color: #2c5aa0;
    text-transform: uppercase;
    letter-spacing: 0.5pt;
    border-bottom: 0.75pt solid #ccc;
    padding-bottom: 3pt;
    margin-bottom: 6pt;
}

.profile-text {
    font-size: 10pt;
    text-align: justify;
}

.skills-text {
    font-size: 9.5pt;
}

.skills-text b {
    color: #333;
}

.experience-item {
    margin-bottom: 8pt;
}

.exp-header {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    flex-wrap: wrap;
}

.exp-title {
    font-weight: bold;
    font-size: 10.5pt;
}

.exp-dates {
    font-size: 9.5pt;
    color: #555;
}

.exp-company {
    font-size: 9.5pt;
    color: #2c5aa0;
}

.exp-company .location {
    color: #666;
}

.exp-bullets {
    margin-left: 15pt;
    margin-top: 3pt;
}

.exp-bullets li {
    font-size: 9.5pt;
    margin-bottom: 2pt;
}

.earlier-exp {
    font-size: 9pt;
    color: #555;
    font-style: italic;
    margin-top: 6pt;
}

.project-item {
    margin-bottom: 5pt;
}

.project-name {
    font-weight: bold;
    font-size: 10pt;
}

.project-tech {
    color: #2c5aa0;
    font-size: 9pt;
}

.project-desc {
    font-size: 9pt;
    color: #444;
}

.project-link {
    font-size: 8.5pt;
    color: #2c5aa0;
}

.hackathon-list {
    font-size: 9.5pt;
}

.hackathon-list li {
    margin-bottom: 1pt;
}

.education-item {
    margin-bottom: 4pt;
}

.edu-degree {
    font-weight: bold;
    font-size: 10pt;
}

.edu-school {
    font-size: 9.5pt;
    color: #444;
}

.edu-years {
    font-size: 9pt;
    color: #666;
    float: right;
}

.cert-list {
    font-size: 9.5pt;
}

.cert-list li {
    margin-bottom: 1pt;
}

.languages-row {
    display: flex;
    justify-content: space-between;
    font-size: 9.5pt;
}

.lang-item {
    text-align: center;
}

.lang-name {
    font-weight: bold;
}

.lang-level {
    color: #555;
    font-size: 9pt;
}

ul {
    list-style-type: disc;
    padding-left: 15pt;
}
"""

def generate_html(role, lang):
    """Generate HTML content for a specific role and language."""
    
    # Build experience section
    exp_html = ""
    for exp in EXPERIENCE[role][lang]:
        bullets_html = "".join(f"<li>{b}</li>" for b in exp["bullets"])
        exp_html += f"""
        <div class="experience-item">
            <div class="exp-header">
                <span class="exp-title">{exp["title"]}</span>
                <span class="exp-dates">{exp["dates"]}</span>
            </div>
            <div class="exp-company">{exp["company"]} <span class="location">· {exp["location"]}</span></div>
            <ul class="exp-bullets">{bullets_html}</ul>
        </div>
        """
    
    exp_html += f'<div class="earlier-exp">{EARLIER_EXP[role][lang]}</div>'
    
    # Build projects section
    proj_html = ""
    for proj in PROJECTS[lang]:
        proj_html += f"""
        <div class="project-item">
            <span class="project-name">{proj["name"]}</span> — <span class="project-tech">{proj["tech"]}</span><br>
            <span class="project-desc">{proj["desc"]}</span> <span class="project-link">{proj["link"]}</span>
        </div>
        """
    
    # Build hackathons
    hack_html = "".join(f"<li>{h}</li>" for h in HACKATHONS[lang])
    
    # Build education
    edu_html = ""
    for edu in EDUCATION[lang]:
        edu_html += f"""
        <div class="education-item">
            <span class="edu-years">{edu["years"]}</span>
            <span class="edu-degree">{edu["degree"]}</span> · <span class="edu-school">{edu["school"]}</span>
        </div>
        """
    
    # Build certifications
    cert_html = "".join(f"<li>{c['name']} — {c['note']}</li>" for c in CERTIFICATIONS[lang])
    
    # Build languages
    lang_html = ""
    for spoken in LANGUAGES_SPOKEN[lang]:
        lang_html += f"""
        <div class="lang-item">
            <span class="lang-name">{spoken["lang"]}</span><br>
            <span class="lang-level">{spoken["level"]}</span>
        </div>
        """
    
    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{CONTACT["name"]} — {TITLES[role][lang]}</title>
</head>
<body>
    <div class="header">
        <div class="name">{CONTACT["name"]}</div>
        <div class="title">{TITLES[role][lang]}</div>
        <div class="contact-line">
            {CONTACT["location"][lang]} · {CONTACT["phone"]} · {CONTACT["email"]}<br>
            <a href="https://{CONTACT["linkedin"]}">{CONTACT["linkedin"]}</a> · 
            <a href="https://{CONTACT["github"]}">{CONTACT["github"]}</a> · 
            <a href="https://{CONTACT["website"]}">{CONTACT["website"]}</a>
        </div>
    </div>
    
    <div class="section">
        <div class="section-title">{HEADERS["profile"][lang]}</div>
        <div class="profile-text">{PROFILES[role][lang]}</div>
    </div>
    
    <div class="section">
        <div class="section-title">{HEADERS["skills"][lang]}</div>
        <div class="skills-text">{SKILLS[role][lang]}</div>
    </div>
    
    <div class="section">
        <div class="section-title">{HEADERS["experience"][lang]}</div>
        {exp_html}
    </div>
    
    <div class="section">
        <div class="section-title">{HEADERS["projects"][lang]}</div>
        {proj_html}
    </div>
    
    <div class="section">
        <div class="section-title">{HEADERS["hackathons"][lang]}</div>
        <ul class="hackathon-list">{hack_html}</ul>
    </div>
    
    <div class="section">
        <div class="section-title">{HEADERS["education"][lang]}</div>
        {edu_html}
    </div>
    
    <div class="section">
        <div class="section-title">{HEADERS["certifications"][lang]}</div>
        <ul class="cert-list">{cert_html}</ul>
    </div>
    
    <div class="section">
        <div class="section-title">{HEADERS["languages"][lang]}</div>
        <div class="languages-row">{lang_html}</div>
    </div>
</body>
</html>"""
    
    return html


def generate_pdf(role, lang_code, lang):
    """Generate a PDF for a specific role and language."""
    html_content = generate_html(role, lang)
    
    output_dir = "assets/resumes"
    os.makedirs(output_dir, exist_ok=True)
    
    filename = f"Fernando_Silva_da_Luz_{role}_{lang_code}.pdf"
    filepath = os.path.join(output_dir, filename)
    
    html = HTML(string=html_content)
    css = CSS(string=CSS_STYLE)
    
    html.write_pdf(filepath, stylesheets=[css])
    print(f"Generated: {filepath}")
    
    return filepath


def main():
    """Generate all 9 PDFs."""
    print("Generating résumé PDFs...")
    print("=" * 50)
    
    generated = []
    
    for role in ROLES:
        for lang_code, lang in LANGS.items():
            filepath = generate_pdf(role, lang_code, lang)
            generated.append(filepath)
    
    print("=" * 50)
    print(f"Successfully generated {len(generated)} PDFs:")
    for path in generated:
        print(f"  - {path}")


if __name__ == "__main__":
    main()
