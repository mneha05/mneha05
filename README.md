<!-- ============================  HEADER  ============================ -->
<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,20&height=210&section=header&text=Neha%20Mahesh&fontSize=64&fontColor=ffffff&animation=fadeIn&fontAlignY=36&desc=ML%20systems%20%E2%80%A2%20GPU%20kernels%20%E2%80%A2%20AI%20that%20actually%20ships&descSize=18&descAlignY=58" width="100%" alt="Neha Mahesh"/>

<img src="https://readme-typing-svg.demolab.com?font=JetBrains+Mono&weight=500&size=19&duration=2600&pause=800&color=A78BFA&center=true&vCenter=true&width=720&lines=CS+%40+Purdue+%C2%B7+Machine+Intelligence+%2B+Math+minor;ex-SWE+Intern+%40+Qualcomm+%C2%B7+agentic+crash+triage;writing+CUDA+kernels+for+fun+(yes+really);I+build+AI+that+does+the+work%2C+not+just+the+talking" alt="typing intro"/>

<p>
  <a href="https://nehamahesh.netlify.app/"><img src="https://img.shields.io/badge/Portfolio-nehamahesh.netlify.app-8B5CF6?style=for-the-badge&logo=netlify&logoColor=white" alt="Portfolio"/></a>
  <a href="https://www.linkedin.com/in/neha-mahesh-purdue/"><img src="https://img.shields.io/badge/LinkedIn-Neha%20Mahesh-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn"/></a>
  <a href="mailto:mahesh54@purdue.edu"><img src="https://img.shields.io/badge/Email-mahesh54%40purdue.edu-EA4335?style=for-the-badge&logo=gmail&logoColor=white" alt="Email"/></a>
</p>

<img src="https://komarev.com/ghpvc/?username=mneha05&label=profile%20visits&color=8B5CF6&style=flat-square" alt="profile visits"/>

</div>

<br/>

<!-- ============================  WHOAMI  ============================ -->

```python
class Neha:
    school    = "Purdue University · CS (Machine Intelligence) · Math minor · class of 2028"
    was       = "SWE Intern @ Qualcomm · modem/OOB software · LLM-driven crash triage"
    leads     = ["Project Lead @ ML@Purdue", "Marketing Lead @ Girls Who Code Purdue"]
    wins      = ["🥇 HackMIT", "🥈 InnovateHer"]
    obsessed  = ["paged attention", "inference serving", "compilers", "agents with guardrails"]
    fun_fact  = "taught Scratch to kids and CUDA to myself, same semester energy"

    def thesis(self):
        return "LLMs become infrastructure the moment you give them tools, guardrails, and a reason to act."
```

<!-- ============================  NOW  ============================ -->

<table>
<tr>
<td width="50%" valign="top">

