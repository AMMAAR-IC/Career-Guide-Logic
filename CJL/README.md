# Career Path Assessment System

A CLI-based career assessment engine using:
- **200-question bank** (Aptitude + Big Five + RIASEC)
- **Adaptive quiz** (15–20 questions per session, different every time)
- **Neural-network-style scoring** (weighted dot product → sigmoid → softmax)
- **Ollama + Kimi K2** for AI narrative, roadmap, and insight generation
- **Structured JSON output**

---

## Prerequisites

```bash
pip install requests   # (optional, if you switch from subprocess curl)
```

Ollama must be running locally:
```bash
ollama serve
ollama pull kimi-k2    # or any model you prefer
```

---

## Usage

```bash
# Standard adaptive quiz (15-20 questions, AI reasoning)
python main.py

# Full 200-question assessment
python main.py --full

# Demo mode (random answers, great for testing)
python main.py --demo

# Skip Ollama (pure scoring, no AI text)
python main.py --no-ai

# Combine flags
python main.py --demo --no-ai
```

---

## How the Scoring Works

### Layer 0 — Raw Answers
- **Aptitude**: 1 point per correct MCQ answer
- **Personality (Big Five + RIASEC)**: Likert scale
  - Positive items: SA=+2, A=+1, N=0, D=-1, SD=-2
  - Negative items: reversed

### Layer 1 — Normalisation
- Each section raw score mapped to [0.0, 1.0]
- Neuroticism **inverted** → Emotional Stability trait

### Layer 2 — Trait Vector
```
{ apt, O, C, E, A, stab, R, I, Art }
```

### Layer 3 — Career Cluster Activation (Neural-Net Style)
For each of 15 career clusters:
1. **Weighted dot product** of trait vector × cluster weights
2. **Sigmoid activation** `σ(12(x - 0.5))` — sharp non-linear response
3. **Softmax** across all 15 clusters → probabilities sum to 100%

### Output Example
```json
{
  "profile": {
    "normalised_traits": {
      "aptitude": 0.725,
      "openness": 0.8,
      "conscientiousness": 0.65,
      "extraversion": 0.3,
      "agreeableness": 0.6,
      "emotional_stability": 0.7,
      "realistic": 0.4,
      "investigative": 0.85,
      "artistic": 0.45
    },
    "career_probabilities": {
      "Science / Research": {
        "probability_pct": 22.5,
        "sample_roles": ["Biologist", "Chemist", "Physicist"]
      },
      "STEM / Technology": {
        "probability_pct": 20.1,
        "sample_roles": ["Software Engineer", "Data Scientist"]
      }
    },
    "top_career_cluster": "Science / Research"
  },
  "ai_analysis": {
    "narrative": "...",
    "strengths": ["..."],
    "roadmap": [{ "step": 1, "title": "...", "detail": "...", "timeline": "..." }],
    "key_insight": "..."
  }
}
```

---

## Career Clusters (15 total)
1. STEM / Technology
2. Engineering / Trades
3. Science / Research
4. Creative Arts & Design
5. Business / Management
6. Healthcare / Medicine
7. Social Work / Counseling
8. Education / Academia
9. Law / Policy
10. Finance / Economics
11. Communication / Media
12. Sports / Physical Education
13. Military / Law Enforcement
14. Hospitality / Tourism
15. Environment / Agriculture

---

## Changing the AI Model

In `ai_reasoning.py`, change:
```python
DEFAULT_MODEL = "kimi-k2"  # or "llama3", "mistral", "gemma", etc.
```

---

## File Structure
```
career_assessment/
├── main.py          ← CLI entry point
├── questions.py     ← Full 200-question bank
├── scoring.py       ← Scoring engine + adaptive selector
├── ai_reasoning.py  ← Ollama/Kimi K2 integration
└── README.md
```

Results are saved as `result_YYYYMMDD_HHMMSS.json` in the working directory.
