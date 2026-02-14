# 🎮 Provably Fair Crash Game (Aviator-style)

A web-based crash game inspired by Aviator, built using **Python (Flask)**,  
featuring **provably fair RNG**, **animated multiplier**, and **betting system**.

This project demonstrates understanding of:
- Game backend logic
- RNG & fairness systems
- Frontend animation
- QA / game testing concepts

---

## 🚀 Features

- Provably Fair crash algorithm using SHA256
- Server seed commitment & nonce-based rounds
- Real-time animated multiplier (JavaScript)
- Betting & balance management
- Win / loss calculation
- Casino-style dark UI

---

## 🧠 How Provably Fair Works

1. Server generates a secret seed
2. SHA256 hash of seed is published before gameplay
3. Each round uses:
