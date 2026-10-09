Answers to your three questions. All are orchestrator decisions (agent-grade), made under the owner's go-ahead for the run. Record them in the design as such, not as owner decisions.

## 1. New concepts: Option A (block by default, a one-line waiver clears it)

Accepted. I checked `matrix_page.js:122` at the pin: it links `"/concept/" + row.concept_id` for every manifest row, so an unlisted concept is a dead link on the website. Spec criterion 2's "a new concept the website doesn't list yet" passes was the spec author's inference, and your evidence overturns it. The orchestrator will amend criterion 2 and the spec's "New concepts" open question after your design lands, and flag the change to the owner. Design against the amended version: a new served concept not in the website's list fails the gate unless a waiver names it with a reason. The waiver goes stale at the next re-pin and is deleted then.

## 2. A recorded contract instead of a hand list: accepted, with four conditions

Your reasoning holds: the frontend can only read what the pinned server sent, so a recording can't miss a read. The conditions:

1. **The contract is a pure function of the pin SHA.** Re-recording reads the pinned commit only, so it can never clear a block. Keep that property explicit and tested.
2. **Readable and diffable.** The committed recording is normalized and sorted (one field path per line, or similar), with a header naming the pin SHA and how to regenerate it. A reviewer can see what a re-pin changed.
3. **Maps aren't records.** Some response objects are maps with data-driven keys, such as parameter names, CAS accounts or concept IDs, rather than fixed-field records. If the recording treats every key as a required field, ordinary model work (a parameter renamed, a CAS account added) will trip the gate and bury it in waivers. Record a map by the shape of its values, not its key set, unless the pinned JS reads a specific key; cite the line where it does. Say in the design how a path is classified as map or record, and how a reviewer checks that.
4. **Measure the false-block rate before building on it.** There are 29 commits touching `exploration/concept_explorer/data/` since 2026-04-01. Implementation's first phase replays the recorder's comparison across that history. For each data change that would trip the gate, it checks whether the pinned JS would actually break. If ordinary regenerations trip it often, revisit the map/record split before building the rest. Put this in the design as the de-risking step and say what result would send it back.

## 3. Tooling and the image question

Facts I checked:

- **Docker isn't available to any agent in this run.** User `reid` isn't in the `docker` group (`/var/run/docker.sock` is `root:docker 0660`), and there's no podman. `bypassPermissions` doesn't change that. Changing it is the owner's call, and I'm not asking for it.
- **Python is available in implementation.** The implement stage runs with `bypassPermissions`. It can build a serving-set venv in a scratch directory (`uv venv <dir>` plus `uv pip install --python <dir> -r requirements-serve.txt`) and measure timings there.
- **The repo tracks 5.6 GB at HEAD** (`git ls-tree -r -l HEAD`), mostly `exploration/` 3.5 GB and `work/` 1.1 GB. A default `actions/checkout` downloads all of it on every push, and `Dockerfile:24` (`COPY . .`) puts all of it into the image. That cost hits the 5-minute budget whether or not the gate builds an image.

Decision rule: **prefer a gate whose every part the implementing agent can run and verify locally** over one that can only be verified after an owner push. So:

- Don't make a Docker image build the gate's main mechanism. Run the contract against the server started from the checkout, in the serving dependency set, the same way locally and in CI.
- Limit what CI checks out to what the server reads at runtime (sparse checkout or similar), and show how that set is derived and kept correct. If a path the server reads is missing from it, the gate must fail loudly, not pass on missing data.
- Treat `.dockerignore` breaks as a separate, cheap check. One option: record which files the server opens during the contract run and assert none is excluded by `.dockerignore`, using a matcher with Docker's semantics. Weigh that against recording `.dockerignore` breaks as out of scope with the reason. Pick one and justify it.
- The 5-minute budget: give an estimate that includes checkout. Implementation measures the local parts. Timing on a GitHub-hosted runner becomes an owner acceptance step after the owner pushes. Say so in the design; the orchestrator will move it in the spec.

## Also

- The 5.6 GB build context and image is a real finding. Put one line in the design's out-of-scope notes. The orchestrator will add a backlog row.
- Keep the main body near the command's ~300-line target. Put the field inventory and the fetch-site list in an appendix if you need them.

Now write the design.
