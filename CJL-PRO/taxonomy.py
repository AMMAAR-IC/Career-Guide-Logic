"""
taxonomy.py
===========
Defines the 3-layer career drill-down tree:
  Stage 1: Broad Fields       (Science, Arts, Commerce, etc.)
  Stage 2: Sub-Fields         (within each field)
  Stage 3: Specializations    (within each sub-field)

Each node carries:
  - trait_weights: how normalised traits drive it
  - riasec_code:  dominant RIASEC letters
  - description:  short label for terminal display
"""

# ─────────────────────────────────────────────────────────────────
# STAGE 1 — BROAD FIELDS
# Traits: apt, O, C, E, A, stab, R, I, Art
# ─────────────────────────────────────────────────────────────────
FIELDS = {
    "Science": {
        "description": "Empirical inquiry, analysis, discovery",
        "trait_weights": {"apt": 0.30, "I": 0.35, "O": 0.20, "C": 0.10, "stab": 0.05},
        "emoji": "🔬",
    },
    "Technology": {
        "description": "Engineering systems, software, hardware",
        "trait_weights": {"apt": 0.30, "I": 0.25, "R": 0.20, "C": 0.15, "O": 0.10},
        "emoji": "💻",
    },
    "Arts & Humanities": {
        "description": "Creative expression, culture, language",
        "trait_weights": {"Art": 0.40, "O": 0.30, "E": 0.12, "A": 0.10, "stab": 0.08},
        "emoji": "🎨",
    },
    "Commerce & Business": {
        "description": "Trade, finance, enterprise, management",
        "trait_weights": {"apt": 0.25, "C": 0.25, "E": 0.20, "A": 0.15, "stab": 0.15},
        "emoji": "📈",
    },
    "Medicine & Health": {
        "description": "Human wellbeing, diagnosis, care",
        "trait_weights": {"apt": 0.20, "I": 0.20, "A": 0.25, "C": 0.20, "stab": 0.15},
        "emoji": "🏥",
    },
    "Law & Social Sciences": {
        "description": "Justice, society, policy, human behavior",
        "trait_weights": {"apt": 0.25, "E": 0.20, "O": 0.20, "A": 0.20, "I": 0.15},
        "emoji": "⚖️",
    },
    "Education": {
        "description": "Teaching, training, curriculum, mentorship",
        "trait_weights": {"A": 0.30, "E": 0.25, "O": 0.20, "C": 0.15, "stab": 0.10},
        "emoji": "📚",
    },
    "Trades & Engineering": {
        "description": "Practical construction, machinery, infrastructure",
        "trait_weights": {"R": 0.40, "C": 0.25, "apt": 0.20, "stab": 0.10, "I": 0.05},
        "emoji": "🔧",
    },
    "Sports & Physical": {
        "description": "Athletics, fitness, outdoor, coaching",
        "trait_weights": {"R": 0.35, "E": 0.25, "stab": 0.20, "C": 0.12, "A": 0.08},
        "emoji": "🏋️",
    },
    "Environment & Agriculture": {
        "description": "Ecology, sustainability, food systems",
        "trait_weights": {"R": 0.28, "I": 0.22, "O": 0.20, "C": 0.18, "A": 0.12},
        "emoji": "🌱",
    },
}

