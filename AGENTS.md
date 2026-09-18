# Repository Instructions

## Role

This repository is the authoritative editable source for the `three-space-development` skill.
It defines Problem → Intention → Specification → Solution Architecture and owns the SDD Handoff Contract.

`sdd-development` consumes the contract; it does not redefine the upstream specification.

## Source and runtime

- Edit this source repository only.
- The copy under the Codex user skills directory is an installed runtime artifact.
- Never use an installed runtime copy as the source of truth.
- Do not treat a project-local legacy copy as an active source.

## GitHub workflow

- Work from a non-`main` branch.
- Open a pull request for every change.
- Do not push directly to `main` or force-push it.
- Run the repository quality checks before requesting merge.
- Contract changes must state the contract version and the compatibility impact on `sdd-development`.
- Use Squash Merge after the required checks pass.

## Verification

Run the following from the repository root:

```text
python -m compileall -q scripts
python scripts/validate_specification_package.py templates/specification-package.md --template
python scripts/validate_public_surface.py
```

## Versioning

- Patch: wording, examples, or non-semantic corrections;
- Minor: compatible fields or behavior;
- Major: removed fields, changed semantics, or changed handoff flow.

After merge, tag the source commit before synchronizing the runtime copy.
