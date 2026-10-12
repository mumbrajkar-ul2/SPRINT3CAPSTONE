Q: assuming we never had a semantic layer built for accompanying the PRD and we solely relied on the .md files that were generated across all the previous stages, would the model not be able to generate the same output that it would with the semantic layer?

CURSOR:

The model could probably still build something. It would not build the same thing, and you could not show why. The semantic layer adds no facts that the Markdown files lack. Each YAML item cites its design file in a `source:` list. So the layer is a cleaned-up copy of the Markdown, not new information. The cleaning is what matters.

**What the Markdown files do not give a model**

1. **There is too much of it, and some of it is out of date.** `docs/03-identity/` through `docs/14-audit/` hold well over 60 files, and many are long. They record history as well as current rules. Some are superseded:
   - `target-access-matrix.md` says 34 rows. The policy now has 35.
   - The first S04-07 run says `httpx` is in no requirements file. That was fixed later.
   - `access-semantics.yaml` still says admin is allowed every action.

   A person reading them knows which sentence won. A model has to guess.

2. **The terms have no fixed names.** In Markdown, the same idea appears as "audit read", "audit-read row", `resource.audit_log`, and "the audit route". The YAML gives each one a single id, such as `rule.shared_admin_not_least_privilege`. When two models read prose, they can pick different words for one idea. Then you cannot tell a real difference from a naming difference.

3. **The label on a claim is easy to miss.** Files mark text as Verified Fact, Inference, Assumption, Unknown, or PROPOSED. Those labels sit inside sentences. In the YAML they are fields (`proposed: true`, `owner:`). A model reading prose can treat an Unknown as settled.

4. **The files describe how the first app solved the problems.** The evidence files quote code, test names and fixes. S08 forbids the brief from mentioning how the first app solved anything (line 26). If you attach those files, the second model copies the first app. The comparison then measures copying.

5. **Nothing checks the model's output against the meaning.**
   - `semantic-layer/tests` has 35 tests.
   - `build.py` validates the schema.
   - S08 counts any status word not in `status-taxonomy.yaml` as drift.

   With Markdown there is no list of allowed words, so drift cannot be counted.

6. **You cannot prove both models got the same input.** S08 records a SHA-256 hash of every file under `semantic-layer/` before and after the run. Dozens of Markdown files that keep changing, with evidence files rewritten on each run, do not give a fixed input to hash.

**What would still work**

- A strong model reading all the files could build a working app with similar routes and the same four AI outcomes. Much of the content is clear.
- The risk is in the details: ids, status words, which source is current, and open questions. These are the places where S08 looks for drift.

**What this means for the project**

The challenge guide asks whether the meaning survives a change of model. If you hand over the Markdown pile, the answer to that question is muddy. If the second app differs, you cannot tell whether the model drifted, whether the files contradicted each other, or whether the model copied the first app. The semantic layer removes those three causes. That is why S05R moves each meaning into the YAML before S08 freezes it.

This is a reasoned explanation. The project has not run a Markdown-only test, so how much worse it would be is Unknown.

I'm in Ask mode, so I did not add this turn to `transcript/chat_transcript.md`.