# ─────────────────────────────────────────────────────────────────
# STAGE 2 — SUB-FIELDS  (keyed by Field name)
# ─────────────────────────────────────────────────────────────────
SUB_FIELDS = {

    "Science": {
        "Computer Science": {
            "description": "Algorithms, data, computation theory",
            "trait_weights": {"apt": 0.35, "I": 0.35, "C": 0.20, "O": 0.10},
        },
        "Biological Sciences": {
            "description": "Life, organisms, genetics, ecology",
            "trait_weights": {"I": 0.35, "O": 0.25, "A": 0.20, "C": 0.15, "apt": 0.05},
        },
        "Chemical Sciences": {
            "description": "Matter, reactions, molecular structure",
            "trait_weights": {"apt": 0.30, "I": 0.35, "C": 0.25, "O": 0.10},
        },
        "Physics & Math": {
            "description": "Fundamental forces, abstract structures",
            "trait_weights": {"apt": 0.40, "I": 0.35, "O": 0.15, "C": 0.10},
        },
        "Earth & Space Sciences": {
            "description": "Geology, astronomy, climate, oceans",
            "trait_weights": {"I": 0.30, "O": 0.30, "R": 0.20, "apt": 0.12, "C": 0.08},
        },
        "Psychology": {
            "description": "Mind, behavior, cognition, mental health",
            "trait_weights": {"I": 0.28, "A": 0.28, "O": 0.22, "E": 0.12, "stab": 0.10},
        },
    },

    "Technology": {
        "Software Development": {
            "description": "Building applications, systems, APIs",
            "trait_weights": {"apt": 0.35, "I": 0.30, "C": 0.25, "O": 0.10},
        },
        "Artificial Intelligence & Data": {
            "description": "ML, deep learning, analytics, statistics",
            "trait_weights": {"apt": 0.35, "I": 0.35, "O": 0.15, "C": 0.15},
        },
        "Cybersecurity": {
            "description": "Networks, vulnerabilities, defense, forensics",
            "trait_weights": {"apt": 0.30, "I": 0.30, "C": 0.25, "stab": 0.15},
        },
        "Hardware & Electronics": {
            "description": "Circuits, embedded systems, IoT",
            "trait_weights": {"R": 0.30, "I": 0.30, "apt": 0.25, "C": 0.15},
        },
        "Cloud & DevOps": {
            "description": "Infrastructure, automation, deployment pipelines",
            "trait_weights": {"apt": 0.30, "C": 0.30, "I": 0.25, "stab": 0.15},
        },
        "UX & Product Design": {
            "description": "User experience, product strategy, interfaces",
            "trait_weights": {"Art": 0.30, "I": 0.25, "E": 0.20, "O": 0.15, "A": 0.10},
        },
    },

    "Arts & Humanities": {
        "Visual Arts": {
            "description": "Painting, sculpture, illustration, photography",
            "trait_weights": {"Art": 0.45, "O": 0.35, "C": 0.10, "stab": 0.10},
        },
        "Performing Arts": {
            "description": "Theatre, dance, music performance",
            "trait_weights": {"Art": 0.35, "E": 0.30, "O": 0.20, "stab": 0.15},
        },
        "Literature & Writing": {
            "description": "Fiction, journalism, poetry, content",
            "trait_weights": {"Art": 0.30, "O": 0.35, "I": 0.20, "C": 0.15},
        },
        "Film & Media Production": {
            "description": "Directing, editing, cinematography, broadcasting",
            "trait_weights": {"Art": 0.30, "E": 0.25, "O": 0.25, "C": 0.20},
        },
        "History & Philosophy": {
            "description": "Critical thinking, ethics, civilizations",
            "trait_weights": {"O": 0.35, "I": 0.30, "C": 0.20, "apt": 0.15},
        },
        "Languages & Linguistics": {
            "description": "Translation, communication, language structure",
            "trait_weights": {"O": 0.30, "A": 0.25, "E": 0.25, "I": 0.20},
        },
    },

    "Commerce & Business": {
        "Finance & Accounting": {
            "description": "Numbers, investments, auditing, tax",
            "trait_weights": {"apt": 0.35, "C": 0.30, "I": 0.20, "stab": 0.15},
        },
        "Marketing & Sales": {
            "description": "Brand, persuasion, customer acquisition",
            "trait_weights": {"E": 0.30, "Art": 0.20, "O": 0.20, "C": 0.15, "A": 0.15},
        },
        "Entrepreneurship": {
            "description": "Startups, innovation, risk, leadership",
            "trait_weights": {"E": 0.25, "O": 0.25, "stab": 0.20, "C": 0.15, "apt": 0.15},
        },
        "Operations & Supply Chain": {
            "description": "Logistics, process optimization, quality",
            "trait_weights": {"C": 0.35, "R": 0.25, "apt": 0.20, "stab": 0.20},
        },
        "Human Resources": {
            "description": "People, recruitment, culture, training",
            "trait_weights": {"A": 0.35, "E": 0.30, "C": 0.20, "stab": 0.15},
        },
        "Economics & Policy": {
            "description": "Macro/micro economics, public policy analysis",
            "trait_weights": {"apt": 0.30, "I": 0.30, "O": 0.20, "C": 0.20},
        },
    },

    "Medicine & Health": {
        "Clinical Medicine": {
            "description": "Diagnosis, treatment, direct patient care",
            "trait_weights": {"I": 0.25, "A": 0.25, "C": 0.25, "stab": 0.15, "apt": 0.10},
        },
        "Surgery & Specialties": {
            "description": "Operative precision, high-stakes interventions",
            "trait_weights": {"apt": 0.25, "C": 0.30, "stab": 0.25, "R": 0.10, "I": 0.10},
        },
        "Mental Health": {
            "description": "Psychiatry, therapy, counseling",
            "trait_weights": {"A": 0.35, "O": 0.20, "stab": 0.20, "I": 0.15, "E": 0.10},
        },
        "Pharmacy & Biomedical": {
            "description": "Drug science, lab research, biochemistry",
            "trait_weights": {"apt": 0.30, "I": 0.30, "C": 0.30, "O": 0.10},
        },
        "Nursing & Allied Health": {
            "description": "Patient support, therapy, rehabilitation",
            "trait_weights": {"A": 0.35, "C": 0.25, "stab": 0.20, "E": 0.20},
        },
        "Public Health": {
            "description": "Epidemiology, policy, population wellness",
            "trait_weights": {"I": 0.25, "A": 0.25, "O": 0.20, "E": 0.15, "C": 0.15},
        },
    },

    "Law & Social Sciences": {
        "Law & Legal Practice": {
            "description": "Litigation, contracts, advocacy, justice",
            "trait_weights": {"apt": 0.30, "E": 0.25, "C": 0.25, "O": 0.20},
        },
        "Sociology & Anthropology": {
            "description": "Society, culture, human groups, fieldwork",
            "trait_weights": {"O": 0.30, "I": 0.25, "A": 0.25, "E": 0.20},
        },
        "Political Science": {
            "description": "Government, power, international relations",
            "trait_weights": {"E": 0.28, "O": 0.25, "apt": 0.22, "I": 0.25},
        },
        "Social Work": {
            "description": "Community support, welfare, advocacy",
            "trait_weights": {"A": 0.40, "E": 0.25, "stab": 0.20, "C": 0.15},
        },
        "Criminology & Forensics": {
            "description": "Crime, investigation, evidence, behavior",
            "trait_weights": {"I": 0.30, "C": 0.25, "stab": 0.25, "apt": 0.20},
        },
    },

    "Education": {
        "Primary & Secondary Teaching": {
            "description": "K-12 classroom instruction, child development",
            "trait_weights": {"A": 0.30, "E": 0.30, "C": 0.20, "stab": 0.20},
        },
        "Higher Education & Research": {
            "description": "University lecturing, academic publishing",
            "trait_weights": {"I": 0.30, "O": 0.25, "C": 0.25, "E": 0.20},
        },
        "Special Education": {
            "description": "Inclusive learning, disabilities, adaptive methods",
            "trait_weights": {"A": 0.35, "stab": 0.25, "C": 0.25, "E": 0.15},
        },
        "Corporate Training & L&D": {
            "description": "Adult learning, professional development, e-learning",
            "trait_weights": {"E": 0.30, "C": 0.25, "O": 0.25, "A": 0.20},
        },
        "Educational Technology": {
            "description": "EdTech, learning platforms, instructional design",
            "trait_weights": {"O": 0.25, "I": 0.25, "C": 0.25, "Art": 0.15, "E": 0.10},
        },
    },

    "Trades & Engineering": {
        "Civil & Structural Engineering": {
            "description": "Buildings, bridges, infrastructure design",
            "trait_weights": {"R": 0.30, "apt": 0.30, "C": 0.25, "I": 0.15},
        },
        "Electrical Engineering": {
            "description": "Power, circuits, electronics, automation",
            "trait_weights": {"apt": 0.30, "I": 0.30, "R": 0.25, "C": 0.15},
        },
        "Mechanical Engineering": {
            "description": "Machines, thermodynamics, manufacturing",
            "trait_weights": {"R": 0.30, "apt": 0.30, "I": 0.25, "C": 0.15},
        },
        "Construction & Carpentry": {
            "description": "Hands-on building, site work, craftsmanship",
            "trait_weights": {"R": 0.45, "C": 0.25, "stab": 0.20, "A": 0.10},
        },
        "Chemical Engineering": {
            "description": "Processes, materials, energy, refining",
            "trait_weights": {"apt": 0.35, "I": 0.30, "C": 0.25, "R": 0.10},
        },
        "Automotive & Aerospace": {
            "description": "Vehicles, propulsion, aerodynamics",
            "trait_weights": {"R": 0.30, "I": 0.28, "apt": 0.27, "C": 0.15},
        },
    },

    "Sports & Physical": {
        "Professional Athletics": {
            "description": "Competitive sport, performance, training",
            "trait_weights": {"R": 0.35, "stab": 0.30, "E": 0.20, "C": 0.15},
        },
        "Coaching & Sports Science": {
            "description": "Athletic training methodology, biomechanics",
            "trait_weights": {"R": 0.25, "I": 0.25, "E": 0.25, "A": 0.15, "C": 0.10},
        },
        "Physiotherapy & Rehabilitation": {
            "description": "Injury recovery, movement science, patient care",
            "trait_weights": {"A": 0.30, "I": 0.25, "R": 0.25, "stab": 0.20},
        },
        "Nutrition & Dietetics": {
            "description": "Food science, health optimization, counseling",
            "trait_weights": {"I": 0.30, "A": 0.25, "C": 0.25, "O": 0.20},
        },
        "Outdoor & Adventure Education": {
            "description": "Wilderness, experiential learning, leadership",
            "trait_weights": {"R": 0.35, "O": 0.25, "E": 0.20, "A": 0.20},
        },
    },

    "Environment & Agriculture": {
        "Environmental Science": {
            "description": "Climate, pollution, conservation, research",
            "trait_weights": {"I": 0.30, "O": 0.25, "R": 0.25, "C": 0.20},
        },
        "Agriculture & Food Science": {
            "description": "Farming, crop science, food technology",
            "trait_weights": {"R": 0.35, "I": 0.25, "C": 0.25, "O": 0.15},
        },
        "Forestry & Wildlife": {
            "description": "Ecosystems, conservation biology, rangers",
            "trait_weights": {"R": 0.35, "O": 0.25, "I": 0.20, "A": 0.20},
        },
        "Sustainability & Green Energy": {
            "description": "Renewables, carbon, circular economy, policy",
            "trait_weights": {"O": 0.30, "I": 0.25, "C": 0.25, "A": 0.20},
        },
        "Marine & Oceanography": {
            "description": "Ocean systems, aquatic biology, deep-sea research",
            "trait_weights": {"I": 0.30, "R": 0.25, "O": 0.25, "C": 0.20},
        },
    },
}

