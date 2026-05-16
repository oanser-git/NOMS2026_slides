# Speech Notes

## Title Slide

Hello everyone. My name is Omar Anser. I am a postdoctoral researcher at the University of Luxembourg, and today I will present our work titled **"An Empirical Study on Configuration Robustness of Unsupervised IDS."** I did this work during my PhD, before I started my current position.

## Slide 1: ML-Based AD IDS Workflow

Let's start with some context. To deploy a machine-learning-based anomaly detection IDS, we typically follow this workflow.

**Click 1.** First, we train a model, for example here an Isolation Forest, on a training dataset. In anomaly detection, this typically means learning a representation of legitimate traffic, so that traffic that deviates from this representation can later be flagged as suspicious.

**Click 2.** Then, at validation, we use a validation split to choose the model configuration. This configuration is not learned like the model itself; we select it by testing candidate choices on validation data. This validation data can include some attack traffic to guide the selection.

The configuration includes the hyperparameters. For example, with Isolation Forest, the number of trees or the subsampling strategy can change the anomaly scores. Too few trees may make scores unstable, and poor subsampling may miss rare attack structure.

At this step, there is a loop between training and validation. In each iteration, we refine the model configuration until we obtain the best-performing model for the validation data.

**Click 3.** After that, we evaluate the selected model on a final test set, \(\mathcal{D}_{\text{test}}\), which is supposed to estimate performance on unseen traffic.

**Click 4.** Finally, the selected model and its configuration are deployed to monitor live traffic.

**Click 5.** In this work, we focus specifically on hyperparameter configuration and its impact on AD IDS performance.

## Slide 2: Related Work and Gap

There are two main lines of related work that motivate this study.

First, in the broader machine learning literature, prior work has shown that hyperparameters matter a lot. A small number of hyperparameters can explain a large part of the performance variation. Other work on distribution shift also shows that hyperparameters optimized on one distribution may fail when the data distribution changes.

Second, in security and IDS, several studies show that tuning and validation choices strongly affect reported IDS performance. The figure on the right, from Bilot et al., illustrates this very clearly: tuned and untuned IDS variants can lead to different conclusions.

However, these IDS studies mostly provide a static analysis of the impact of configuration. They show that configuration matters, but they do not quantify what happens when traffic changes over time.

So we already know that configuration matters, and we already know that traffic changes over time.

The gap is that we do not yet have a direct quantification of this effect for AD IDS under network context changes.

## Slide 3: Operational Setting and Research Questions

The two research questions of this work are based on two operational settings.

First, reconfiguring can be costly. It is time-consuming because it requires a loop between training and validation, and it requires labeled validation traffic, ideally including attack traffic. For this reason, a configuration is often selected once and then kept fixed.

But the deployment traffic is not fixed. The volume can change, the traffic composition can change, the topology can change, and the attacks can change. So the configuration selected at one point may no longer be appropriate later.

From this setting, we ask two questions.

First, can cheaper strategies, such as defaults or low-budget optimization, get close to the oracle-optimized reference without full reconfiguration?

Second, if we keep a configuration fixed and reuse it, how much performance do we lose compared with reconfiguring for the current network context?

In other words, we measure the performance penalty of avoiding full reconfiguration in AD IDS.

## Slide 4: Experimental Setup - Benchmark Context

We answer these two research questions with an empirical study.

**Click 1.** We used the corrected IDS2017 and IDS2018 datasets. They are organized as day-level traffic datasets, from \(D_0\) to \(D_{13}\). The first four days, \(D_0\) to \(D_3\), come from IDS2017. The remaining ten days, \(D_4\) to \(D_{13}\), come from IDS2018, which has a different topology and different hosts.

**Click 2.** Then we show two simple indicators for each day. First, the flow volume changes strongly across days. Second, the benign share is above 95 percent on 8 days out of 14, but it is clearly lower on the remaining days. So even before looking at the attack types, the normal traffic context is not identical from one day to another.

**Click 3.** The attack types also change by day. For example, one day is DoS-heavy, another mixes scanning and LOIC traffic, and other days contain web, infiltration, or botnet activity.

**Click 4.** Because the year, topology, traffic volume, benign-share pattern, and attack types all vary across days, we treat each day as a distinct deployment context. This lets us test whether a configuration selected in one context remains robust when the network context changes.

## Slide 5: Experimental Setup - IF, BO, and Robustness Metric

This slide defines the basic evaluation unit.

**Click 1.** The detector is Isolation Forest. For each evaluation, we train it on benign training flows. Then we score evaluation flows that contain both benign and attack traffic.

This matches the anomaly-detection setting: the model is trained to represent benign traffic, and attacks are expected to appear as anomalous observations.

**Click 2.** To compare configurations, we use ROC-AUC. Here, each flow receives an anomaly score. ROC-AUC measures how well these scores rank attack flows above benign flows. A high value means that, most of the time, an attack flow receives a higher anomaly score than a benign flow. I call this value \(p_{\text{robust}}\), the robustness score.
This is useful because we compare the scoring quality of configurations without choosing one operational alert threshold.

So the question is not whether one threshold happens to be good. The question is whether the scoring function separates benign and attack traffic well.

**Click 3.** The configuration \(\theta\) contains seven Isolation Forest hyperparameters. They control effects such as the number and depth of trees, split granularity, and how features are combined.

These choices can change the anomaly scores even when the training and testing data are the same.

**Click 4.** For each day, Bayesian optimization gives us an oracle reference configuration, \(\theta_i^\star = BO(D_i)\). This is not meant to be an operationally cheap solution. It is the reference we compare against when we ask how much robustness cheaper strategies lose.

## Slide 6: Research Question 1

This brings us to the first research question.

Can cheaper strategies approach the oracle-optimized reference without running full reconfiguration every time?

The next three slides define the cheaper strategies we test.

## Slide 7: Experimental Setup - Alternative 1, Default

The first low-cost strategy is the simplest one: use the software default configuration.

This strategy has zero tuning cost. It is also common in practice, either because tuning is expensive or because the default is assumed to be reasonable.

For each day, we keep \(\theta_{\text{default}}\) unchanged and measure \(p_{\text{robust}}\) on that day.

The baseline question is therefore: do we need configuration search at all, or are defaults already robust enough when the network context changes?

## Slide 8: Experimental Setup - Alternative 2, Single Overall

The second strategy is to optimize once on a heterogeneous pool of historical data.

Here, we combine all days into one global dataset, run Bayesian optimization once, and obtain one configuration, \(\theta_{\text{overall}}^\star\).

Then we reuse this same configuration on every day.

This is attractive because the BO effort is paid only once. It also seems reasonable if we believe that a diverse historical pool captures enough variability.

The question is whether one global configuration can cover all deployment contexts, or whether it hides failures on specific days.

## Slide 9: Experimental Setup - Alternative 3, 10% Sample BO

The third strategy keeps day-specific adaptation, but reduces the optimization effort.

For each day, we take a stratified 10 percent sample. This preserves the label proportions, but uses much less data during Bayesian optimization.

BO then returns a day-specific sampled configuration, and we evaluate that configuration on the full day.

This tests a practical compromise: can a small representative sample recover most of the robustness of full daily optimization?

If it works, it would be a cheaper way to adapt to each deployment context.

## Slide 10: Experimental Setup - Nested Cross-Validation

This slide shows how we avoid test leakage.

**Click 1.** We use a nested cross-validation protocol. For benign traffic, four folds are used for training and one fold is used for testing. For attack traffic, one fold is used during configuration and four folds are kept for testing.

The key point is that the test folds are not used to choose \(\theta\).

**Click 2.** The configuration step happens inside the training data. For BO, the validation uses inner benign folds plus one attack training fold. For reuse strategies, we skip BO and use the fixed candidate configuration.

**Click 3.** Once \(\theta\) is fixed, we train Isolation Forest on the benign training folds and evaluate on the same held-out test folds.

**Click 4.** We do not compute the final value from only one split. We repeat the same outer loop over the five folds.

**Click 5.** Each fold gives one \(p_{\text{robust}}\) score, and the reported robustness score is the mean \(p_{\text{robust}}\) over the five folds.

This protocol is important because otherwise a configuration could look robust simply because it was selected using the test data.

## Slide 11: Main Results

Now I move to the main results.

**Click 1.** The first curve is the daily BO oracle. This is the reference where each day gets its own optimized configuration. As expected, it stays consistently high.

This tells us that the detector can perform well on most days if the configuration is adapted to the current context.

**Click 2.** The next curve is the single overall configuration. Its aggregate score looks high, around 0.95. But the day-level view shows that this average hides unstable days.

This is one of the main messages: an aggregate score can make a configuration look robust even when it fails in particular deployment contexts.

**Click 3.** The default configuration is good only on a few easier days. On other days, it drops sharply, and on day 13 it is close to zero.

So defaults are not uniformly robust when the network context changes.

**Click 4.** The 10 percent sample BO strategy reduces optimization effort, but it does not remove instability. It still has low values on several days, including early days, day 7, and day 13.

This means that sampling can make optimization cheaper, but the sample may not preserve the information needed to choose a robust configuration.