**🔭 Right now**
- Making attention kernels fast on GPUs ([hetero-serve](https://github.com/mneha05/hetero-serve), [attnc](https://github.com/mneha05/attnc))
- Open source PRs in flight: **Cloudflare quiche**, **NVIDIA cudf / Spark**, **Hugging Face**
- Merged into **OpenMRS** 🎉

</td>
<td width="50%" valign="top">

**💬 Ask me about**
- Why `block_size = 16` was secretly the right answer
- Recompute vs. migrate a KV cache (it depends on your network!)
- Why the noise traders in Figgie win more pots and still go broke

</td>
</tr>
</table>

<div align="center">
<img src="https://capsule-render.vercel.app/api?type=rect&color=gradient&customColorList=6,11,20&height=3" width="100%"/>

## ⚡ Flagship builds
</div>

### 🧠 [hetero-serve](https://github.com/mneha05/hetero-serve) · KV-cache-aware LLM serving + CUDA paged-attention kernels

<p align="center">
  <img src="https://raw.githubusercontent.com/mneha05/hetero-serve/main/docs/hero.gif" width="92%" alt="hetero-serve: a shared prefix fills on one accelerator, a second request reuses it, then the cached KV crosses the interconnect to a second GPU"/>
  <br/>
  <sub>a prefix fills, the next request <i>reuses</i> it, then the cache crosses the interconnect &nbsp;·&nbsp; <a href="https://mneha05.github.io/hetero-serve/">▶ drive it in your browser</a> &nbsp;·&nbsp; <a href="https://colab.research.google.com/github/mneha05/hetero-serve/blob/main/notebooks/verify_cuda_kernel.ipynb">▶ compile the kernels on free Colab</a></sub>
</p>

A serving system that answers one question: when a request's KV cache already exists **on the wrong accelerator**, should you wait, recompute, or move it?

| | |
|---|---|
| 🚀 **55.4%** of Tesla T4 peak memory bandwidth | up from 13.4%, **10 to 22× PyTorch SDPA** on paged data |
| ⏱️ **p50 3.60 s → 1.94 s** | cache-aware routing: highest hit rate *and* spread load |
| 🧩 **5 hand-written CUDA kernels** | fused gather, online softmax, context split, prefill, tensor-core WMMA |
| ✅ **101 tests, zero mocks** | real processes, real sockets, kernels fuzzed against a NumPy oracle |

<details>
<summary><b>📖 the full engineering story (it's a good one)</b></summary>
<br/>

The core is a **paged KV cache** (16-token blocks, refcounts, chain-hashed prefix sharing, LRU eviction), **continuous batching** with chunked prefill and recompute-preemption, and a router whose cost model prices *stay* vs *migrate* in seconds using per-device speeds it **measures at startup rather than assumes**. Workers are real OS processes over real TCP through a token-bucket shaper, so transfers genuinely contend: at 50 Mbps moving an 18.9 MB prefix loses to recomputing it, at 10 Gbps it wins.

Then profiling said a third of every decode step wasn't accelerator time at all. It was the host gathering KV blocks into contiguous tensors. So I wrote the kernel that deletes it, then three more. **v1** fuses the gather away. **v2** adds FlashAttention-style online softmax. **Nsight** showed v2 was *occupancy*-starved (0.1 waves across 40 SMs), which produced **v3**, a context split that took it from 13.4% to 55.4% of peak bandwidth. Sweeping the split count caught my own heuristic being wrong: it picked 2 where 32 was 2.1× faster, because online softmax is *sequential* and splitting shortens a dependent chain, not a wave count. A 16-token KV page is exactly one 16×16×16 WMMA fragment, which is why the tensor-core version fits so cleanly.

GQA is supported throughout and it moves the scheduler's answer: Llama-3's 4:1 ratio drops the migration crossover from **503 Mbps to 126 Mbps**, from datacenter fabric to commodity networking.

Five bugs are documented in the repo, each found by measuring rather than reading. My favorite: I was *confident* one was a serialization-layout problem, benchmarked first, and was wrong. Profile before optimizing applies to your own hypotheses too.

<p align="center"><img src="https://raw.githubusercontent.com/mneha05/hetero-serve/main/docs/architecture.png" width="92%" alt="hetero-serve architecture"/></p>
</details>

`CUDA` `C++` `WMMA` `Nsight Compute` `PyTorch` `FlashAttention` `GQA` `NCCL` `asyncio` `OpenVINO` `Docker`

---

### 🛠️ [attnc](https://github.com/mneha05/attnc) · a tiny compiler that writes fused CUDA attention for you

<p align="center">
  <a href="https://mneha05.github.io/attnc/"><img src="https://raw.githubusercontent.com/mneha05/attnc/main/docs/assets/attnc-demo.gif" width="92%" alt="attnc playground composing attention variants into IR and fused CUDA"/></a>
  <br/>
  <sub>compose a variant, watch the DSL, IR, CUDA, and tile plan change together &nbsp;·&nbsp; <a href="https://mneha05.github.io/attnc/">▶ try the playground</a></sub>
</p>

Hand-tuned attention kernels are fast and rigid. **attnc** treats causal masks, sliding windows, GQA, softcaps, and ALiBi as a *program*: Python DSL → shared IR → passes that classify tiles as skipped / fast / predicated → NVRTC emits **one fused online-softmax kernel**. Correctness is anchored by **160 randomized differential tests** against an independent NumPy interpreter.

`Python` `CUDA` `NVRTC` `IR passes` `symbolic tracing` `compiler design`

---

### 🃏 [Figment](https://github.com/mneha05/figment) · self-play market-making arena for Jane Street's Figgie

<p align="center">
  <img src="https://raw.githubusercontent.com/mneha05/figment/main/assets/replay.gif" width="88%" alt="Figment: one Figgie round replayed with prices, Bayesian belief, and P&L"/>
</p>

A from-scratch **continuous double auction** (4 order books, price-time priority) plus a **Bayesian market maker** that infers the hidden goal suit with an exact multivariate-hypergeometric posterior and quotes **Avellaneda–Stoikov style**. Evolutionary self-play grew a timid bot from **+$6 to +$37 per game** in 14 generations. Best result: noise traders *win the pot more often* yet *lose money every game*. **Edge ≠ outcome.** 15 tests prove the market never creates or destroys a card or a dollar.

`Python` `NumPy` `Bayesian inference` `market microstructure` `evolutionary optimization` `Elo`

<!-- ============================  MORE  ============================ -->

<div align="center">
<img src="https://capsule-render.vercel.app/api?type=rect&color=gradient&customColorList=6,11,20&height=3" width="100%"/>

## 🧪 More from the lab
</div>

<table>
<tr>
<td width="50%" valign="top">
<h4>📊 <a href="https://github.com/mneha05/mneha05/tree/main/productpulse">ProductPulse</a></h4>
Airflow → Iceberg → Trino → dbt analytics stack computing DAU/MAU, funnels, D1/D7 retention, and A/B conversion, with a Python metric oracle checking dbt's math.<br/><br/>
<code>dbt</code> <code>Trino</code> <code>Airflow</code> <code>Iceberg</code>
</td>
<td width="50%" valign="top">
<h4>📺 <a href="https://github.com/mneha05/mneha05/tree/main/media-systems-lab">Media Systems Lab</a></h4>
The plumbing behind ad-supported streaming: AVOD decisioning with pacing and frequency caps, VAST parsing, SSAI splicing into HLS, ABR, an LRU CDN edge sim, and an MMR-reranked recommender. 17 tests.<br/><br/>
<code>HLS/DASH</code> <code>FFmpeg</code> <code>VAST</code> <code>RecSys</code>
</td>
</tr>
<tr>
<td valign="top">
<h4>🕵️ <a href="https://github.com/mneha05/parallax">PARALLAX</a></h4>
Multi-agent reliability investigator: a director agent fans incidents out to parallel statistical workers, then a cross-validation layer reconciles their findings. Because N agents without verification is N chances to hallucinate.<br/><br/>
<code>TypeScript</code> <code>orchestrator-workers</code> <code>fault isolation</code>
</td>
<td valign="top">
<h4>🔀 <a href="https://github.com/mneha05/vibegraphv1">VibeGraph</a></h4>
Workflow IDE where YAML and a visual DAG are two views of one state, synced both ways. Custom static analyzer catches broken references before runtime, plus a step-through debugger for agent pipelines. 33 tests.<br/><br/>
<code>Next.js</code> <code>React Flow</code> <code>Monaco</code> <code>ELK</code>
</td>
</tr>
<tr>
<td valign="top">
<h4>🛡️ <a href="https://github.com/mneha05/aegismesh-rs">AegisMesh</a></h4>
3-replica Rust service with quorum writes, WAL persistence, failover routing, replica catch-up, and a 3-node chaos test in green CI.<br/><br/>
<code>Rust</code> <code>replication</code> <code>chaos testing</code>
</td>
<td valign="top">
<h4>🦾 <a href="https://github.com/mneha05/flowctrl-lab">FlowCtrl Lab</a></h4>
NumPy-only showdown of behavior cloning vs. diffusion policy vs. flow matching on a simulated manipulation task with bimodal demos.<br/><br/>
<code>imitation learning</code> <code>diffusion</code> <code>flow matching</code>
</td>
</tr>
<tr>
<td valign="top">
<h4>📡 <a href="https://github.com/mneha05/sentinel">Sentinel</a></h4>
Sensor anomaly workbench that sorts deviations into noise, drift, or imminent failure, and ships every alert with its evidence. Built against alert fatigue.<br/><br/>
<code>TypeScript</code> <code>telemetry</code> <code>explainable AI</code>
</td>
<td valign="top">
<h4>📈 <a href="https://github.com/mneha05/meridian">MERIDIAN</a></h4>
Zero-backend BI: in-browser SQL plus a charting engine hand-rolled from raw SVG. Zero infra cost, zero data leaves your machine.<br/><br/>
<code>Next.js</code> <code>AlaSQL</code> <code>custom SVG</code>
</td>
</tr>
</table>

<details>
<summary><b>➕ even more (PipelineForge · GridLens · QueryDesk)</b></summary>
<br/>

- **[PipelineForge](https://github.com/mneha05/pipelineforge)** · data pipelines as typed, composable DAGs with end-to-end lineage and topology validation
- **[GridLens](https://github.com/mneha05/gridlens)** · tabular exploration built around one rule: interaction never lags behind thought
- **[QueryDesk](https://github.com/mneha05/querydesk)** · conversational analytics, because nobody should need a LEFT JOIN to get an answer
</details>

<!-- ============================  HARDWARE  ============================ -->

```
┌─ off-github builds ───────────────────────────────────────────────────────┐
│  POSTUREGUARD    edge-AI wearable · MediaPipe → LSTM on a Raspberry Pi    │
│                  → Arduino haptics · no cloud in the loop                 │
│  NEURALDRIVE     autonomous nav in C++/PyTorch on a Jetson Nano           │
│  BOILEREXCHANGE  campus marketplace, 7-person team · Next.js, Django      │
│                  Ninja, Postgres, Algolia, Stripe · real users, real $    │
└───────────────────────────────────────────────────────────────────────────┘
```

<!-- ============================  STACK  ============================ -->

<div align="center">

## 🧰 Toolbox

<img src="https://skillicons.dev/icons?i=py,cpp,c,ts,rust,go,r&theme=dark" alt="languages"/>
<br/>
<img src="https://skillicons.dev/icons?i=pytorch,tensorflow,fastapi,nextjs,react,django&theme=dark" alt="frameworks"/>
<br/>
<img src="https://skillicons.dev/icons?i=postgres,docker,kubernetes,linux,gcp,azure,aws&theme=dark" alt="infra"/>
<br/>
<img src="https://img.shields.io/badge/CUDA-76B900?style=for-the-badge&logo=nvidia&logoColor=white" alt="CUDA"/>
<img src="https://img.shields.io/badge/Nsight-76B900?style=for-the-badge&logo=nvidia&logoColor=white" alt="Nsight"/>
<img src="https://img.shields.io/badge/LangGraph-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white" alt="LangGraph"/>
<img src="https://img.shields.io/badge/dbt-FF694B?style=for-the-badge&logo=dbt&logoColor=white" alt="dbt"/>

<sub><b>deep in:</b> agent architectures · tool use & function calling · RAG · GPU programming · embedded ML</sub>

</div>

<!-- ============================  ACTIVITY  ============================ -->

<div align="center">

## 🐍 Commit history

<img src="https://ghchart.rshah.org/8B5CF6/mneha05" alt="contribution graph" width="92%"/>
<br/><br/>
<img src="https://raw.githubusercontent.com/mneha05/mneha05/output/github-contribution-grid-snake-dark.svg" alt="snake eating my contributions" width="92%"/>

<br/><br/>

<img src="https://readme-typing-svg.demolab.com?font=JetBrains+Mono&weight=600&size=20&duration=2800&pause=900&color=8B5CF6&center=true&vCenter=true&width=700&lines=profile+before+you+optimize;shipping+%3E+talking;building+AI+that+acts%3F+let's+talk+%F0%9F%91%8B" alt="outro"/>

<br/>

<a href="mailto:mahesh54@purdue.edu"><img src="https://img.shields.io/badge/Say_hi-mahesh54%40purdue.edu-8B5CF6?style=for-the-badge&logo=gmail&logoColor=white" alt="email"/></a>
<a href="https://www.linkedin.com/in/neha-mahesh-purdue/"><img src="https://img.shields.io/badge/Connect-LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn"/></a>
<a href="https://nehamahesh.netlify.app/"><img src="https://img.shields.io/badge/Explore-Portfolio-1a1a2e?style=for-the-badge&logo=netlify&logoColor=white" alt="Portfolio"/></a>

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,20&height=150&section=footer&text=see%20you%20in%20the%20commits%20%E2%9C%A8&fontSize=26&fontColor=ffffff&animation=twinkling&fontAlignY=70" width="100%"/>

</div>