# ─────────────────────────────────────────────────────────────────
# STAGE 3 — SPECIALIZATIONS  (keyed by Sub-Field name)
# ─────────────────────────────────────────────────────────────────
SPECIALIZATIONS = {

    # ── Technology > Software Development ────────────────────────
    "Software Development": {
        "Backend Engineering": {
            "description": "APIs, databases, server logic, microservices",
            "trait_weights": {"apt": 0.35, "I": 0.30, "C": 0.25, "O": 0.10},
            "tools": ["Python/Go/Java", "PostgreSQL", "REST/gRPC", "Docker"],
        },
        "Frontend Engineering": {
            "description": "UI, browser rendering, accessibility, performance",
            "trait_weights": {"Art": 0.25, "apt": 0.25, "I": 0.25, "O": 0.15, "C": 0.10},
            "tools": ["React/Vue/Angular", "CSS", "TypeScript", "Figma"],
        },
        "Mobile Development": {
            "description": "iOS/Android apps, cross-platform frameworks",
            "trait_weights": {"apt": 0.30, "I": 0.25, "Art": 0.20, "C": 0.25},
            "tools": ["Swift/Kotlin", "Flutter/React Native", "Firebase"],
        },
        "Full Stack": {
            "description": "End-to-end: client, server, database, deployment",
            "trait_weights": {"apt": 0.30, "I": 0.28, "C": 0.22, "O": 0.12, "Art": 0.08},
            "tools": ["Next.js", "Node.js", "PostgreSQL", "CI/CD"],
        },
        "Embedded & Systems": {
            "description": "Low-level programming, OS, firmware, real-time",
            "trait_weights": {"apt": 0.35, "R": 0.25, "I": 0.25, "C": 0.15},
            "tools": ["C/C++/Rust", "RTOS", "Linux kernel", "Assembly"],
        },
        "Game Development": {
            "description": "Interactive experiences, graphics, physics engines",
            "trait_weights": {"Art": 0.25, "apt": 0.25, "I": 0.25, "O": 0.15, "C": 0.10},
            "tools": ["Unity/Unreal", "C#/C++", "GLSL/Shaders", "Blender"],
        },
    },

    # ── Technology > AI & Data ───────────────────────────────────
    "Artificial Intelligence & Data": {
        "Machine Learning Engineering": {
            "description": "Building and deploying ML models at scale",
            "trait_weights": {"apt": 0.35, "I": 0.35, "C": 0.20, "O": 0.10},
            "tools": ["Python", "PyTorch/TF", "MLflow", "Kubernetes"],
        },
        "Deep Learning & NLP": {
            "description": "Neural networks, language models, vision AI",
            "trait_weights": {"apt": 0.35, "I": 0.35, "O": 0.20, "C": 0.10},
            "tools": ["Transformers", "CUDA", "HuggingFace", "LangChain"],
        },
        "Data Science & Analytics": {
            "description": "Statistical analysis, insight extraction, BI",
            "trait_weights": {"apt": 0.30, "I": 0.30, "C": 0.25, "O": 0.15},
            "tools": ["Python/R", "SQL", "Tableau/PowerBI", "Spark"],
        },
        "Data Engineering": {
            "description": "Pipelines, warehouses, ETL, real-time streaming",
            "trait_weights": {"apt": 0.30, "C": 0.30, "I": 0.25, "R": 0.15},
            "tools": ["Airflow", "Kafka", "dbt", "Snowflake"],
        },
        "Computer Vision": {
            "description": "Image recognition, object detection, video analysis",
            "trait_weights": {"apt": 0.30, "I": 0.35, "Art": 0.15, "O": 0.20},
            "tools": ["OpenCV", "YOLO", "PyTorch", "CUDA"],
        },
        "AI Research": {
            "description": "Novel architectures, benchmarks, academic papers",
            "trait_weights": {"apt": 0.35, "I": 0.40, "O": 0.20, "C": 0.05},
            "tools": ["LaTeX", "PyTorch", "HPC clusters", "arXiv"],
        },
    },

    # ── Science > Computer Science ───────────────────────────────
    "Computer Science": {
        "AI & Machine Learning": {
            "description": "Theory and practice of intelligent systems",
            "trait_weights": {"apt": 0.35, "I": 0.40, "O": 0.15, "C": 0.10},
            "tools": ["Python", "Math (linear algebra, stats)", "PyTorch"],
        },
        "Theoretical Computer Science": {
            "description": "Algorithms, complexity, automata, formal methods",
            "trait_weights": {"apt": 0.45, "I": 0.35, "O": 0.15, "C": 0.05},
            "tools": ["Proof writing", "Graph theory", "Haskell/Coq"],
        },
        "Software Engineering": {
            "description": "Systems design, architecture, coding methodology",
            "trait_weights": {"apt": 0.30, "I": 0.28, "C": 0.28, "O": 0.14},
            "tools": ["Design patterns", "Agile", "System design"],
        },
        "Human-Computer Interaction": {
            "description": "Usability, accessibility, cognitive ergonomics",
            "trait_weights": {"I": 0.25, "Art": 0.25, "A": 0.25, "E": 0.25},
            "tools": ["UX research", "Eye tracking", "Prototyping tools"],
        },
        "Networks & Security": {
            "description": "Distributed systems, protocols, cryptography",
            "trait_weights": {"apt": 0.30, "I": 0.30, "C": 0.25, "stab": 0.15},
            "tools": ["Wireshark", "Linux", "Cryptography math"],
        },
        "Database Systems": {
            "description": "Storage engines, query optimization, data models",
            "trait_weights": {"apt": 0.30, "I": 0.30, "C": 0.30, "O": 0.10},
            "tools": ["SQL/NoSQL", "Query planning", "Indexing"],
        },
    },

    # ── Science > Biological Sciences ────────────────────────────
    "Biological Sciences": {
        "Genetics & Genomics": {
            "description": "DNA, gene expression, sequencing, CRISPR",
            "trait_weights": {"I": 0.35, "apt": 0.25, "C": 0.25, "O": 0.15},
            "tools": ["PCR", "Bioinformatics", "CRISPR", "R/Python"],
        },
        "Microbiology": {
            "description": "Bacteria, viruses, infection, antimicrobials",
            "trait_weights": {"I": 0.35, "C": 0.30, "apt": 0.20, "A": 0.15},
            "tools": ["Culture techniques", "Microscopy", "ELISA"],
        },
        "Ecology & Conservation": {
            "description": "Ecosystems, biodiversity, wildlife, fieldwork",
            "trait_weights": {"O": 0.30, "R": 0.28, "I": 0.25, "A": 0.17},
            "tools": ["GIS", "Field sampling", "Statistical ecology"],
        },
        "Neuroscience": {
            "description": "Brain, neural circuits, cognition, behavior",
            "trait_weights": {"I": 0.35, "apt": 0.25, "O": 0.25, "A": 0.15},
            "tools": ["fMRI", "Patch clamp", "MATLAB", "Python"],
        },
        "Biochemistry": {
            "description": "Molecules of life: proteins, enzymes, metabolism",
            "trait_weights": {"I": 0.30, "apt": 0.30, "C": 0.25, "O": 0.15},
            "tools": ["Chromatography", "Spectroscopy", "Cell culture"],
        },
    },

    # ── Arts > Visual Arts ───────────────────────────────────────
    "Visual Arts": {
        "Graphic Design": {
            "description": "Branding, layout, typography, visual identity",
            "trait_weights": {"Art": 0.40, "O": 0.30, "C": 0.20, "E": 0.10},
            "tools": ["Adobe Suite", "Figma", "Typography", "Color theory"],
        },
        "Illustration & Animation": {
            "description": "2D/3D character art, motion graphics, storyboards",
            "trait_weights": {"Art": 0.45, "O": 0.30, "C": 0.15, "stab": 0.10},
            "tools": ["Procreate", "After Effects", "Blender", "Clip Studio"],
        },
        "Photography": {
            "description": "Composition, lighting, documentary, commercial",
            "trait_weights": {"Art": 0.35, "O": 0.30, "R": 0.15, "C": 0.20},
            "tools": ["DSLR/mirrorless", "Lightroom", "Composition rules"],
        },
        "Fine Arts & Sculpture": {
            "description": "Traditional mediums, galleries, conceptual art",
            "trait_weights": {"Art": 0.50, "O": 0.35, "stab": 0.10, "C": 0.05},
            "tools": ["Oil/acrylic", "Ceramics", "Installation", "Portfolio"],
        },
        "Fashion & Textile Design": {
            "description": "Clothing, patterns, trends, material science",
            "trait_weights": {"Art": 0.35, "O": 0.30, "E": 0.20, "C": 0.15},
            "tools": ["Pattern making", "CAD", "Fabric knowledge", "Sewing"],
        },
    },

    # ── Arts > Literature & Writing ──────────────────────────────
    "Literature & Writing": {
        "Journalism": {
            "description": "News reporting, investigation, media literacy",
            "trait_weights": {"E": 0.28, "O": 0.25, "I": 0.25, "Art": 0.22},
            "tools": ["AP Style", "Interview techniques", "CMS tools"],
        },
        "Creative Writing": {
            "description": "Fiction, screenwriting, poetry, narrative craft",
            "trait_weights": {"Art": 0.40, "O": 0.40, "stab": 0.10, "I": 0.10},
            "tools": ["Story structure", "Character development", "Scrivener"],
        },
        "Technical Writing": {
            "description": "Documentation, manuals, instructional content",
            "trait_weights": {"C": 0.35, "I": 0.28, "Art": 0.20, "O": 0.17},
            "tools": ["Markdown/LaTeX", "DITA", "Docs-as-code", "Grammarly"],
        },
        "Content & Copywriting": {
            "description": "Marketing copy, SEO, brand voice, social media",
            "trait_weights": {"Art": 0.30, "E": 0.25, "O": 0.25, "C": 0.20},
            "tools": ["SEO tools", "CMS", "Analytics", "Brand guidelines"],
        },
        "Academic & Research Writing": {
            "description": "Scholarly articles, theses, peer review, citations",
            "trait_weights": {"I": 0.35, "C": 0.35, "O": 0.20, "apt": 0.10},
            "tools": ["Zotero", "LaTeX", "Academic databases", "APA/MLA"],
        },
    },

    # ── Commerce > Finance & Accounting ─────────────────────────
    "Finance & Accounting": {
        "Investment Banking": {
            "description": "M&A, capital markets, deal structuring, valuation",
            "trait_weights": {"apt": 0.35, "C": 0.30, "E": 0.20, "stab": 0.15},
            "tools": ["Excel/VBA", "Bloomberg", "Financial modelling", "Pitchbooks"],
        },
        "Portfolio & Asset Management": {
            "description": "Fund management, risk, asset allocation, markets",
            "trait_weights": {"apt": 0.35, "I": 0.30, "C": 0.20, "stab": 0.15},
            "tools": ["Python", "Bloomberg", "Risk metrics", "CFA knowledge"],
        },
        "Accounting & Audit": {
            "description": "GAAP/IFRS, financial statements, tax, compliance",
            "trait_weights": {"C": 0.40, "apt": 0.30, "stab": 0.20, "I": 0.10},
            "tools": ["SAP", "Excel", "Tax software", "Audit standards"],
        },
        "Fintech & Quant Finance": {
            "description": "Algorithmic trading, blockchain, financial models",
            "trait_weights": {"apt": 0.40, "I": 0.35, "O": 0.15, "C": 0.10},
            "tools": ["Python/R", "SQL", "Stochastic calculus", "APIs"],
        },
        "Risk & Actuarial Science": {
            "description": "Statistical modeling of uncertainty and insurance",
            "trait_weights": {"apt": 0.40, "I": 0.30, "C": 0.20, "stab": 0.10},
            "tools": ["R/SAS", "Actuarial exams", "Monte Carlo", "Probability"],
        },
    },

    # ── Medicine > Mental Health ─────────────────────────────────
    "Mental Health": {
        "Clinical Psychology": {
            "description": "Assessment, therapy, CBT, psychological testing",
            "trait_weights": {"I": 0.28, "A": 0.28, "stab": 0.22, "O": 0.12, "C": 0.10},
            "tools": ["DSM-5", "CBT/DBT", "Psychological assessments"],
        },
        "Psychiatry": {
            "description": "Medical diagnosis, psychopharmacology, inpatient care",
            "trait_weights": {"apt": 0.25, "I": 0.28, "stab": 0.25, "A": 0.22},
            "tools": ["DSM-5", "Pharmacology", "Mental Status Exam"],
        },
        "Counseling & Psychotherapy": {
            "description": "Talk therapy, life transitions, relationship issues",
            "trait_weights": {"A": 0.38, "stab": 0.28, "E": 0.18, "O": 0.16},
            "tools": ["Person-centered", "ACT", "MI", "Trauma-informed"],
        },
        "School & Educational Psychology": {
            "description": "Child/adolescent learning, behavioral support, IEPs",
            "trait_weights": {"A": 0.30, "C": 0.25, "stab": 0.25, "E": 0.20},
            "tools": ["WISC", "RTI", "School counseling", "IEP writing"],
        },
        "Neuropsychology": {
            "description": "Brain-behavior relationships, cognitive assessment",
            "trait_weights": {"I": 0.35, "apt": 0.30, "C": 0.20, "A": 0.15},
            "tools": ["Neuroimaging", "WAIS", "Halstead-Reitan", "fMRI"],
        },
    },

    # ── Trades > Electrical Engineering ─────────────────────────
    "Electrical Engineering": {
        "Power Systems": {
            "description": "Grid, transmission, renewable energy integration",
            "trait_weights": {"R": 0.30, "apt": 0.30, "C": 0.25, "I": 0.15},
            "tools": ["MATLAB/Simulink", "AutoCAD Electrical", "PLC"],
        },
        "Electronics & Embedded": {
            "description": "PCBs, microcontrollers, IoT, signal processing",
            "trait_weights": {"R": 0.30, "I": 0.30, "apt": 0.25, "C": 0.15},
            "tools": ["Arduino/STM32", "KiCad", "Oscilloscope", "C/C++"],
        },
        "Telecommunications": {
            "description": "RF, wireless, 5G, network protocols, antennas",
            "trait_weights": {"apt": 0.30, "I": 0.30, "C": 0.25, "R": 0.15},
            "tools": ["MATLAB", "RF equipment", "Wireshark", "Python"],
        },
        "Control Systems & Robotics": {
            "description": "Automation, feedback loops, industrial robots",
            "trait_weights": {"I": 0.32, "R": 0.28, "apt": 0.25, "C": 0.15},
            "tools": ["ROS", "MATLAB/Simulink", "PID control", "Python"],
        },
        "VLSI & Chip Design": {
            "description": "Integrated circuits, semiconductor design, EDA tools",
            "trait_weights": {"apt": 0.35, "I": 0.30, "C": 0.25, "R": 0.10},
            "tools": ["Verilog/VHDL", "Cadence", "Synopsys", "SPICE"],
        },
    },

    # ── Environment > Environmental Science ─────────────────────
    "Environmental Science": {
        "Climate Science": {
            "description": "Atmospheric modeling, GHG, climate projections",
            "trait_weights": {"I": 0.35, "O": 0.25, "C": 0.25, "apt": 0.15},
            "tools": ["Python/R", "GIS", "Climate models", "NetCDF"],
        },
        "Environmental Policy": {
            "description": "Regulation, ESG, international agreements, advocacy",
            "trait_weights": {"O": 0.30, "A": 0.25, "E": 0.25, "I": 0.20},
            "tools": ["Policy analysis", "Stakeholder engagement", "Law"],
        },
        "Ecology & Biodiversity": {
            "description": "Species, habitats, population dynamics, fieldwork",
            "trait_weights": {"R": 0.30, "I": 0.28, "O": 0.25, "A": 0.17},
            "tools": ["GIS/ArcGIS", "R/vegan", "Field surveys", "Camera traps"],
        },
        "Pollution & Waste Management": {
            "description": "Remediation, toxicology, waste streams, compliance",
            "trait_weights": {"I": 0.28, "C": 0.28, "R": 0.25, "stab": 0.19},
            "tools": ["GC-MS", "GIS", "EIA", "Remediation tech"],
        },
        "Water Resources": {
            "description": "Hydrology, water quality, irrigation, WASH",
            "trait_weights": {"I": 0.30, "R": 0.28, "C": 0.25, "apt": 0.17},
            "tools": ["HEC-RAS", "SWAT", "Water chemistry", "GIS"],
        },
    },

    # Fallback for sub-fields not explicitly listed
    "_default_": {
        "Core Track": {
            "description": "Main practitioner path in this sub-field",
            "trait_weights": {"apt": 0.25, "I": 0.25, "C": 0.25, "O": 0.25},
            "tools": ["Domain-specific skills", "Certifications"],
        },
        "Research & Theory": {
            "description": "Academic and theoretical exploration",
            "trait_weights": {"I": 0.40, "O": 0.30, "C": 0.20, "apt": 0.10},
            "tools": ["Research methods", "Literature review", "Publishing"],
        },
        "Applied Practice": {
            "description": "Real-world application and client-facing work",
            "trait_weights": {"A": 0.30, "E": 0.25, "C": 0.25, "stab": 0.20},
            "tools": ["Industry software", "Case management", "Communication"],
        },
    },
}
