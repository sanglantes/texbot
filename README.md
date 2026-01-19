# TeXBot
An IRC bot that renders and displays TeX code.

## Installation
TeXBot can be run in Docker with `docker build -t tex .` followed by `docker run tex`. Configure where TeXBot will connect to in the Dockerfile.

## Notes
TeXBot runs on TeX, not LaTeX. It can only render inside math mode, not in documents. Images are uploaded to [https://0x0.st/](https://0x0.st/). To avoid false TeX detections, TeXBot exclusively responds to LaTeX math delimiters (`\(...\)` for inline math and `\[...\]` for display mode).

## Showcase
![Example messages](/imgs/1.png)
![Example results](/imgs/2.png)