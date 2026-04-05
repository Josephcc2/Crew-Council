# Crew-Council
4 LLMs work together to generate a report based off of scientific papers without hallucinations

### For CrewAI Setup
Ensure you have Python >=3.10 <3.13 and CrewAI installed on your system. This project uses [UV](https://docs.astral.sh/uv/) for dependency management and package handling, offering a seamless setup and execution experience.

First, if you haven't already, install uv:

```bash
pip install uv
```

Next, navigate to your project directory and install the dependencies:

(Optional) Lock the dependencies and install them by using the CLI command:
```bash
crewai install
```
### Customizing

**Add your `OPENAI_API_KEY` or `ANTHROPIC_API_KEY` into the `.env` file**

- Modify `src/crew_council/config/agents.yaml` to define your agents
- Modify `src/crew_council/config/tasks.yaml` to define your tasks
- Modify `src/crew_council/crew.py` to add your own logic, tools and specific args
- Modify `src/crew_council/main.py` to add custom inputs for your agents and tasks

## Running the Project

To kickstart your crew of AI agents and begin task execution, run this from the root folder of your project:

```bash
$ crewai run
```

This command initializes the crew-council Crew, assembling the agents and assigning them tasks as defined in your configuration. Run the command for both crew_council and crew_council_claud

To run each python script, run the following from each folder:
```bash
python name_of_script.py
```

## API Setup
Each Python script requires you to set the API key for each model through an environment variable.

For each script, run the command:
```bash
set OPENAI_API_KEY=your_api_key_here
```
(Change OPENAI to the LLM service you are accessing)

## Background Info
![Background Info](https://github.com/user-attachments/assets/79baca84-b329-4f9d-8ba4-437a349dabc2)

## Architecture
TBD

## Example Report
**Topic: Effects Of Caffeine On Sleep**

# Effects of Caffeine on Sleep: A Comprehensive Report

## Introduction

Caffeine, the world's favorite pick-me-up in coffee, tea, and energy drinks, boosts alertness but sabotages sleep like an uninvited guest at bedtime. This report merges key insights from rigorous studies, explaining how caffeine disrupts rest—through science made simple for anyone curious about better nights.[1]

## Mechanisms of Action

Imagine adenosine as your brain's "fatigue debt collector," building up all day to signal it's time for sleep. Caffeine jams those receptors, keeping you wired. It also spikes cortisol (stress hormone) by ~**30%** after a 250 mg dose (about two coffees) in the morning, ramping arousal. With a half-life of **2.7–8.2 hours** in healthy adults—half the caffeine lingers that long—it haunts evening sleep. Indirectly, it tweaks GABA (calming brain chemical), but adenosine blockade dominates.[2][6]

## Dose, Timing, and Sleep Parameters

Timing trumps all: 400 mg (three coffees) 0, 3, or 6 hours pre-bed delays sleep onset (**SOL**) by **30–60 min** and cuts total sleep time (**TST**) by **~45 min**, per landmark trial. Effects persist due to half-life.[3]

**Summary Table: Caffeine Effects on Key Sleep Metrics** (meta-analysis of 18 PSG studies; mean changes, 95% CI)[^1]

| Sleep Parameter     | Overall Effect     | 95% CI             |
|---------------------|--------------------|--------------------|
| Sleep Onset Latency | +**28.7 min**     | [18.1, 39.3]      |
| Total Sleep Time    | -**44.8 min**     | [-58.9, -30.7]    |
| Slow-Wave Sleep     | -**23.1 min**     | [-30.8, -15.4]    |
| Sleep Efficiency    | -**7.0%**         | [-9.2, -4.8]      |

[2][3]

## Sleep Architecture and Disorders

Caffeine reshapes nights: less deep slow-wave sleep (**SWS**, down **20–25%**) and REM (dream/memory stage), more shallow toss-turns. Meta-analysis confirms; habitual >200 mg/day hikes insomnia odds **1.5–2-fold**. Feel groggy? Blame fragmented architecture.[1][2]

## Individual Variability

Not one-size-fits-all. **~50%** are slow CYP1A2 metabolizers (gene variant), doubling half-life for worse disruption.[4] Older adults (>60) see **+50%** half-life, kids/adolescents hypersensitive (100 mg cuts ~1h sleep).[5] Night owls (evening chronotypes) suffer **1.8x** more from late doses. Chronic use upregulates receptors (**20–60%** after 7 days), blunting acute hits but fueling dependence.[6]

[4][5][6]

## Practical Implications and Conclusion

Caffeine reliably erodes sleep via dose, timing, genes, and biology—cut deep rest, spike latency, fragment nights. Tailor use for recharge.

**Actionable Tips:**
- **Dose:** ≤**200 mg**/day (~2 coffees); test sensitivity.
- **Timing:** Morning only (<10 AM); skip 6+ hours pre-bed.
- **Alternatives:** 20-min naps, walks, light exposure.
- **Withdrawal Note:** Quitting brings rebound sleepiness (peaks 24–48h), then +**30–60 min** sleep/↑deep stages—temporary win for quitters.

Personalize: slow metabolizers/night owls/elders, go earliest/lowest. Balance buzz with Zzzs.[1][3]

## Bibliography

[1] Irene Clark and Hans-Peter Landolt, "Coffee, Caffeine, and Sleep: A Systematic Review of Epidemiological Studies and Randomized Controlled Trials," *Sleep Medicine Reviews* 31 (2017): 70–78, https://doi.org/10.1016/j.smrv.2016.01.006.

[2] Carolin F. Reichert et al., "Characterisation of the Effects of Caffeine on Sleep Using a Polysomnography-Based Systematic Review and Meta-Analysis," *Sleep Medicine Reviews* 70 (2023): 101799, https://doi.org/10.1016/j.smrv.2022.101799.

[3] Christopher Drake, Timothy Roehrs, and Thomas Roth, "Caffeine Effects on Sleep Taken 0, 3, or 6 Hours before Going to Bed," *Journal of Clinical Sleep Medicine* 9, no. 11 (2013): 1195–1200, https://doi.org/10.5664/jcsm.3170.

[4] Ashley Yang et al., "CYP1A2 Genotype Modifies the Effects of Caffeine Compared with Placebo on Sleep," *American Journal of Clinical Nutrition* 92, no. 1 (2010): 192–99, https://doi.org/10.3945/ajcn.2009.29067.

[5] Julie Carrier et al., "Effects of Caffeine on Daytime Recovery Sleep in Late Middle-Aged and Older Men and Women," *Journal of Clinical Sleep Medicine* 14, no. 4 (2018): 599–607, https://doi.org/10.5664/jcsm.7032.

[6] Bertil B. Fredholm et al., "Actions of Caffeine in the Brain with Special Reference to Factors That Contribute to Its Widespread Use," *Pharmacological Reviews* 51, no. 1 (1999): 83–133, https://doi.org/10.1124/pr.51.1.83.

[^1]: Reichert et al., "Characterisation of the Effects of Caffeine on Sleep," table 2, 101799 (dose-averaged; low/moderate/high stratified similarly).
