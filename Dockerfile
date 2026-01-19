FROM python:3.14.2-slim

WORKDIR /bot

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt 

RUN apt-get update \
 && DEBIAN_FRONTEND=noninteractive apt-get -y install --no-install-recommends dvipng texlive-latex-extra texlive-fonts-recommended cm-super \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

COPY . .

RUN mkdir -p /home/.config/matplotlib && \
    echo "text.latex.preamble : \\usepackage{amssymb} \\usepackage{amsmath}" \
    >> /home/.config/matplotlib/matplotlibrc

CMD ["python3", "bot.py", "irc.zoite.net", "#test", "1"]
# server address, channel, use ssl (0, 1)
