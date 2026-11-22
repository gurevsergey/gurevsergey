<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/dashboard-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/dashboard-light.svg">
  <img src="assets/dashboard-dark.svg" width="100%" alt="gurevsergey: networks, monitoring, automation, Rust CLI tools, drawn as a dashboard with a network topology and a traffic chart">
</picture>

Networks first: routing, tunnels and firewalls on Linux and MikroTik, watched with Prometheus and Grafana, rolled out with Ansible. When a tool is missing, I write it in Rust.

### Tech Stack

![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)
![MikroTik](https://img.shields.io/badge/MikroTik-293239?style=for-the-badge&logo=mikrotik&logoColor=white)
![Prometheus](https://img.shields.io/badge/Prometheus-E6522C?style=for-the-badge&logo=prometheus&logoColor=white)
![Grafana](https://img.shields.io/badge/Grafana-F46800?style=for-the-badge&logo=grafana&logoColor=white)
![Ansible](https://img.shields.io/badge/Ansible-EE0000?style=for-the-badge&logo=ansible&logoColor=white)
![Wireshark](https://img.shields.io/badge/Wireshark-1679A7?style=for-the-badge&logo=wireshark&logoColor=white)
![NetBox](https://img.shields.io/badge/NetBox-00857D?style=for-the-badge)
![nftables](https://img.shields.io/badge/nftables-4B5563?style=for-the-badge)
![systemd](https://img.shields.io/badge/systemd-2F855A?style=for-the-badge)
![Bash](https://img.shields.io/badge/Bash-121011?style=for-the-badge&logo=gnubash&logoColor=white)
![fish](https://img.shields.io/badge/fish-34C534?style=for-the-badge&logo=fishshell&logoColor=white)
![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white)
![Arch Linux](https://img.shields.io/badge/Arch_Linux-1793D1?style=for-the-badge&logo=archlinux&logoColor=white)
![Hyprland](https://img.shields.io/badge/Hyprland-58E1FF?style=for-the-badge&logo=hyprland&logoColor=black)
![Neovim](https://img.shields.io/badge/Neovim-57A143?style=for-the-badge&logo=neovim&logoColor=white)
![tmux](https://img.shields.io/badge/tmux-1BB91F?style=for-the-badge&logo=tmux&logoColor=white)

### Featured

<a href="https://github.com/gurevsergey/mtcap">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/mtcap-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="assets/mtcap-light.svg">
    <img src="assets/mtcap-dark.svg" width="100%" alt="mtcap: live packet capture from MikroTik routers into Wireshark, with a terminal demo of a DNS capture">
  </picture>
</a>

### Projects

| Project | What it does | Built with |
|---|---|---|
| **[mtcap](https://github.com/gurevsergey/mtcap)** | Live packet capture from MikroTik routers into Wireshark: starts the sniffer over the API, unwraps TZSP, ships filter presets and capture reports | Rust, RouterOS API, tshark |
| **[next-hop](https://github.com/gurevsergey/next-hop)** | `hop`, a command-line location switcher with per-app routing, failover and a kill switch | Rust, nftables, systemd |
| **[dotfiles](https://github.com/gurevsergey/dotfiles)** | My Arch Linux desktop on Hyprland with Waybar, kitty, fish, rofi, Neovim and tmux, plus guides to the tmux and Neovim setup | Lua, shell, Python |

### How I work

- **Measure before changing.** A capture or a graph first, a config change second.
- **Leave the router as I found it.** My tools restore settings on exit and carry a watchdog for when the laptop disappears.
- **Write it down.** Every change ends in a note: what was asked, what was done, how it was checked.

### Lab

At home: a routing lab in EVE-NG for BGP practice, and a Prometheus and Grafana stack watching the network.
