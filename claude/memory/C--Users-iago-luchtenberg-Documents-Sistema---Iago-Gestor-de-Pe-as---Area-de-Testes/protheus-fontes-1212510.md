---
name: protheus-fontes-1212510
description: Onde estão os fontes Protheus 12.1.2510 na máquina e qual é a rotina oficial que monta o ProductionOrder.
metadata:
  type: reference
---

Os fontes TOTVS 12.1.2510 estão na máquina e evitam qualquer suposição sobre
ADVPL:

- pacote original: `C:\Users\iago.luchtenberg\Downloads\1212510.rar`;
- já extraídos em um scratchpad de sessão anterior:
  `C:\Users\iago.luchtenberg\AppData\Local\Temp\claude\C--Users-iago-luchtenberg-Documents-Sistema---Iago-Gestor-de-Pe-as---Area-de-Testes\3d3d0826-5b6e-4521-9fe1-c236752fbe80\scratchpad\fontes\1212510\fontes\totvspcp`
  (~20 MB; scratchpads podem ser limpos — se sumir, extrair o `.rar` de novo);
- também há `C:\Users\iago.luchtenberg\Documents\Atualização PPI.zip`.

Cadeia oficial que gera o `ProductionOrder` (descoberta em 02/09/2026):

```
PCPA111.prw::sincOP()      posiciona SC2 -> mata650PPI(,,.T.,.T.,.F.,.F.)
mata650.prx::mata650PPI()  -> PCPa650PPI()   (param oficial lInCustom p/ customizacao)
pcpxfun.prx::PCPa650PPI()  define lRunPPI/cPonteiro/INCLUI/ALTERA e chama
                              MATI650("", TRANS_SEND, EAI_MESSAGE_BUSINESS, "2.004")
                              aRetXML[2] := EncodeUTF8(aRetXML[2])
                           e SO DEPOIS transporta via PCPWebsPPI()
MATI650.prw::MATI650()     monta e RETORNA o XML em memoria (aRet[2])
MATI650.prw::completXml()  envolve no TOTVSMessage 2.004 usando cEmpAnt/cFilAnt/FunName()
```

**Why:** `MATI650` devolver o XML em memória é o que torna o modo *inline*
possível; sem esse fato a Etapa 6.2 teria caído no fallback *push*.

**How to apply:** consultar estes fontes antes de escrever qualquer ADVPL/TLPP,
em vez de inferir assinatura. O endpoint entregue está em
`fontes/10-PCP/GPOPSYNC.prw`. Ver também [[etapa61-totvs-sem-pull-de-op]].
