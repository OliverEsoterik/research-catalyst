# Academic Augmentation & Review Pipeline

A structured, Human-in-the-Loop (HITL) workflow for augmenting academic manuscripts. This pipeline leverages an autonomous research agent to help you transform a raw draft into a polished, citation-rich, publication-ready paper through a rigorous six-stage process.

## Overview

This project provides the instruction set and directory scaffolding for an AI-assisted academic writing pipeline. It is designed around the principle of **minimal intervention**: the agent refines your voice, sources supporting and challenging literature, and structures your arguments&mdash;but you, the author, remain in control at every step.

The pipeline enforces a **dialectical research** methodology, requiring the agent to find not only supporting evidence but also literature that challenges your premises. This ensures a balanced and academically robust final manuscript.

## Key Principles

-   **Human-in-the-Loop (HITL):** The pipeline pauses at the end of every stage, presenting its work for your explicit review and approval. You must say "APPROVED" for it to proceed.
-   **Dialectical Research:** For every major claim, the agent actively seeks both supporting and challenging literature.
-   **Text Protection:** Any text you mark as `[PROTECTED]` or explicitly ask to be kept is preserved verbatim throughout the entire process.
-   **Minimal Drafting Intervention:** The agent does not invent new arguments. Its role is to refine grammar, improve flow, and integrate your sources.

## The Pipeline

The workflow is divided into six distinct stages, each producing a specific artifact in a structured directory.

```
docs/
└── [research-title]/
    ├── 00_raw_inputs/
    │   └── manuscript.md          # Your starting draft and protected phrases
    ├── 01_analysis/
    │   └── gap_report.md          # Analysis of arguments, gaps, and citations
    ├── 02_literature/
    │   └── dialectical_research.md  # Sourced claims, supports, and challenges
    ├── 03_structure/
    │   └── structural_blueprint.md  # The final paper outline and mapping
    ├── 04_integration/
    │   ├── integrated_draft.md      # Merged manuscript with citations
    │   └── final_manuscript.md      # Copy-edited and polished paper
    └── 05_publish/
        ├── final_manuscript.tex     # LaTeX source for compilation
        └── final_manuscript.pdf     # The final compiled PDF
```

### Stage 1: Ingestion & Gap Analysis
**Input:** `manuscript.md` (your raw draft)  
**Action:** The agent analyzes your manuscript to extract the core vision, identify primary research questions, and find logical gaps or claims lacking sufficient citations.  
**Output:** `01_analysis/gap_report.md`  
**Gate:** You review the `gap_report.md` and provide feedback or approval.

### Stage 2: Dialectical Literature Sourcing
**Input:** Approved `gap_report.md`  
**Action:** The agent conducts targeted literature retrieval. For each identified claim, it finds supporting and challenging evidence, formatted with full bibliographic details.  
**Output:** `02_literature/dialectical_research.md`  
**Gate:** You review the sourced literature, manually deleting irrelevant sources before approving.

### Stage 3: Structural Blueprinting
**Input:** `manuscript.md`, `gap_report.md`, and `dialectical_research.md`  
**Action:** The agent designs an optimal outline for your final paper, mapping your original paragraphs and the sourced literature to specific sections (e.g., Introduction, Literature Review, Discussion).  
**Output:** `03_structure/structural_blueprint.md`  
**Gate:** You review and can rearrange sections within the structural blueprint.

### Stage 4: Manuscript Integration
**Input:** Approved `structural_blueprint.md`  
**Action:** The agent assembles the `integrated_draft.md` by merging your original text with approved citations, following the exact layout of the blueprint. No rewriting occurs; the focus is on building a coherent document flow.  
**Output:** `04_integration/integrated_draft.md`  
**Gate:** You review the integrated draft.

### Stage 5: Light-Touch Polish
**Input:** `integrated_draft.md`  
**Action:** A careful copy-edit is performed to fix syntax, improve transitions, and ensure a cohesive academic tone. The agent avoids synthetic verbosity and ensures the text reads as a single human author.  
**Output:** `04_integration/final_manuscript.md`  
**Gate:** You review the final manuscript for text and tone.

### Stage 6: Typesetting & PDF Compilation
**Input:** `final_manuscript.md`  
**Action:** The manuscript is converted into a well-structured `.tex` file using a provided template and compiled into a professional PDF.  
**Output:** `05_publish/final_manuscript.tex` and `final_manuscript.pdf`  
**Gate:** Pipeline complete. The final PDF is presented to you.

## Getting Started

To use this pipeline, begin by creating your research project's directory structure and placing your raw draft inside it.

1.  **Create your project folder:**
    ```bash
    mkdir -p docs/research-title/00_raw_inputs
    cd docs/my-awesome-research
    ```
2.  **Prepare your manuscript:**
    Write your initial draft in `00_raw_inputs/manuscript.md`. Mark any text you want to protect from rewriting with `[PROTECTED]`.
3.  **Run the Pipeline:**
    Provide the initial manuscript to the PI Agent or run the command associated with the `pi` agent. The agent will take over, executing each stage and pausing for your approval.

## Citation & Bibliography Rules

To maintain academic integrity, the pipeline enforces strict citation protocols:
-   **Immediate Logging:** Every external source used in `gap_report.md` is logged instantly.
-   **Traceability:** Every claim must be traceable to its origin, with exact URLs or hyperlinks for all digital sources.
-   **Consistency:** The final bibliography is formatted into a standard academic style (e.g., APA).

## How It Works

-   The pipeline is driven by the instruction set defined in `INSTRUCTIONS.md`.
-   Each stage halts execution and explicitly asks for your "APPROVED" input to proceed.
-   Text marked with `[PROTECTED]` is carried over verbatim into all subsequent outputs, ensuring your core arguments remain untouched.
-   The tone is strictly managed to avoid common AI artifacts, ensuring the final manuscript reads as a unified, human-authored document.

## Contributing

This is an opinionated workflow designed for rigorous academic augmentation. If you have suggestions for new pipeline stages, improved prompts, or better directory structures, feel free to open an issue or submit a pull request.
