---
marp: true
theme: workshop
paginate: true
title: Inside DRAM
author: Workshop
---

<!-- _class: title -->

<img class="gem5-brand" src="../../assets/images/gem5-icon.png" alt="gem5 logo" />

## How does DRAM find the data?

![Controller selects a bank and row within DRAM width:970px](../../assets/diagrams/dram-structure.svg)

**A memory controller selects a bank and a row.**

<!-- The controller is outside the DRAM chips. A DRAM read returns data through the controller toward the caches and CPU. -->

---

<img class="gem5-brand" src="../../assets/images/gem5-icon.png" alt="gem5 logo" />

## DRAM stores bits as charge.

![A simplified one-transistor one-capacitor DRAM cell width:970px](../../assets/diagrams/dram-cell.svg)

**A tiny capacitor needs refreshing.**

<!-- This simplified 1T1C cell represents the storage idea, not a production cell layout or precise timing. Then zoom back out to banks and rows. -->

---

<img class="gem5-brand" src="../../assets/images/gem5-icon.png" alt="gem5 logo" />

## DRAM has independent banks and rows.

![Two DRAM banks with rows width:970px](../../assets/diagrams/dram-banks.svg)

<!-- Banks can work somewhat independently; each bank has many rows and can have an open row. The shown rows are a small teaching sample, not the actual geometry of DDR3. -->

---

<img class="gem5-brand" src="../../assets/images/gem5-icon.png" alt="gem5 logo" />

## Same open row: row hit.

![Request for row four when row four is open width:970px](../../assets/diagrams/row-hit.svg)

The bank can reuse its open row.

<!-- The request travels toward the bank. A DRAM row buffer hit is different from a CPU cache hit. -->

---

<img class="gem5-brand" src="../../assets/images/gem5-icon.png" alt="gem5 logo" />

## Different row, same bank: conflict.

![Request for row nine when row four is open width:970px](../../assets/diagrams/row-conflict.svg)

Switching rows adds operations.

<!-- The request travels toward the bank. A large stride does not guarantee a row conflict; address mapping can select another bank instead. -->
