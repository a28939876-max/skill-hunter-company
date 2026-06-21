# Case 03 - Due diligence: vet a social publishing skill

**The need (verbatim):** "I need a skill or plugin that can help draft and publish
X posts, but I do not want an unknown package touching accounts without a review."

**The old plan:** search for "twitter skill", install the first promising match, and
hope the README's trust claims are current.

**What the firm should check before placement:**

```
$ python3 firm.py vet Xquik-dev/tweetclaw
```

For a social publishing candidate such as
[TweetClaw](https://github.com/Xquik-dev/tweetclaw), the useful background check
is not just "does it exist?" The hiring bar should include:

- **Provenance:** public GitHub source, npm package metadata, OpenClaw install
  surface, and catalog listings should point to the same project.
- **Capability fit:** the package should describe a narrow social workflow, not a
  generic account-control tool.
- **Approval posture:** any posting or account-affecting operation should stay
  approval-gated and documented as such.
- **Release evidence:** if the candidate ships a skill packet, check for
  `SKILL.md`, a skill card, eval or benchmark notes, and a recent SkillSpector
  report.
- **Honest trust status:** do not treat a package as NVIDIA signed or verified
  unless a detached signature such as `skill.oms.sig` and verification
  instructions are present.

**Placement decision:**

TweetClaw is a fit when the team wants an OpenClaw-compatible X workflow with
public provenance and explicit approval boundaries. It is not a fit for fully
autonomous posting, credential extraction, hidden browser control, or claims that
go beyond the public release evidence.

**The lesson:** social skills need a stricter vetting shape than ordinary content
helpers. The firm should verify source, release evidence, and approval boundaries
before it makes the hire.
