# Use ParrotSec core as base
FROM parrotsec/core:latest
ENV DEBIAN_FRONTEND=noninteractive

# Install core tools
RUN apt update && apt upgrade -y && \
    apt install -y --no-install-recommends \
        git curl wget sudo zsh tmux htop neofetch unzip stow fzf && \
    apt clean

# Add non-root user
RUN useradd -m crvngr && \
    echo "crvngr ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/crvngr && \
    chown -R crvngr:crvngr /home/crvngr

SHELL ["/usr/bin/zsh", "-c"]

# Switch to non-root user
USER crvngr
WORKDIR /home/crvngr

# Install tmux, ohmyposh and dotfiles from repo
RUN git clone https://github.com/tmux-plugins/tpm /home/crvngr/.tmux/plugins/tpm
RUN curl -sS https://raw.githubusercontent.com/ajeetdsouza/zoxide/main/install.sh | bash

USER root
RUN curl -s https://ohmyposh.dev/install.sh | bash -s -- -d /usr/local/bin
USER crvngr

RUN git clone https://github.com/CuriousAvenger/Dotfiles.git /home/crvngr/Dotfiles && \
    stow -d /home/crvngr/Dotfiles -t /home/crvngr .

# Copy HackTheBox OVPN file
COPY .Env/hackthebox.ovpn /home/crvngr/hackthebox.ovpn
WORKDIR /home/crvngr
ENTRYPOINT ["zsh"]
