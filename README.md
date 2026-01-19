# Project Ansanet

Ansanet is a **network deception framework** designed to deploy and manage low-interaction honeypots within a dedicated virtual environment. Built on the principle of **"minimalism as security"**, Ansa provides a fast, dedicated, and auditable command-line interface (CLI) for monitoring and controlling simulated network activity.

## 🎯 Purpose and Function

The primary goal of Ansanet is to serve as a high-efficiency sentinel for threat detection. By running the core management logic on a bare-bones Alpine Linux installation, the manager system itself presents a minimal attack surface.

Ansanet allows a security operator to:

- Deploy Virtual Traps: Instantiate and monitor a customizable network of simulated hosts and vulnerable services.

- Observe Attacks: Log and visualize simulated network probing, brute-force attempts, and exploit attempts targeting the emulated services.

- Manage Status: Manually toggle the operational status of individual simulated honeypots (online/offline) directly from the CLI.

## 🛠️ The Technical Stack

Ansanet adheres strictly to a minimalist execution model:

| Component        | Role                                  | Rationale                                                                                    |
| ---------------- | ------------------------------------- | -------------------------------------------------------------------------------------------- |
| Operating System | Alpine Linux (x86_64)                 | Boots to a non-GUI, disk-installed system, reducing attack surface to the bare minimum.      |
| Virtualization   | QEMU + KVM                            | Provides high-performance, hardware-accelerated virtualization for deployment repeatability. |
| Core Logic       | Python 3                              | Runs the ansa_manager.py CLI for fast, colorful, and interactive management.                 |
| Deployment       | Host Orchestrator (bash) + Custom ISO | Ensures zero-touch, automated installation and provisioning via Git clone upon first boot.   |

This project prioritizes resource efficiency and direct control. By eliminating unnecessary system overhead, Ansanet ensures that computational resources are dedicated entirely to deception, logging, and monitoring.

## 💻 The Interface

The Ansanet CLI is designed for a TTY-compatible environment, so basic ANSI color support will be implemented.

### Screen Compatibility Standard

Adhering to the principle of "minimalism as security", the screen should use as little resources as possible.

- **Minimum Column Width:** The entire dashboard layout is guaranteed to render correctly at a minimum width of 80 columns.

- **Default Display:** The application runs in a tight loop, making the necessary changes on every update cycle.

### Dashboard Layout Zones

The interface is divided into three distinct zones:

#### A. Header Zone

The header provides branding and global status information.

    Content: Project name (ANSA MANAGER CLI), project motto/meaning, and the count of active honeypots.

    Color Use: Primarily Magenta (C_MAGENTA) for structure and Bold (C_BOLD) for emphasis.

#### B. Host Table Zone

This is the primary data display area, detailing the state of each simulated honeypot.

| Field      | Width (Approx.) | Purpose                                                  | Color Coding                                              |
| ---------- | --------------- | -------------------------------------------------------- | --------------------------------------------------------- |
| IP ADDRESS | 15 characters   | The simulated network address of the trap host.          | None (Default text)                                       |
| NAME       | 15 characters   | Human-readable identifier (e.g., Web-Trap-01).           | None (Default text)                                       |
| SERVICES   | 20 characters   | List of emulated services/ports (e.g., HTTP/80, SSH/22). | None (Default text)                                       |
| STATUS     | 10 characters   | Operational state (ONLINE or OFFLINE).                   | Green (Online), Yellow (Offline)                          |
| ACTIVITY   | Remainder       | Threat level based on simulated probing intensity.       | Green (Low), Blue (Medium), Yellow (High), Red (Critical) |

#### C. Footer and Control Zone

The footer provides navigation and command entry.

- Menu: Lists the available one-character commands: [M]anage | [L]ogs | [Q]uit.

- Command Prompt: The application uses a distinct, colored prompt: Ansanet > .

### 3. Core Color Palette (ANSI)

Colors are used not just for aesthetics, but for rapid status indication.

- C_MAGENTA: Branding and structural elements (separators, borders).

- C_CYAN: Logging timestamps and minor headings.

- C_GREEN: Good status (Host ONLINE, Activity LOW).

- C_YELLOW: Warning/Management state (Host OFFLINE, Activity HIGH).

- C_BLUE: Medium activity or secondary status.

- C_RED: Critical security alerts (Highest Activity level).