**Click 5.** The deployment view makes the risk visible. The same risky days appear across strategies, but the performance penalty of using the wrong configuration differs.

The takeaway is that low-budget configurations do not reliably approximate the daily BO oracle.

This answers the first research question. Next, we move from low-cost alternatives to configuration reuse across contexts.

## Slide 12: Research Question 2

This brings us to the second research question.

If a configuration is reused, how much performance is lost compared with reconfiguring for the current network context?

The next experiments measure this loss when configurations are transferred across days and across years.

## Slide 13: Day-to-Day Transferability - Method

The next question is whether optimized configurations transfer across days.

**Click 1.** Bayesian optimization gives one oracle configuration per day. We pick one source day \(D_j\), and take its optimized configuration \(\theta_j^\star\).

**Click 2.** The diagonal cells are the oracle references. They are not transfer evaluations, because the source and target day are the same.

**Click 3.** For transfer, we keep \(\theta_j^\star\) fixed and evaluate it on every other target day \(D_i\), excluding \(i=j\).

This gives us the loss from using a configuration optimized on a different day.

**Click 4.** Repeating this for all source days fills the off-diagonal matrix. Each column corresponds to one source configuration, and each row corresponds to one target day.

**Click 5.** For example, row \(R_0\) collects all transfer losses for target day \(D_0\), from all source days except \(D_0\) itself. We then summarize that row as one box plot.

Lower row losses mean safer configuration reuse for that target day.

## Slide 14: Day-to-Day Transferability - Results

Here, each box summarizes one target day.

The value inside a box is the performance decrease when we use configurations transferred from other days instead of the oracle configuration for that target day.

Low medians mean that most source configurations transfer well to that target day.

Wide boxes and outliers mean that the result depends strongly on which source day we choose.

The key observation is that transferability is not universal. Some days are relatively safe, but days 5, 6, 7, and 10 are much riskier. On these days, the loss can approach 40 percent.

So even if a configuration was optimal somewhere in the benchmark, it may be a poor choice for another deployment day.

## Slide 15: Cross-Year Attack Transfer - Method

The last experiment asks whether configurations transfer across years for the same attack family.

**Click 1.** We start from the 18 attack families that are common to IDS2017 and IDS2018.

**Click 2.** For one attack \(a_k\), we build a paired dataset in both years. The attack family is the same, but the year, topology, traffic volume, and surrounding context differ.

The benign background is sampled once from IDS2017 and reused in both paired datasets. This keeps the benign side controlled while we compare the effect of year and attack context.

**Click 3.** We run BO on the IDS2017 source data to get \(\theta_{a_k}^{\star 2017}\). We also run BO on the IDS2018 target data to get the IDS2018 oracle, \(\theta_{a_k}^{\star 2018}\).

**Click 4.** Then we evaluate both configurations on the IDS2018 target data and measure the gap.

The question is whether the same attack family implies the same robust configuration. The answer is not always.

## Slide 16: Cross-Year Attack Transfer - Results

This figure shows the transfer result for each attack family.

For each attack, we compare the IDS2017-tuned configuration transferred to IDS2018 against the IDS2018 oracle.

Some attacks transfer close to the oracle. In particular, attacks 23, 17, 16, 14, and 26 show small gaps.

But other attacks have much larger cross-year gaps, especially attacks 31, 1, and 30.

The message is that the attack label alone is not enough. Even for the same attack family, year-level context changes can change which configuration is robust.

So cross-year context changes can still require reconfiguration.

## Slide 17: Takeaway

To conclude, the first takeaway is that retraining alone is not enough if the hyperparameters remain fixed.

The detector can be retrained on new benign traffic, but if the configuration is poorly matched to the current context, robustness can still drop.

Second, configuration reuse under changing contexts can remove a large part of the discrimination power. In our experiments, some transfer losses approach roughly one third to 40 percent, depending on the setting.

Third, AD IDS should not treat configuration as a one-time setup. The configuration needs to be monitored and, when necessary, updated.

A natural next direction is to avoid continuous expensive optimization, and instead trigger reconfiguration only when a lightweight change detector reports enough traffic change.

The final message is: treat the configuration as an operational asset to monitor.

## Slide 18: Acknowledgments

I would like to acknowledge the funding support for this work.

This work received partial support from the French National Research Agency through the France 2030 initiative, under the Superviz project, ANR-22-PECY-0008.

It also received support from the Luxembourg National Research Fund under the COCTEL project.

The opinions expressed are those of the authors and do not necessarily reflect the views of the French government.

## Questions

Thank you for your attention. I would be happy to take your questions.
