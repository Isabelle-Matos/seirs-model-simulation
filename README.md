# Malware Propagation Simulation: SEIRS and Human Correction

This repository contains the implementation of an epidemiological SEIRS model based on cellular automata, used to analyze malware propagation in mobile device networks. The project uses distinct branches to differentiate the base model from the proposed extension.

## Branch Structure

The code is organized as follows:

* `master`: Contains the original implementation of the propagation methodology according to [1, 2]. This branch simulates infection dynamics without external intervention, serving as a baseline for validation.
* `feature/human-factor`: Contains the extended version that introduces the human factor ($p$) as a mitigation variable. This implementation allows analyzing how individual decision-making acts to contain the infectious outbreak across different neighborhood topologies.

## How to Run

To access the different versions of the project, use Git commands to switch between branches:

1. To access the base model:
   ```bash
   git checkout master
2. To access the extended model (Human-Factor):
   ```bash
   git checkout feature/human-factor

## References
[1] Peng, S., Wang, G., & Yu, S. (2013). Modeling the dynamics of worm propagation using two-dimensional cellular automata in smartphones. Journal of Computer and System Sciences, 79(4), 586-595.

[2] Signes-Pont, M. T., Cortés-Castillo, A., Mora-Mora, H., & Szymanski, J. (2018). Modelling the malware propagation in mobile computer devices. Computers & Security, 79, 80-93.