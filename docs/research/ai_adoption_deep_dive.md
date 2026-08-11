# AI Adoption — Evidence Base Deep-Dive

**Corpus category:** `ai-adoption` — the core evidence base for the
KI-Kompetenz-Training ALaaS (AI Literacy as a Service) offer.

---

## Why This Category Matters

AI adoption research answers the questions KI-Kompetenz-Training sells
against: *do companies that adopt AI actually get more productive, and what
separates successful adopters from failures?* This is the academic
underpinning of the ALaaS value proposition — evidence that AI literacy
training (not just tool access) drives measurable outcomes.

## Key Research Threads

### 1. Firm-Level Productivity Effects

Econometric studies on AI adoption show heterogeneous returns: firms that
pair AI tools with complementary organizational change (skills, processes,
management) capture multiples of the gains of tool-only adopters. The effect
is strongest for:

- **Task augmentation** — AI assists skilled workers more than it replaces them
- **Complementary upskilling** — adoption ROI scales with literacy investment
- **Reorganization** — process redesign matters as much as the model choice

### 2. Barriers to Adoption (SME Focus)

Survey evidence across European SMEs consistently ranks:

| Barrier | Frequency | Implication for ALaaS |
|---------|-----------|----------------------|
| Missing skills / AI literacy | Highest | Core offer: training as the unlock |
| Regulatory uncertainty (EU AI Act) | High | Offer: compliance-aware literacy paths |
| Cost / unclear ROI | High | Offer: use-case-first training, not theory |
| Data quality & infrastructure | Medium | Offer: audit + training combo |

### 3. The EU AI Act Compliance Pressure

The EU AI Act creates a concrete, date-bound demand for AI competence:
organizations deploying AI systems must ensure staff have sufficient
AI literacy. This is the regulatory tailwind behind ALaaS — compliance
deadlines convert "nice-to-have training" into "must-have".

### 4. AI Literacy as a Construct

Educational research distinguishes **conceptual**, **practical** and
**critical** AI literacy. Training effects decay without practice; the most
robust interventions combine:

- Conceptual grounding (how AI works, limits, risks)
- Hands-on use cases (business-relevant, not toy tasks)
- Critical evaluation (output verification, hallucination awareness)

## What the Corpus Adds

- Moment-by-moment velocity of AI-adoption papers (published monthly)
- The surge of generative-AI productivity studies (post-2024)
- SME-specific subcorpora (`ai-adoption/application`, `ai-adoption/mechanism`)
- Gap analysis: few papers cover *training-as-a-service* delivery models —
  white space for thought leadership

## How to Use This Evidence

1. **Blog/content:** cite firm-level studies in landing-page claims
   ("companies that train their teams on AI report X")
2. **Offer design:** align tier structure with the literacy taxonomy
   (conceptual → practical → critical)
3. **Sales conversation:** use adoption-barrier data to open conversations
   with skeptical SME decision-makers
4. **Positioning:** EU AI Act literacy deadlines as the urgency driver

## Key Corpus Queries

```bash
python3 tools/trend_scanner.py --months 12 --json | python3 -c "import json,sys; d=json.load(sys.stdin); print([t for t in d['trends'] if 'ai' in t['keyword'] or 'literacy' in t['keyword']])"
python3 tools/brief_generator.py "EU AI Act literacy requirements" --papers 5
```

Regenerate trend views with:

```bash
python3 scripts/analysis/generate_analysis.py
python3 tools/trend_scanner.py --months 12
```