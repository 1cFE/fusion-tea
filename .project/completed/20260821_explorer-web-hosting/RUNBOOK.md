# Runbook: Deploy & Operate the Concept Explorer on Railway

**Audience:** the repo owner (the manual account/billing/connect steps can't be done by an agent).
**Goal:** a public, always-on URL for the concept explorer that **redeploys automatically on every push to `main`** that passes the deploy gate (see **Deploy gate**).
**Prereq:** the hosting code is on `main` — i.e. branch `feat/explorer-web-hosting` (the `Dockerfile`, `.dockerignore`, `railway.toml`, `requirements-serve.txt`, `scripts/smoke_explorer.py`) has been merged. The two pre-existing startup bugs it depends on are already merged (PR #81 UTF-8 registry, PR #82 `model_setup` path).

Everything Railway needs is already in the repo:
- **`Dockerfile`** — Railway sees this and builds the image with it (it ignores its own auto-builder when a Dockerfile is present).
- **`railway.toml`** — declares the Dockerfile builder, the start command, and restart policy, so you don't have to type those into the Railway UI.
- The start command binds `0.0.0.0` on Railway's injected `$PORT`, single worker. **Don't add `--workers`** — the app keeps state in one process; multiple workers would give inconsistent results.

---

## What "done" looks like

- A URL like `https://<service>.up.railway.app` loads the explorer.
- `scripts/smoke_explorer.py <url>` prints `SMOKE OK`.
- Editing a `data/*.json` value and pushing to `main` updates the live site with no manual deploy step.
- Cost is ~$5/mo (Railway Hobby plan).

---

## One-time setup

### 1. Confirm the code is on `main`
Merge the `feat/explorer-web-hosting` branch first. Railway builds from a branch (you'll point it at `main`), so the artifacts must be there.

### 2. Create a Railway account + project
1. Go to https://railway.com and sign up (GitHub login is easiest — it also makes step 3 smoother).
2. Add a payment method and select the **Hobby plan** (~$5/mo, always-on). The free trial sleeps and has low limits; Hobby is what keeps the URL warm.

### 3. Connect the GitHub repo
1. **New Project → Deploy from GitHub repo.**
2. Authorize Railway for the `1cFE` org if prompted, then pick **`1cFE/fusion-tea`**.
3. When asked which branch to deploy, choose **`main`**.
   - Railway detects the `Dockerfile` and `railway.toml` automatically — you should **not** need to set a build or start command by hand. If the UI shows a build/start command field, leave it empty (railway.toml supplies them) or paste the start command from `railway.toml`.

### 4. First build & deploy
- Railway starts building immediately. The build runs `pip install -r requirements-serve.txt` then copies the repo tree. Expect a few minutes (the jaxlib/scipy install is the slow part; the image is ~1.16 GB — normal for this app, well within Railway limits).
- Watch the **Deploy Logs**. A healthy start ends with uvicorn logging `Application startup complete` and `Uvicorn running on http://0.0.0.0:<port>`.
- If the build or startup fails, see **Troubleshooting** below.

### 5. Make it public (generate a domain)
1. Open the service → **Settings → Networking** (or **Public Networking**).
2. Click **Generate Domain**. Railway gives you `https://<service>.up.railway.app`.
   - If it asks for a port, it's already handled — the app reads `$PORT`, which Railway injects.

### 6. Verify the deploy
From a clone of the repo (any interpreter — the smoke script is standard-library only):
```bash
python scripts/smoke_explorer.py https://<service>.up.railway.app
# expect: SMOKE OK  page/findings=<id>  compute=<id>  lcoe_per_mwh=<number>
```
Then open the URL in a browser and confirm:
- the matrix/pipeline/compare/cost-landscape/concept pages render, and
- dragging a slider on a cost-model concept updates the headline LCOE (this exercises `/api/compute`).

### 7. Confirm auto-redeploy (push-to-main)
1. Edit one value in a committed `exploration/concept_explorer/data/*.json` (e.g. a display field), commit, push to `main`.
2. Watch Railway: a new deployment should start on its own. Once "Wait for CI" is on (see **Deploy gate**), it first waits a few minutes for the `website-contract` workflow's `gate` check, then deploys. There is no manual deploy step.
3. After it goes live, re-run the smoke script (or reload the page) and confirm the changed value is visible.

Once steps 6 and 7 pass, the deployment meets its acceptance criteria.

---

## Operating: bumping `1costingfe` (or any serving dependency)

`1costingfe` is pinned **exactly** (`==0.1.0a2`) because the only PyPI release is a pre-release, and because the numerical output must be reviewed whenever it changes. To move to a new version:

1. Edit the pin in **`requirements-serve.in`** (e.g. `1costingfe==0.1.0aN`).
2. Recompile the fully-pinned lockfile (the `--prerelease=explicit` flag is required — it allows the pre-release **only** for the explicitly-pinned `1costingfe`, keeping numpy/scipy/pydantic on stable releases):
   ```bash
   uv pip compile requirements-serve.in -o requirements-serve.txt --prerelease=explicit
   ```
3. **Review the numbers.** Rebuild and smoke locally before pushing, so a bad bump never reaches the live URL:
   ```bash
   sg docker -c 'docker build -t explorer .'        # or plain `docker build` if your shell is in the docker group
   sg docker -c 'docker run --rm -d --name explorer_check -e PORT=8421 -p 8421:8421 explorer'
   python scripts/smoke_explorer.py http://127.0.0.1:8421
   sg docker -c 'docker rm -f explorer_check'
   ```
   Spot-check that a known concept's LCOE is what you expect (concept 01 baseline ≈ **161.69**).
4. Commit **both** `requirements-serve.in` and `requirements-serve.txt`, push to `main`. Railway rebuilds the image and redeploys automatically. The deploy gate runs on this push too. A new `1costingfe` can change the shape of `/api/compute` responses and fail it; judge such failures as in **Deploy gate**.

The same edit-recompile-review-push loop applies to bumping any of the other serving libs.

---

## Deploy gate

**The point.** The public page `1cf.energy/tools/concepts/` (the *website*, repo `1cFE/website`) runs a frozen copy of the explorer's frontend, taken from one fusion-tea commit (the *pin*). That copy fetches everything from the live API at `concepts.1cf.energy`. So a push to `main` can break the website while `concepts.1cf.energy` keeps working. The deploy gate stops that:

- A GitHub Actions workflow, `website-contract`, runs on every push. Its one job is called `gate`.
- It replays the frozen copy's requests against the pushed code and compares the answers with a recording taken at the pin (`exploration/concept_explorer/website_contract/contract.txt`). It also runs the CORS tests.
- With Railway's "Wait for CI" on, Railway waits for it. If it fails, Railway skips that deploy, and `concepts.1cf.energy` keeps serving the last version that passed.
- A push that passes deploys as before, with no manual step.
- No secrets or tokens are involved. Nothing here needs one.

Decision records: `.project/adr/0011-explorer-deploys-wait-for-website-contract.md` and `.project/adr/0012-website-contract-recorded-from-pin.md`.

### What can hold a deploy

Four kinds of failure. Each has its own fix.

| Kind | What it means | How it clears |
|---|---|---|
| Real break | The push would break the website. | Fix the code or data, and push the fix. |
| False block | The push changed something the frozen copy never reads, or reads safely. | One waiver entry in `waivers.toml`, pushed. See **Clearing a false block**. |
| New concept | The push serves a concept the website has no page for. | Omit it or waive it. See **A new concept**. |
| Infrastructure | The gate couldn't run: a download failed three times, or it ran out of time. | Push again. An empty commit works. |

Replaying fusion-tea's history from April to October 2026 found false blocks in 5 of the 23 explorer changes it could replay, not counting changes that added a concept. None came after 2026-06-15, and each needed at most two waiver lines.

### When a deploy didn't happen

**How it looks.**

- In GitHub, the commit on `main` has a red ✗. Its failing check is `website-contract / gate`.
- In Railway, the deployment for that commit is skipped instead of deployed. *Unconfirmed: the exact wording Railway shows hasn't been seen yet. The owner corrects this line after the first held deploy.*
- `concepts.1cf.energy` still serves the last deploy that passed. Nothing is broken. The new change just isn't live.
- If the failure is in the code or data, every later push to `main` is held too, until it is fixed or waived, because each run checks the whole tree.

**Find out why.**

1. Open the failed run: click the red ✗, then **Details**. Or open the repo's **Actions** tab, then **website-contract**, then the run.
2. Open the log of the step labelled `Run timeout 480 exploration/concept_explorer/website_contract/gate.sh`, and scroll to the end. Ignore the `UserWarning` and `RuntimeWarning` lines from the cost models. They are normal.
3. Look at how far it got. Each stage prints `step <name> <seconds>s`.
   - A step before `gate.sh` failed (checkout or `setup-uv`), or the log ends before `step contract`, or shows `attempt 3 of 3 failed`: infrastructure.
   - The step ended with `exit code 124`, or the job was cancelled at 10 minutes: it ran out of time. Infrastructure.
   - `configuration error in …/waivers.toml`: a waiver the gate can't read. The message names the waiver and what's wrong with it. Fix it and push.
   - `configuration error in …/.dockerignore`: a pattern the gate's matcher doesn't implement, using `?`, `[`, `]`, `\` or a `!` on its own. Rewrite it without those characters and push.
   - Lines starting `FAIL `: the contract check found something. Go to step 4.
   - A Python traceback in the contract step, or a pytest line starting `ERROR`: the server no longer starts or imports. A real break: fix the code.
   - A pytest line `FAILED …/test_cors.py::…`: the CORS allowlist changed. If `https://1cf.energy` lost access, it's a real break. If the allowlist was changed on purpose, ask a developer.
   - A pytest line `FAILED …/test_website_contract.py::…`: the gate's own self-tests failed. If the test name mentions workflows, see **Rules the gate enforces**. Otherwise ask a developer; it is not something a waiver can clear.
4. Read each `FAIL` line. After `FAIL` comes a *failure key*: the rule, then the request, then a field path, a field the website sends, or a concept ID. For example, `FAIL shape GET /api/concepts/{id} .confinement_family` means the concept response's `confinement_family` field no longer has the kind of value the website got at the pin. Under the keys, the gate prints one line per failing rule saying what it means. The rules:

| Rule | Fails when | Can a waiver clear it? |
|---|---|---|
| `status` | a request the website sends gets a different HTTP status than at the pin, such as 404 or 422 | yes |
| `request-field` | a field the website sends in a `POST` body is no longer declared by the server's request model, so the server ignores it. For example, `apply_analyst_overrides` was renamed. | yes, if the server never needed it (see **Clearing a false block**) |
| `shape` | a response field is gone, has a different type, or is null where the pin always sent a value | yes |
| `unpopulated` | a field the pin only ever sent empty or null now carries data | yes, with a cite (below) |
| `enum`, `literal` | a value is outside the set the frozen copy knows, such as a new fit grade | yes |
| `concept-missing` | a concept the website lists is gone from a list the website joins on | yes |
| `concept-unlisted` | a concept the website doesn't list appears where the website builds links | yes |
| `coverage` | a concept lost its findings, its sliders or its analyst-override toggle | yes |
| `cors` | the website's origin, `https://1cf.energy`, may not read a response | **never** |
| `files` | the server reads a file the gate's checkout lacks, or `.dockerignore` keeps out of Railway's image | **never** |

5. Decide which kind of failure it is (the table in **What can hold a deploy**).
   - `concept-unlisted` for a concept you just added: **A new concept**.
   - `cors` or `files`: always fix (see **Clearing a false block**, last part).
   - Anything else: judge it as in **Clearing a false block**. If the website would really break, fix the change.

### Getting a deploy out after the fix

Railway deploys a commit only once that commit's own `gate` run passes.

1. Make the fix: code, data, a waiver or an omit-list line. An infrastructure failure needs no fix.
2. Push it to `main`. The gate also runs on pull requests, so a PR shows the result before you merge.
   - For an infrastructure failure, push an empty commit: `git commit --allow-empty -m "Re-run the deploy gate"`, then `git push`.
3. Wait for the new commit's `gate` check to turn green, a few minutes. Railway then deploys that commit, which includes every change before it.

Re-running the failed run in GitHub ("Re-run jobs") may not make Railway deploy. *Unconfirmed: the owner records here what Railway does after a re-run turns green.* Until then, push a new commit.

### Clearing a false block

A false block is a failure the website can't notice: the push removed or changed something the frozen copy never reads, or reads safely because it checks first.

1. **Check that the website really doesn't depend on it.** The key's last part names the field, such as `.data_grounded` or `.cost_model.cas71`. Search the frozen copy's JavaScript for the field's name. The pin is the `pin` line near the top of `contract.txt`:
   ```bash
   git grep -n "data_grounded" 10f7b9b1f1466d2057a211bf25f09fc35d80a12b -- exploration/concept_explorer/static/js
   ```
   - No hits, or only comments: nothing reads it. A false block.
   - Hits: read each one. If the code checks the value before using it (`!= null`, `if (x)`), a false block. If it would crash or show a wrong value, a real break: fix the change instead.
   - The design's Appendix C lists the fields the frozen copy never reads and the ones that crash it. It is in `design.md` of the `explorer-api-contract-gate` work item, under `.project/active/` (or `.project/completed/` once the item closes).
   - For a `request-field` key, the last word is a field the website sends. It is a false block only if the server never needed it, such as `timestamp`, which the server sets itself. If the server now reads the value under another name, the website's request does nothing: a real break. The exception is a `POST /api/state` field, which is always a false block cleared by a waiver, because neither site reads state back.
   - If you can't tell, don't waive. Ask someone who reads JavaScript, or undo the change.
2. **Add a waiver** at the end of `exploration/concept_explorer/website_contract/waivers.toml`:
   ```toml
   [[waiver]]
   match = "shape GET /api/concepts/{id} .data_grounded"
   reason = "The pinned frontend never reads data_grounded."
   evidence = "unread: data_grounded (git grep at 10f7b9b in exploration/concept_explorer/static/js finds nothing)"
   date = 2026-10-08
   ```
   - `match` is the key exactly as printed after `FAIL `. A `*` stands for one whole word or one whole path segment, so `shape GET /api/concepts/{id} .cost_model.*.cost_m_usd` covers every cost account. A `*` can't stand for the rule (the first word) or for part of a segment (`cas*`).
   - `reason` says why the website doesn't need what changed.
   - `evidence` says where that shows. For an `unpopulated` key it must cite the JavaScript line that reads the field (like `concept_page.js:318`), or say `unread:` followed by what you searched for. The gate rejects it otherwise.
   - `date` is today, written without quotes.
   - All four are required. A malformed entry fails the gate with `configuration error in …/waivers.toml`.
3. **Optional: run the gate locally** to see the key print as `WAIVED`: `exploration/concept_explorer/website_contract/gate.sh`. It needs `uv` and takes about a minute.
4. **Commit `waivers.toml`** with a message saying what you waived and why, and push it (see **Getting a deploy out after the fix**).

**What a waiver costs.**

- It covers that field for every concept until someone deletes it. While it stands, the gate won't catch a real break at that field.
- A waived `unpopulated` field stays unprotected until the next re-pin records it.
- A waiver that no longer matches anything prints `STALE` in the gate's output. Delete it. Re-pinning clears them too.

**`cors` and `files` failures can't be waived.** A waiver for one stops the gate with `configuration error in …/waivers.toml`. Fix them instead:

- `cors <request>`: the website's origin lost access, or a preflight (the browser's `OPTIONS` check before a `POST`) stopped succeeding. Put `https://1cf.energy` back in the allowlist (`_ExplorerApp` in `exploration/concept_explorer/server.py`) and keep `POST` with a `content-type` header allowed.
- `files missing <path>`: the server reads a file outside the directories the gate checks out. Add its directory to `exploration/concept_explorer/website_contract/runtime_paths.txt` and to the "MUST survive" list at the top of `.dockerignore`.
- `files dockerignore <path>`: `.dockerignore` keeps a file the server reads out of Railway's image. Fix `.dockerignore`.

### A new concept

A push that adds a concept the website doesn't list fails the gate with:

```
FAIL concept-unlisted manifest 40
FAIL concept-unlisted parameters/{name} 40
```

The website's frozen pages link to every concept the API lists, and the website has no page for this one. Visitors would follow a dead link. Often there is also a `shape` key for a field the new concept leaves empty. A concept with no row in `exploration/concept_analysis/tables/archetype_fit.csv`, for example, adds `FAIL shape GET /api/manifest .concepts[].fit_grade`.

There are two ways through. Pick by which site matters more until the website adds the concept.

**Option 1: omit it. The website stays whole.**

1. Add a line to `exploration/concept_explorer/omit_list.yaml`: `"40": "Not on the website yet; remove when the website re-pins to a commit that serves it"`.
2. Commit and push. The gate passes. Nothing else is needed.

- Cost: `concepts.1cf.energy` hides the concept too, until the line comes out.
- Bringing it onto both sites later: remove the line on a branch. The website imports that branch's commit, which serves the concept. Then re-pin the gate to the same commit (see **Re-pinning**) and merge the removal and the new contract together. Merge with a merge commit, not a squash or rebase, so the commit the website pinned stays in `main`'s history. Whichever site updates first, the other shows a broken page or a dead link for the concept until the second catches up, so do the two close together.

**Option 2: waive it. The concept shows on `concepts.1cf.energy` now.**

1. Add a waiver for the unlisted keys. The `*` covers both lists:
   ```toml
   [[waiver]]
   match = "concept-unlisted * 40"
   reason = "Concept 40 is new and the website doesn't list it yet. We accept a dead link on the website until it re-pins."
   evidence = "Decided by <name> on <date>. Not omitted because <why it must show on concepts.1cf.energy now>."
   date = 2026-10-08
   ```
2. Add one waiver per `shape` key the new concept caused. For the missing archetype-fit row, this one is checked against the pinned JavaScript:
   ```toml
   [[waiver]]
   match = "shape GET /api/manifest .concepts[].fit_grade"
   reason = "Concept 40 has no archetype-fit row yet, so its fit_grade is null. The pinned pages show no fit marker and group it as unspecified."
   evidence = "index_page.js:157 and matrix_page.js:125 pass it to caveatMarker, which compares it only to \"None\" (caveat_marker.js:53); matrix_data.js:220 groups null as unspecified"
   date = 2026-10-08
   ```
   For any other `shape` key, judge it as in **Clearing a false block**. If you can't show the pinned pages handle the empty field, take option 1 instead.
3. Commit and push.

- Cost: the website's index, matrix and cost-landscape pages, and its parameter cards, link to the concept, and the link leads nowhere until the website re-pins.
- Cost: each `shape` waiver covers that field for every concept. While the `fit_grade` waiver stands, a website concept losing its fit grade in the manifest also passes the gate. The concept response's own `fit_grade` is still checked.
- At the re-pin these waivers print as `STALE`. Delete them then.

### Emergency bypass

Use it only when a deploy must go out now and the gate can't be made green in time. For example: GitHub Actions is down (Railway skips a deploy still waiting after 2 hours), or a real failure will take days to fix and something else is urgent. The cost: whatever goes out is unchecked. If it breaks the website, the website breaks. Only the owner can do this.

1. In Railway, open service `1cfe-fusion-tea-explorer`, then **Settings**. In the source section showing `1cFE/fusion-tea` / `main`, turn **Wait for CI** off.
2. Start a deploy: push a new commit to `main` (an empty commit works). With the setting off, Railway deploys it without waiting.
3. Confirm it's live: `python scripts/smoke_explorer.py https://concepts.1cf.energy` prints `SMOKE OK`.
4. Turn **Wait for CI** back on.
5. Fix or waive the failure on `main` soon. Until the gate is green again, every later push is held.

### Re-pinning when the website re-imports the explorer

Do this whenever the website imports the explorer frontend from a newer fusion-tea commit, or when the daily drift run turns red. Until then, the gate checks pushes against the website's old frontend, so it can miss a break to the new one and can block a change the new one handles. No code reading is needed unless the website's JavaScript changed (step 4).

You need: read access to `1cFE/website`, a full clone of fusion-tea, and `uv`. It takes about two minutes, plus reviewing the diff.

1. In `1cFE/website`, open `src/vendor/concepts/provenance.json`. Copy its `commit`, the full 40-character SHA. Note its `conceptIds` list.
2. In your fusion-tea clone, run `git fetch origin` so the clone has that commit. Make a branch from up-to-date `main`, then run:
   ```bash
   exploration/concept_explorer/website_contract/gate.sh record <full-sha>
   ```
   It takes the pinned commit's files, installs that commit's own dependencies in a throwaway environment, rewrites `contract.txt`, then checks your branch against the new recording.
3. Find the line `concepts 01 02 …` printed after `recorded …/contract.txt from <sha>`. It must list exactly the IDs in `provenance.json`'s `conceptIds`. If it doesn't, stop and ask a developer: the website and its pinned commit disagree about which concepts exist.
4. Recording can refuse, and then writes nothing. Stop in either case:
   - "a developer must re-verify Appendix A", or a list of `fetch(` lines that aren't cited: the website's JavaScript changed, so the list of requests the gate replays may be out of date. A developer compares the request list in `exploration/concept_explorer/website_contract/frontend_requests.py` with the new JavaScript (the design's Appendix A), updates it, and reruns step 2 with `--js-reverified` added at the end.
   - `FAIL files missing …` and "add their directories to runtime_paths.txt": the pinned server reads a directory the gate doesn't take from the pin. Ask a developer.
5. The check at the end of step 2 prints `STALE <match>` for each waiver that matches nothing any more. Delete each one from `waivers.toml`.
6. Run `exploration/concept_explorer/website_contract/gate.sh`. Its summary line should read `website contract (pin <first 9 characters>): 0 failing, 0 waived, 0 stale waivers` (or count only waivers you mean to keep), and its pytest line should show `passed` and no failures. Review `git diff` of `contract.txt`: expect the new `pin` line and lines for whatever the API gained or lost between the old and new pins. Commit `contract.txt` and `waivers.toml`, and merge.

If step 6 shows `FAIL` lines, `main` already serves something the website's new frontend can't use. Treat each one as in **When a deploy didn't happen**.

If step 6's self-tests fail with `test_committed_map_paths_trace_to_appendix_b`, the API at the new pin has a different set of map fields (`dict` fields in the response models). Stop and ask a developer to check the new set and update that test.

### A red drift run

A second workflow, `website-pin-drift`, runs once a day at 15:23 UTC. It reads the pin from `contract.txt` and checks that the website's public concept page links the same fusion-tea commit. It never runs on push, so it never holds a deploy.

- **Green:** the pins match.
- **Passed with a warning:** the website didn't answer, or answered with an error page. Nothing to do. It checks again tomorrow.
- **Red, "the website re-pinned, so re-record the contract":** the website now runs a newer frontend. Re-pin (above).
- **Red, "links no fusion-tea source tree":** the website's page no longer shows a link to its source commit in the form the check expects. Compare `src/vendor/concepts/provenance.json` with the `pin` line of `contract.txt` by hand, and re-pin if they differ. Then ask a developer to update the link pattern (`SOURCE_TREE` in `exploration/concept_explorer/website_contract/drift.py`), or the run stays red every day.

GitHub emails a red scheduled run to the account that last edited the workflow's `schedule` line. GitHub also turns scheduled workflows off after 60 days without activity in the repository. To turn it back on, open the **Actions** tab, then **website-pin-drift**, then **Enable workflow**. **Run workflow** on the same page runs it at any time.

### Turning "Wait for CI" on and off

"Wait for CI" is a Railway setting, and only the owner can change it.

- **On:** in Railway, open service `1cfe-fusion-tea-explorer`, then **Settings**. In the source section showing `1cFE/fusion-tea` / `main`, turn on **Wait for CI**.
- **Off:** the same toggle. Railway then deploys every push to `main` at once, unchecked. Use it only as in **Emergency bypass**.

Railway waits only on workflows that run on push. A failed one skips the deploy. Skipped or neutral runs never block. A deploy still waiting after 2 hours is skipped.

### Owner setup steps

These are for the owner after the deploy gate merges to `main`. None of them needs a secret, token or API key.

1. **Turn on "Wait for CI"** (above), once the `gate` check is green on the merge commit. That way it doesn't hold back the first deploy. Then push an ordinary change and watch Railway wait on `gate`, then deploy. Record here the wording Railway shows for a waiting deploy and, the first time it happens, for a skipped one.
2. **Optional, recommended: require the check on `main`.** In GitHub, open the repo's **Settings**, then a branch rule or ruleset for `main`, and require the status check `gate`. A pull request then can't merge while the gate fails. GitHub also rejects a direct push to `main` from anyone not allowed to bypass the rule, so with it on, fixes, waivers and empty commits go through a pull request.
3. **Optional: watch it fail once.** Push a scratch branch with one deliberate break, for example the `model_type` field renamed in `exploration/concept_explorer/data/04.json`. Its `gate` check should fail, with `FAIL shape GET /api/concepts/{id} .model_type` among its `FAIL` lines. A branch other than `main` never deploys. Delete the branch afterwards.
4. **Optional: add the re-pin to the website's checklist.** In `1cFE/website`'s re-pin checklist (`src/vendor/concepts/README.md`), add one line: "re-pin fusion-tea's deploy gate (fusion-tea RUNBOOK, Deploy gate, Re-pinning)".

### Backing out the deploy gate

The gate changes when Railway deploys, not what it deploys. Merging it adds two workflows, files the server never loads (`exploration/concept_explorer/website_contract/` and one test file) and a comment in `railway.toml`. The server, its data and its frontend are unchanged. So the likely problem is the gate holding a deploy it shouldn't, not the explorer breaking.

Three ways back, cheapest first. Only the owner can do the first two.

1. **Stop the gate holding deploys.** Turn **Wait for CI** off (see **Turning "Wait for CI" on and off**). Railway deploys every push to `main` at once, as it did before the gate. The gate keeps running and showing ✓ or ✗ in GitHub, but holds nothing. Turn the setting back on to undo.
2. **Put the last good version back live.** Use this if `concepts.1cf.energy` is broken after a deploy, whatever caused it. In Railway, open service `1cfe-fusion-tea-explorer`, then **Deployments**. Click the three dots at the end of the last deployment that worked, choose the rollback and confirm. Railway restores that deployment's image and its variables. A deployment older than the plan's retention period has no rollback option. Confirm with `python scripts/smoke_explorer.py https://concepts.1cf.energy`, which should print `SMOKE OK`. A rollback doesn't change `main`, and the next push deploys `main` again, so fix or revert the cause on `main` as well.
3. **Take the gate out of the code.** Turn **Wait for CI** off first and leave it off. After the revert most pushes run no workflow at all, which is how deploys worked before the gate. Then revert the gate's merge on `main`, through a pull request or a push: `git revert -m 1 <merge commit>` if it merged as a merge commit, or `git revert <commit>` if it was squashed. The revert removes the workflows, the gate's code, its docs and ADRs 0011 and 0012, and restores the previous `notify_visualization.yml`. Nothing the explorer or the website serves changes. Record why in a new ADR (`.project/scripts/adr.sh new`), since the revert removes the old ones.

### Rules the gate enforces

- **Never edit `contract.txt` by hand.** It is a recording. The re-pin step is the only way to change it.
- **`cors` and `files` failures are never waived.** Fix them.
- **No workflow that runs on push may be able to fail.** "Wait for CI" waits for every one of them, so any failure skips the deploy. The self-test `test_push_workflows_equal_the_reviewed_list` fails the gate when a push-triggered workflow is added. Before adding the new workflow to the set in that test (`exploration/concept_explorer/tests/test_website_contract.py`), make sure it can't fail, the way `notify_visualization.yml` ends its `curl` with `|| echo "::warning::…"`.
- **The gate must run on every push.** `website-contract.yml` keeps no `paths`, `branches` or `tags` filter, because a skipped run doesn't block a deploy. It also has no `concurrency` cancel, because Railway's handling of a cancelled run is undocumented. A self-test checks the trigger filters.

**What the gate doesn't check.** Numbers such as LCOE values (`scripts/parity_explorer.py` compares those). `concepts.1cf.energy`'s own, newer frontend. A concept losing optional content that another concept already lacked at the pin: the website page shows less but doesn't crash.

---

## Troubleshooting

- **Build fails on `pip install`** — usually a bad/unresolvable pin in `requirements-serve.txt`. Reproduce locally with `docker build`; fix the `.in`, recompile, push.
- **Deploy "succeeds" but the URL 502s / won't load** — the app didn't bind the right port. Confirm the start command uses `--host 0.0.0.0 --port $PORT` (it's in `railway.toml`). Don't hard-code a port.
- **Pages load but a slider drag errors / `/api/compute` 500s** — a runtime file the compute path needs got excluded from the image. Check `.dockerignore` didn't drop `exploration/concept_analysis/analyses/*/model_setup.py`, `scripts/lib/`, or `tables/archetype_fit.csv`. The local `docker run` + smoke catches this before deploy — always smoke locally after editing `.dockerignore`.
- **Findings page shows nothing for some concepts** — those concepts read their analysis from `archive/concept_analysis_pre_rework/<slug>/analysis.md`; make sure `.dockerignore` still keeps that subtree.
- **Push to `main` didn't redeploy** — first look at the commit in GitHub. A red ✗ on its `gate` check means the deploy gate held it: see **Deploy gate → When a deploy didn't happen**. If the check is green, check the service's connected branch is `main` (Settings → the GitHub trigger/branch). Railway redeploys only on pushes to the connected branch.
- **First request is slow after idle** — not expected on Hobby (always-warm). If you ever fall back to a sleeping free tier (HF Spaces / Render free), the first request after sleep re-imports JAX and is slow; that's inherent to those tiers, not a bug.

---

## Notes / decisions of record

- **Public by design.** The service has no auth and serves the full analysis findings (only display names/companies are anonymized). This is intentional.
- **Deploys wait for the deploy gate.** This changes two clauses of hosting FR-6: "without a hand-authored GitHub Actions workflow" no longer holds, and "with no manual deploy step" now holds only for pushes the gate passes. Decision record: `.project/adr/0011-explorer-deploys-wait-for-website-contract.md`; how the contract is recorded: `.project/adr/0012-website-contract-recorded-from-pin.md`.
- **Single worker is load-bearing.** Don't scale to multiple workers/replicas without redesigning state handling.
- **Image size ~1.16 GB** is the CPU-JAX floor (jaxlib + scipy + numpy); the heavy *pipeline* deps (torch/docling/agentic-mbse/sysml-codegen) are excluded. Fine for Railway.
- **Fallback platforms** (documented, not set up): Render uses the same Dockerfile with native push-to-main (`$PORT` injected). Hugging Face Spaces needs the container to listen on 7860 (`app_port: 7860` in the Space README) and deploys by pushing to the **HF** git remote, not GitHub — so GitHub push-to-main does **not** auto-deploy there.
