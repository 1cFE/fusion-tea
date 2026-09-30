# T-003 research worker brief — wave 2 additions

Each wave-2 worker follows the common brief `evidence/briefs/t002-research-common.md` exactly, with the changes below, plus one class section.

## Changes to the common brief

- Your evidence note goes to `work/orchestration/goals/magnet-material-comparison/evidence/sources/<class>.md` with the class name given below.
- **Known registry faults.** `source_registry.py register --url` fails on some PDF URLs with a `UnicodeDecodeError` (and still counts a capture), and it has accepted a bot-check HTML page as a successful capture. Therefore: for a PDF, first download the open copy with `curl -fsSL -o <scratch>/<name>.pdf <url>`, confirm with `file <scratch>/<name>.pdf` that it is a real PDF and open one page to confirm it is the paper, then register with `--local-pdf <scratch>/<name>.pdf`, stating the original URL in `--caveat`. Never register an HTML page that is a captcha, bot check or login wall; record it with `log --failure`. Use your own scratch directory outside the repository.
- Already registered by wave 1 (reuse, do not re-register): Tsui & Hampshire 2012, Lu et al. 2008, Godeke et al. 2006 (Nb₃Sn laws); Demattè & Bruzzone, Sedlak et al. 2020, Takahashi et al. 2010, Breschi et al. 2017 (Nb₃Sn conductors); Molodyk et al. 2021, Senatore et al. 2016, SPARC TFMC program paper (REBCO); Strobridge 1974 (refrigerators); Cooley & Pong 2016 (prices). Grep `knowledge/SOURCE_INDEX.md`.
- Budget about 40 tool calls; return at most 300 words.

## cryo-loads — request `REQ-MMC-CRYO-02`

Evidence note: `evidence/sources/cryo-loads.md`.

1. Register the genuine Green 2015 publisher PDF already on disk: `/tmp/claude-1000/-home-reid-1cfe-fusion-tea/0a548c41-4c93-4118-8650-b762bc653a1a/scratchpad/green2015_iop_publisher.pdf` (SHA-256 `a612649c84d471b10a7cf5e8c01e9ee0a800b2b108f43ad4b5629d34c8587c48`, 9 pages). Use a distinct title such as “Green 2015 cost of coolers at 4.2, 20, 40 and 77 K (publisher PDF)”. In `--caveat`, state that it supersedes the defective registration `knowledge/sources/green_2015_the_cost_of_coolers_for_cooling_superconducting/`, which stored a bot-check page. Then extract and inspect from the rendered pages: the large-refrigerator efficiency law (η = 15.5 R^0.23?), the capital-cost law (C = 3.1 R^0.65 M$2015?), their data domains and the 20 K small-cooler fits, with exact page/figure locations.
2. Find permitted sources for cold-load magnitudes of fusion magnets at 4–5 K: thermal radiation from 80 K shields per unit area, support conduction, nuclear heating, joints. Candidate: Končar et al., EUROfusion WPPMI-CPR(17) 17578, “Heat loads and design temperature optimization of DEMO thermal shields” (scipub.euro-fusion.org).

## cost-common — request `REQ-MMC-COST-02`

Evidence note: `evidence/sources/cost-common.md`.

Register Chislett-McDonald, Surrey, Naish, Turner and Hampshire 2022, arXiv:2205.04441 (use the arXiv PDF via curl and `--local-pdf`). Extract the Nb₃Sn and REBCO prices in USD/kA·m with their stated field, temperature, currency year and scope, their Jc-scaled cost equation, and any cryoplant cost relation with its basis. Note whether its REBCO price is referenced to a temperature other than 4.2 K and whether its sources are independent of PROCESS defaults.

## nb3sn-highfield — request `REQ-MMC-NB3SN-WP-02`

Evidence note: `evidence/sources/nb3sn-highfield.md`.

Register Mitchell et al. 2021, “Superconductors for fusion: a roadmap”, SuST 34 103001 (EPFL Infoscience open manuscript; if the bitstream fails, record the failure). Extract fusion Nb₃Sn TF conductor design points (ITER TF 68 kA / 11.8 T; EU DEMO TF about 83 kA / 13.7 T or others), temperature margin, effective strain, conductor and winding-pack current densities with denominators, plus any statement of the practical Nb₃Sn peak-field limit for fusion TF coils and its basis. Also record any REBCO fusion conductor numbers the roadmap gives, flagged for the rebco class.

## rebco-winding — request `REQ-MMC-REBCO-WP-02`

Evidence note: `evidence/sources/rebco-winding.md`.

Context: the only sourced insulated REBCO winding composition in hand is Stellaris Table 7 (tape stack 9 %, copper jacket 35 %, solder 12 %, steel 36 %, helium 8 %, designed for 24.9 T at 20 K; `knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details/images/page_021_table_0.png`, admissible). The SPARC TFMC is no-insulation. Find a permitted source for an insulated or cable-in-conduit fusion REBCO conductor or winding pack with composition, tape count per conductor, operating current, field, temperature and conductor or winding-pack current density, ideally at 12–20 T near 20 K. Candidates: Bruzzone et al. 2018, “High temperature superconductors for fusion magnets”, Nucl. Fusion 58 103001 (open access); EPFL/SPC HTS DEMO CS or TF conductor papers (Uglietti, Wesche, Bykovsky); VIPER. Record degradation from tape to cable where stated.
