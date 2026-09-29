# Security Policy

AI Delivery Doctor intentionally interacts with deployment environments, so privacy and scope boundaries are part of the product.

## Reporting a vulnerability

Please do not publish exploit-ready details, credentials, tokens, private keys, private endpoints, customer identifiers, or production logs in a public issue.

When reporting a security concern:

- remove secret values;
- replace private hosts with documentation-safe examples;
- minimize logs to the lines needed to reproduce the issue;
- describe whether the issue affects local output, shareable evidence, network probes, or contract parsing.

For ordinary non-sensitive bugs, use GitHub Issues.

## Security model

The v0.1 core:

- does **not** execute arbitrary shell commands from contracts;
- never prints environment-variable values;
- strips URL credentials, query strings, and fragments from HTTP labels;
- offers an explicit `--shareable` mode to further minimize operator-supplied details;
- performs read-only probes;
- does not upload evidence.

## Network probes

TCP/HTTP checks can still contact operator-supplied targets. Only probe systems you are authorized to test.

A successful network probe proves only the bounded observation documented by that check.
