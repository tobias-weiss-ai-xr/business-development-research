# Topic Planner — Example Workflow

This guide walks through turning the corpus into a ki-kompetenz-training.org
article (or an ALaaS offer decision).

## 1. See what's hot

```bash
python3 tools/trend_scanner.py --months 12
```

Example output (illustrative):

```
🔥 TOP KEYWORD BURSTS
ai adoption      12 recent / 30 total  burst=8.2   ################
eu ai act         9 recent / 15 total  burst=6.4   #############
churn             15 recent / 45 total  burst=4.1   ########
```

## 2. Get ranked topics

```bash
python3 tools/topic_planner.py --top 10
```

Writes `docs/topics/ARTICLE_TOPICS.md` with 10 evidence-ranked topics.

## 3. Build a brief

```bash
python3 tools/brief_generator.py "AI adoption in SMEs" --papers 5
```

Output:

```
📝 ARTICLE BRIEF: AI adoption in SMEs
   Category: AI Adoption & Transformation
   Angle: Evidence-based guide to AI adoption in SMEs — synthesize the 5 most
          relevant papers into practical guidance for ki-kompetenz-training.org readers.

Title candidates:
  - AI Adoption in SMEs: What the Research Says
  - AI Literacy as a Service: The Evidence Base for SME Upskilling
  ...

Key papers:
  [2026-02] AI adoption barriers in European SMEs    https://doi.org/...
  [2025-11] The productivity effects of generative AI  https://arxiv.org/abs/...
```

## 4. Write & publish

Publish to the ki-kompetenz-training content pipeline: research → write
(800–1500 words, German or English) → publish on ki-kompetenz-training.org
→ repurpose for the newsletter.

## 5. Use evidence for offer decisions

The same corpus backs offer design: pricing category → ALaaS tier
benchmarks; customer-acquisition → landing page claims; ai-adoption →
the core AI-literacy evidence base.

## 6. Keep the corpus fresh

Weekly CI runs `fetch_new_papers.py --months 1 --create-pr` and opens a PR
with new papers. Review the taxonomy assignments, merge, and the topic list
regenerates automatically.