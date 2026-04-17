# EEG Meditation App - Lemanich Life Sciences Hackathon 2026

This project is a meditation app prototype built around guided or silent meditation sessions, a small exercise library, and lightweight session analytics. Users can browse built-in and custom meditation exercises, start timed sessions, review past practice, and explore simple per-exercise statistics.

At the moment, the meditation scores are not produced by a real EEG-based assessment system. They are generated arbitrarily as placeholders so the rest of the app flow can be tested and demonstrated. In a future version, these scores would ideally come from a proper model that analyzes EEG and related signals to assess meditation quality more meaningfully.

## Current app flow

- Browse a library of meditation exercises
- Add custom exercises with your own instructions and metadata
- Start a timed meditation session
- Save a session result and short reflection
- Review simple practice statistics and score trends over time

## Setup

Create the environment with:

```bash
conda env create -f environment.yml
```
