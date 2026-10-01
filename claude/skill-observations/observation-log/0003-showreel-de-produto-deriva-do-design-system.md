---
id: 3
title: "Motion graphics de produto deve derivar a estetica dos tokens e capturas reais do produto"
status: parked
type: new-skill
skill: []
proposes_skill: "product-motion-reel"
target_file: []
siblings_checked: "nenhuma skill de video/motion instalada cobre isso"
area: "producao de video/motion a partir de um projeto de software"
date: 2026-09-28
session_context: "Showreel de 15 s do Gestor de Pecas (canvas HTML + Playwright + ffmpeg + audio numpy)"
parked_until: "próximo pedido de vídeo/motion de produto — criar product-motion-reel com 2 casos reais via skill-creator"
resolved: 
resolution: 
reference: "outputs/showreel_gestor_pecas.mp4"
---

O primeiro corte usou uma estetica generica neon/cyberpunk escura; o usuario corrigiu com "Tente seguir o design do sistema". O segundo corte partiu de `web/src/styles/tokens.css`, do CSS do Andon e das capturas em `docs/evidencias/` e foi aceito como alinhado.

Regra candidata: quando o video for "do meu projeto", ler antes os tokens de design, o logo e 2 ou 3 capturas reais, e recriar as telas-assinatura (cards de KPI, Andon) como cenas, em vez de inventar uma linguagem visual.

Pipeline reutilizavel: `window.frame(i)` puro no tempo, com motion blur por subamostras; Playwright com fallback para msedge; `image2pipe` para o ffmpeg do imageio-ffmpeg; trilha sintetizada em numpy, com cenas ancoradas em batidas.
