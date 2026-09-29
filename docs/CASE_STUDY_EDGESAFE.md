# Case Study Bridge: EdgeSafe Vision

AI Delivery Doctor was not designed from a blank whiteboard.

One source of its engineering philosophy is the open-source [EdgeSafe Vision](https://github.com/Yazhou-Li/edgesafe-vision) project, which focuses on the last mile of edge-AI delivery:

```text
camera
  → inference/event
  → normalized input
  → rule
  → alarm lifecycle
  → operator feedback
  → acceptance evidence
```

That project exposed a recurring pattern:

- an upstream component can look healthy while the user outcome still fails;
- a running process is not the same as a working workflow;
- a reachable endpoint is not the same as a verified alarm;
- field debugging improves when evidence is collected in chain order.

AI Delivery Doctor generalizes that pattern beyond computer vision.

Its long-term target is any AI application where a team needs to turn:

> "It worked in the demo."

into:

> "These required transitions were actually verified, and this is the first one that was not."
