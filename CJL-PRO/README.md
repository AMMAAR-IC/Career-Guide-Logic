# 3-Stage Career Path Assessment

This system is a modular, adaptive career guidance engine that utilizes **Aptitude**, **Big Five Personality**, and **RIASEC (Holland Codes)** frameworks to pinpoint optimal career paths. The assessment operates in three progressively narrowing stages, culminating in a personalized AI-generated career insight.

## 🚀 Overview

The assessment follows a "drill-down" logic to ensure high-resolution results:

1. **Stage 1: Broad Field Discovery** (~18 questions) – Identifies the general domain (e.g., Technology, Science, Arts).
2. **Stage 2: Sub-Field Focus** (~15 questions) – Narrows the domain (e.g., within Technology, focuses on Software Development).
3. **Stage 3: Specialization Pinpoint** (~12 questions) – Identifies the specific role (e.g., Backend Engineering).

## 🛠️ Key Components

* **`run.py`**: The main entry point that orchestrates the flow between stages, manages the trait accumulator, and triggers the AI reasoning engine.
* **`engine.py`**: The scoring backbone. It processes Likert-scale answers, updates the 9-dimensional trait vector, and uses a **Weighted Dot-Product → Sigmoid → Softmax** pipeline to rank career candidates.
* **`taxonomy.py`**: The career knowledge base. It defines the hierarchy of Fields, Sub-Fields, and Specializations, including their associated trait weights and required tools.
* **`ai_reasoning.py`**: Integrates with local LLMs (via Ollama) to generate deep, personalized narratives, strengths, and growth areas based on the user's specific trait profile.
* **`terminal_ui.py`**: A pure ANSI-based terminal interface featuring progress bars, interim result panels, and trait profile visualizations.

## 🧠 Psychometric Model

The engine tracks nine core traits throughout the assessment:

* **Aptitude (`apt`)**: General cognitive/technical problem-solving.
* **Big Five**: Openness (`O`), Conscientiousness (`C`), Extraversion (`E`), Agreeableness (`A`), and Emotional Stability (`stab`).
* **RIASEC**: Realistic (`R`), Investigative (`I`), and Artistic (`Art`).

### Adaptive Question Selection

Questions are selected dynamically based on **informativeness**. The engine prioritizes questions targeting traits where the user's current score is near 0.5 (mid-range), effectively "filling the gaps" in the trait profile to maximize discrimination between career paths.

## 💻 Usage

Run the interactive assessment from the terminal:

```bash
python run.py

```

### Command Line Arguments:

* `--demo`: Automatically fills random answers for testing purposes.
* `--no-ai`: Skips the AI analysis stage if Ollama is not available.
* `--fast`: Reduces the number of questions in each stage for a quicker session.

## 📊 Data & Output

At the end of the session, the system:

1. Displays a **Final Trait Profile** with horizontal bar charts.
2. Presents an **AI Career Insight** powered by Kimi K2 or Llama3.
3. Saves a comprehensive **JSON result file** (e.g., `career_result_20260222_120000.json`) containing timestamps, trait scores, and full ranking data for all three stages.