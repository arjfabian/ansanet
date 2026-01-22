# 👨🏻‍💻 ANSANET: Automated Honeypot Framework & Training Simulator

**ANSANET** is an ultra-lightweight, procedural network simulation framework designed for **Detection Engineering** training and **Deception** strategy validation. Unlike traditional honeypots that rely on heavy Virtual Machines or Containers, ANSANET emulates infrastructure "on-the-fly" using a **roguelike** approach to network generation.

### 🎯 Project Objectives

* **Zero-Footprint Emulation:** Generate complex network topologies (Windows/Linux) without the overhead of VMs or containers.
* **Procedural Training:** Every session creates a unique network map, forcing analysts and attackers to perform real reconnaissance.
* **Security Visibility:** Provide a dashboard for SOC analysts to monitor emulated "attacks" and lateral movement in real-time.
* **Cost-Effective Education:** A tool for mentoring junior engineers in threat hunting and incident response without licensing costs.

### 🧠 How it Works

1. **Parameters:** Define network rules in `parameters/network.yml`.
2. **Procedural Generation:** `network_generator.py` creates a unique IP/Host mapping.
3. **Host Blueprinting:** `host_generator.py` "dresses" each node with virtual filesystems and services.
4. **Active Alerting:** The **ANSANET Alert System** (Telegram Bot) notifies the SOC of deployment and events.

## Quick Start

1. It's highly recommended to create a virtual environment:

    ```sh
    $ python -m venv .venv
    $ source .venv/bin/activate
    ```

2. Install the requirements:

    ```sh
    pip install -r requirements.txt
    ```

3. Copy the included `.env.sample` to a file called `.env` and populate it using:

- Your Telegram bot

- Your Chat ID

    **Notes:**

    - If you want to create a Telegram bot, use the [BotFather](https://t.me/BotFather) service. Then open it (using https://t.me/[YourBotName] and start a chat.

    - In order to get your Telegram Chat ID, use a service like [UserInfoBot](https://t.me/userinfobot).

4. Start ANSANET:

    ```sh
    $ python ansanet.py
    ```

You should receive a message on your Telegram app displaying details of the generated network.

### 🛠️ Planned Features (Roadmap)

1. **Phase 1 (Core Engine):** Procedural network and host generator (JSON-based state).
2. **Phase 2 (Interaction Layer):** Emulated CLI for attackers (Nmap/SMB/SSH simulation).
3. **Phase 3 (Detection & Alerting):** Integration with Telegram and n8n workflows for incident notification.
4. **Phase 4 (Gamification):** Scoring system based on the **MITRE ATT&CK** framework.

## Licensing

This project is licensed under the **MIT License**. You are free to use, modify, and distribute this lab as long as you provide attribution.