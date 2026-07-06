<div align="center">

```
███╗   ██╗███████╗██╗  ██╗ █████╗     ███╗   ███╗ █████╗ ██╗  ██╗███████╗███████╗██╗  ██╗
████╗  ██║██╔════╝██║  ██║██╔══██╗    ████╗ ████║██╔══██╗██║  ██║██╔════╝██╔════╝██║  ██║
██╔██╗ ██║█████╗  ███████║███████║    ██╔████╔██║███████║███████║█████╗  ███████╗███████║
██║╚██╗██║██╔══╝  ██╔══██║██╔══██║    ██║╚██╔╝██║██╔══██║██╔══██║██╔══╝  ╚════██║██╔══██║
██║ ╚████║███████╗██║  ██║██║  ██║    ██║ ╚═╝ ██║██║  ██║██║  ██║███████╗███████║██║  ██║
╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝    ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚══════╝╚═╝  ╚═╝
```

<img src="https://readme-typing-svg.herokuapp.com?font=JetBrains+Mono&weight=500&size=20&duration=2600&pause=700&color=C4B5FD&center=true&vCenter=true&width=720&lines=agentic+AI+systems+%2F%2F+LLM+orchestration+%2F%2F+ML+infrastructure;CS+%40+Purdue+%E2%80%94+Machine+Intelligence+track;SWE+Intern+%40+Qualcomm+%E2%80%94+autonomous+crash+triage;I+build+AI+that+does+the+work%2C+not+just+the+talking" alt="headline" />

<br/>

[![Portfolio](https://img.shields.io/badge/PORTFOLIO-mneha05.github.io-1a1a2e?style=for-the-badge&labelColor=8B5CF6)](https://mneha05.github.io)
[![LinkedIn](https://img.shields.io/badge/LINKEDIN-neha--mahesh-1a1a2e?style=for-the-badge&labelColor=0A66C2)](https://linkedin.com/in/neha-mahesh)
[![Email](https://img.shields.io/badge/EMAIL-mahesh54@purdue.edu-1a1a2e?style=for-the-badge&labelColor=EA4335)](mailto:mahesh54@purdue.edu)

</div>

<br/>

## About

**CS junior @ Purdue University** — Machine Intelligence track, Mathematics minor. Currently **SWE Intern @ Qualcomm**, where I architect an autonomous, agentic crash-triage pipeline: an LLM-driven tool-use loop that ingests raw modem crash reports, autonomously resolves build artifacts, retrieves source context, and localizes root cause before a human engineer ever opens the log.

> **The thesis behind everything I build:** LLMs stop being toys and start being infrastructure the moment you give them tools, guardrails, and a reason to act. *I design that layer.*

Off the keyboard: **Project Team Lead @ ML@Purdue** · **Marketing Lead @ Girls Who Code Purdue**

<br/>

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=rect&color=gradient&customColorList=6,11,20&height=3" width="100%"/>

<h2>SELECTED WORK</h2>

</div>

### [PARALLAX](https://github.com/mneha05/parallax) — Multi-Agent Reliability Investigation Platform

> `[ agentic orchestration ] [ multi-agent systems ] [ autonomous investigation ]`

A hierarchical multi-agent system built on the **orchestrator-workers pattern**: a director agent decomposes reliability incidents into a task graph and **fans out to specialized statistical worker agents in parallel**, each operating with an isolated toolset and context. Results fan back in through a **cross-validation layer** that reconciles conflicting findings before synthesis — because a multi-agent system without verification is just N chances to hallucinate. Handles failure isolation per-worker (one agent dying doesn't kill the investigation) and produces structured, evidence-linked root-cause reports. It's the difference between an LLM that *summarizes* an incident and a system that *investigates* one: hypothesis generation, statistical testing, dead-end pruning — autonomously.

`TypeScript` `orchestrator-workers architecture` `parallel task decomposition` `fault isolation` `structured LLM outputs`

---

### [VibeGraph](https://github.com/mneha05/vibegraphv1) — Bidirectional Code-Canvas Workflow IDE

> `[ AI workflow tooling ] [ real-time bidirectional sync ] [ static analysis ]`

An IDE for agentic workflows where **YAML source and a visual DAG are two projections of one canonical state** — edit either, and a **bidirectional reconciliation engine** syncs them in real time without drift or destructive rewrites. The interesting engineering lives underneath: a **custom static analyzer** performs variable scope resolution and data-flow validation across workflow steps, catching broken references *before* execution — compiler techniques applied to workflow definitions. A **step-through simulator** works like a debugger for agent pipelines (breakpoints, state inspection, deterministic replay), and layout is handled by **ELK's layered graph algorithm** for readable auto-arrangement of arbitrary DAGs. Shipped with **33 passing tests** across the sync engine and analyzer, because developer tooling doesn't get to be flaky.

`Next.js` `React Flow` `Monaco` `Zustand` `static analysis` `bidirectional state reconciliation` `DAG layout algorithms`

---

### [Sentinel](https://github.com/mneha05/sentinel) — AI-Driven Sensor Anomaly Workbench

> `[ anomaly detection ] [ AI decision support ] [ real-time telemetry ]`

A multi-channel anomaly triage workbench that ingests **streaming sensor telemetry** and layers AI-driven decision support on top — classifying deviations as noise, drift, or imminent failure, with **cross-channel correlation** to distinguish a failing sensor from a failing system. Designed around a production-reliability truth: **alert fatigue kills monitoring systems faster than missed alerts do.** Every flag ships with its supporting evidence, correlated channels, and a recommended action, keeping the human in the loop *deciding* instead of *deciphering*. Explainability isn't a feature here — it's the architecture.

`TypeScript` `streaming telemetry ingestion` `cross-channel correlation` `explainable AI` `human-in-the-loop systems`

---

### [MERIDIAN](https://github.com/mneha05/meridian) — Zero-Backend Self-Service BI Platform

> `[ analytics infrastructure ] [ in-browser compute ] [ data democratization ]`

A full business-intelligence platform with a deliberately contrarian architecture: **the entire compute layer moved client-side.** An in-browser SQL engine (AlaSQL) executes queries directly over uploaded datasets, and visualization runs on a **charting engine hand-rolled from raw SVG primitives** — no chart library, no rendering dependency, full control over every pixel and every render pass. The result: **zero backend, zero infrastructure cost, zero data leaving the user's machine** — a privacy-preserving analytics loop that collapses upload → query → visualize into a single client-side artifact. Built to interrogate a real systems tradeoff: how much of the modern data stack is architecture, and how much is habit?

`Next.js` `in-browser SQL execution` `custom SVG rendering engine` `client-side compute` `zero-infrastructure design`

---

### [PipelineForge](https://github.com/mneha05/pipelineforge) — Visual Data Pipeline Architect

> `[ dataflow systems ] [ visual programming ] [ pipeline orchestration ]`

A visual environment that models data pipelines as **typed, composable DAGs** — connect stages, trace **data lineage end-to-end**, and validate topology before anything touches production data. The design bet: pipeline failures are overwhelmingly *architecture* failures (implicit dependencies, untracked lineage, silent schema drift), so the tool makes the architecture inspectable first-class — you reason about the graph, not the glue code.

`TypeScript` `Next.js` `DAG modeling` `data lineage` `topology validation`

---

### [GridLens](https://github.com/mneha05/gridlens) — High-Velocity Data Exploration

> `[ interactive analytics ] [ frontend performance engineering ]`

Tabular data exploration engineered around a single latency budget: **interaction must never lag behind thought.** Filtering, slicing, and pattern-hunting across datasets with a front-end architecture tuned for render performance — because the moment an exploratory tool makes the analyst wait, the exploration ends. An exercise in treating **UI latency as a systems problem**, not a styling problem.

`TypeScript` `Next.js` `interaction-latency optimization` `render performance`

---

### [QueryDesk](https://github.com/mneha05/querydesk) — Conversational Analytics Workspace

> `[ natural-language data access ] [ query UX ]`

A workspace built for the pattern every data tool is converging on: **the query interface is a conversation, not a syntax exam.** Ask in natural language, refine iteratively, drill down — collapsing the distance between a question and its answer for users who shouldn't need to know what a LEFT JOIN is to get one.

`TypeScript` `Next.js` `natural-language querying` `iterative refinement UX`

---

### Off-GitHub Builds

```
POSTUREGUARD    Edge-AI wearable running the full inference pipeline on-device:
                MediaPipe pose estimation feeding a custom-trained LSTM on a
                Raspberry Pi, closing the control loop through Arduino haptic
                feedback. Real-time sequence classification under embedded
                compute and memory constraints — no cloud in the loop.

BOILEREXCHANGE  Campus marketplace shipped by a 7-person team: Next.js front-end,
                Django Ninja API, PostgreSQL, Algolia full-text search, and
                Stripe payment infrastructure. Real users, real money, real
                consequences for bad schema decisions.

NEURALDRIVE     Autonomous navigation stack in C++/PyTorch deployed on a Jetson
                Nano — the full perception-to-control loop running on
                GPU-accelerated embedded hardware.

OPEN SOURCE     Active contributions in flight: freeCodeCamp, OpenMRS (global
                open-source EMR platform serving clinics worldwide).
```

<br/>

```
──────────────────────────────  A R S E N A L  ──────────────────────────────
```

<div align="center">

![Python](https://img.shields.io/badge/Python-0d1117?style=for-the-badge&logo=python)
![TypeScript](https://img.shields.io/badge/TypeScript-0d1117?style=for-the-badge&logo=typescript)
![C++](https://img.shields.io/badge/C++-0d1117?style=for-the-badge&logo=cplusplus&logoColor=00599C)
![C](https://img.shields.io/badge/C-0d1117?style=for-the-badge&logo=c&logoColor=A8B9CC)
![R](https://img.shields.io/badge/R-0d1117?style=for-the-badge&logo=r&logoColor=276DC3)

![PyTorch](https://img.shields.io/badge/PyTorch-0d1117?style=for-the-badge&logo=pytorch)
![CUDA](https://img.shields.io/badge/CUDA-0d1117?style=for-the-badge&logo=nvidia&logoColor=76B900)
![LangGraph](https://img.shields.io/badge/LangGraph-0d1117?style=for-the-badge&logo=langchain&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0d1117?style=for-the-badge&logo=fastapi)
![Next.js](https://img.shields.io/badge/Next.js-0d1117?style=for-the-badge&logo=nextdotjs&logoColor=white)
![React](https://img.shields.io/badge/React-0d1117?style=for-the-badge&logo=react)
![Django](https://img.shields.io/badge/Django-0d1117?style=for-the-badge&logo=django&logoColor=092E20)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-0d1117?style=for-the-badge&logo=postgresql)
![Docker](https://img.shields.io/badge/Docker-0d1117?style=for-the-badge&logo=docker)
![Linux](https://img.shields.io/badge/Linux-0d1117?style=for-the-badge&logo=linux&logoColor=FCC624)

**Deep in:** agentic architectures (ReAct, orchestrator-workers, plan-and-execute) · LLM tool-use & function calling · RAG systems · GPU programming · embedded ML

</div>

<br/>

<br/>

```
────────────────────  C O M M I T   H I S T O R Y  ────────────────────
```

<div align="center">

<img src="https://ghchart.rshah.org/8B5CF6/mneha05" alt="contribution graph" width="92%"/>

<br/><br/>

<img src="https://raw.githubusercontent.com/mneha05/mneha05/output/github-contribution-grid-snake-dark.svg" alt="snake eating my contributions" width="92%"/>

<br/><br/>

<img src="https://readme-typing-svg.herokuapp.com?font=JetBrains+Mono&weight=600&size=22&duration=2800&pause=900&color=8B5CF6&center=true&vCenter=true&width=700&lines=building+agents+%3E+building+demos;shipping+%3E+talking;if+you're+building+AI+that+acts+%E2%80%94+let's+talk;mahesh54%40purdue.edu" alt="outro" />

<br/>

[![Say hi](https://img.shields.io/badge/SAY_HI-mahesh54@purdue.edu-8B5CF6?style=for-the-badge)](mailto:mahesh54@purdue.edu)
[![Connect](https://img.shields.io/badge/CONNECT-LinkedIn-0A66C2?style=for-the-badge)](https://linkedin.com/in/neha-mahesh)
[![Explore](https://img.shields.io/badge/EXPLORE-Portfolio-1a1a2e?style=for-the-badge)](https://mneha05.github.io)

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,20&height=160&section=footer&text=see%20you%20in%20the%20commits&fontSize=28&fontColor=fff&animation=twinkling&fontAlignY=72" width="100%"/>

</div>
