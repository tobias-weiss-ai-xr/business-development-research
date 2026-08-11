# Business Development Research — Taxonomy

The corpus classifies every paper into a **20 × 8 taxonomy**: 20 business
development categories × 8 research aspects. This structure powers
saturation tracking, gap analysis and momentum reporting.

---

## Categories (20)

| ID | Category | Focus |
|----|----------|-------|
| `market-analysis` | Market Analysis & Research | Segmentation, sizing, preferences, conjoint/WTP studies |
| `go-to-market` | Go-to-Market Strategy | Market entry, launches, adoption & diffusion, early adopters |
| `sales-strategy` | Sales Strategy & Process | Forecasting, performance, account management, pipelines |
| `b2b-marketing` | B2B Marketing & Lead Gen | Lead generation, funnels, industrial marketing |
| `content-marketing` | Content Marketing & Thought Leadership | Content strategy, authority building, influencer marketing |
| `digital-marketing` | Digital Marketing & SEO | SEO, paid acquisition, social media, advertising effectiveness |
| `brand-building` | Brand & Positioning | Brand equity, loyalty, reputation, word of mouth |
| `customer-acquisition` | Customer Acquisition & Growth | CAC, referrals, free trials, freemium, viral growth |
| `customer-retention` | Customer Retention & Churn | Churn prediction, retention, subscription analytics |
| `customer-success` | Customer Success & Expansion | Satisfaction, NPS, upsell/cross-sell, support automation |
| `pricing-strategy` | Pricing & Monetization | Pricing models, elasticity, dynamic pricing, monetization |
| `product-market-fit` | Product-Market Fit & Validation | Customer development, MVP, user research, validation |
| `business-models` | Business Models & Innovation | Platform economics, network effects, SaaS/subscription models |
| `competitive-intelligence` | Competitive Intelligence | Competitive advantage, positioning, benchmarking |
| `partnerships` | Partnerships & Alliances | Alliances, joint ventures, ecosystems, affiliate channels |
| `sales-psychology` | Sales Psychology & Negotiation | Persuasion, trust, nudging, behavioral economics |
| `networking` | Networking & Relationships | Social capital, weak ties, professional networks, relationship marketing |
| `entrepreneurship` | Entrepreneurship & Small Business | Startups, venture capital, solo operators, SMEs |
| `growth-metrics` | Growth Metrics & Analytics | KPIs, unit economics, LTV, cohort analysis, A/B testing |
| `ai-adoption` | AI Adoption & Transformation | Firm-level AI adoption, AI literacy, EU AI Act, digital transformation |

## Research Aspects (8)

| ID | Aspect |
|----|--------|
| `theory` | Theory — frameworks, models, fundamentals |
| `mechanism` | Mechanism — why/how it works, drivers, dynamics |
| `method` | Method — techniques, processes, playbooks |
| `application` | Application — case studies, practice, deployment |
| `development` | Development — tools, software, implementation |
| `systems` | Systems & Technology — infrastructure, platforms |
| `evaluation` | Evaluation & Benchmarks — measurement, studies, KPIs |
| `review` | Reviews & Surveys — syntheses of the literature |

## Cell Notation

A cell is written `category/subcategory`, e.g. `ai-adoption/application`
(AI adoption case studies) or `pricing-strategy/evaluation`
(pricing effectiveness studies). Gaps and momentum are tracked per cell in
`statistics.json` and `README.md`.

## Paper Format

Every paper in `papers.yaml` carries:

```yaml
- title: "AI adoption in small and medium-sized enterprises"
  date: "2026-03"
  url: https://doi.org/10.xxxx/xxxxx
  category: ai-adoption
  subcategory: application
  authors: ["First Author", "Second Author"]
  abstract: "Short abstract..."
  venue: "Journal of Business Research"
```