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

First, if we keep a configuration fixed and reuse it, how much performance do we lose compared with reconfiguring for the current network context?

Second, can simple low-budget strategies, such as defaults or reduced-budget optimization, get close to the performance of full reconfiguration?

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

**Click 4.** For each day, Bayesian optimization gives us an oracle reference configuration, \(\theta_i^\star = BO(D_i)\). This is not meant to be an operationally cheap solution. It is the reference we compare against when we ask how much robustness simple low-budget strategies lose.

## Slide 6: Experimental Setup - Data Splits and BO Search

This slide explains how we compute the oracle reference without using test traffic during configuration.

**Click 1.** We start with an outer split. For benign traffic, four folds are used for training and one fold is held out for testing. For attack traffic, one fold is available during configuration and four folds are held out for testing.

The key point is that the test folds stay outside the configuration step.

**Click 2.** Bayesian optimization happens only on the training side. It uses inner cross-validation and the training-side attack fold to select the oracle configuration \(\theta_i^\star\).

**Click 3.** Once \(\theta_i^\star\) is selected, we train Isolation Forest on the benign training folds and test on held-out benign and attack traffic. This gives one \(p_{\text{robust}}\) value.

**Click 4.** We repeat the same outer construction over the five folds.

**Click 5.** The oracle reference reported for a day is the mean \(p_{\text{robust}}\) over these folds.

## Slide 7: Research Question 1

This brings us to the first research question.

If a configuration is reused, how much performance is lost compared with reconfiguring for the current network context?

The next experiments measure this loss when configurations are transferred across days and across years.

## Slide 8: Day-to-Day Transferability - Method

The next question is whether optimized configurations transfer across days.

**Click 1.** Bayesian optimization gives one oracle configuration per day. As a concrete example, we pick source day \(D_9\), and take its optimized configuration \(\theta_9^\star\).

**Click 2.** The diagonal cells are the oracle references. They are not transfer evaluations, because the source and target day are the same.

**Click 3.** For transfer, we keep \(\theta_9^\star\) fixed and evaluate it on every other target day \(D_i\), excluding \(i=9\).

This gives us the loss from using a configuration optimized on a different day.

**Click 4.** Repeating this for all source days fills the off-diagonal matrix. Each column corresponds to one source configuration, and each row corresponds to one target day.

**Click 5.** Each row \(R_i\) groups the transfer losses for one target day \(D_i\). For example, row \(R_0\) collects losses for target day \(D_0\) from all other source days.

Lower row losses mean safer configuration reuse for that target day.

## Slide 9: Day-to-Day Transferability - Results

**Click 1.** Here, each box summarizes one target day.

The value inside a box is the performance decrease when we use configurations transferred from other days instead of the oracle configuration for that target day.

Wide boxes and outliers mean that the result depends strongly on which source day we choose.

The key observation is that transferability is day-dependent, not reliable. Some days are relatively safe, but days 5, 6, 7, and 10 are much riskier. On these days, the loss can approach 40 percent.

So even if a configuration was optimal somewhere in the benchmark, it may be a poor choice for another deployment day.

**Click 2.** We also tested cross-year transferability: configurations tuned on IDS2017 were reused on IDS2018 for common attack types. We observed the same behavior.

**Click 3.** The bottom box gives the answer to the first research question: the cost of reusing a configuration depends on the target context. Some days lose very little, but others can lose up to 40 percent. Even for the same attack type across years, reuse may still require reconfiguration.

## Slide 10: Research Question 2

This brings us to the second research question.

Can simple low-budget strategies approach the performance of full reconfiguration?

The next three slides define the simple low-budget strategies we test.

## Slide 11: Alternative 1 -- Default

The first low-cost strategy is the simplest one: use the software default configuration.

This strategy has zero tuning cost. It is also common in practice, either because tuning is expensive or because the default is assumed to be reasonable.

For each day, we keep \(\theta_{\text{default}}\) unchanged and measure \(p_{\text{robust}}\) on that day.

The baseline question is therefore: do we need configuration search at all, or are defaults already robust enough when the network context changes?

## Slide 12: Alternative 2 -- Single Overall

The second strategy is to optimize once on a heterogeneous pool of historical data.

Here, we combine all days into one global dataset, run Bayesian optimization once, and obtain one configuration, \(\theta_{\text{overall}}^\star\).

Then we reuse this same configuration on every day.

This is attractive because the BO effort is paid only once. It also seems reasonable if we believe that a diverse historical pool captures enough variability.

The question is whether one global configuration can cover all deployment contexts, or whether it hides failures on specific days.

## Slide 13: Alternative 3 -- 10% Sample BO

The third strategy keeps day-specific adaptation, but reduces the optimization effort.

For each day, we take a stratified 10 percent sample. This preserves the label proportions, but uses much less data during Bayesian optimization.

BO then returns a day-specific sampled configuration, and we evaluate that configuration on the full day.

This tests a practical compromise: can a small representative sample recover most of the robustness of full daily optimization?

If it works, it would be a lower-cost way to adapt to each deployment context.

## Slide 14: Nested Cross-Validation

This slide summarizes the common evaluation protocol used for the oracle and for the three simple low-budget strategies.

The outer split is the same as before: benign train and test folds, and attack configuration and test folds.

In the configuration step, there are two cases. The oracle uses BO inside the training data to select \(\theta_i^\star\). The default strategy uses no BO. The overall and sample strategies are BO-derived alternative candidates that are selected before the final evaluation.

After a configuration is fixed, all strategies use the same train-and-test path. We train Isolation Forest on benign training folds and evaluate on the same held-out benign and attack test folds.

This is important because the comparison is fair: the strategies differ in how \(\theta\) is chosen, not in the test data used to evaluate it.

## Slide 15: Main Results

Now I move to the results for the second research question.

**Click 1.** The first curve is the daily BO oracle. This is the reference where each day gets its own optimized configuration. As expected, it stays consistently high.

This tells us that the detector can perform well on most days if the configuration is adapted to the current context.

**Click 2.** The next curve is the single overall configuration. Its aggregate score looks high, around 0.95. But the day-level view shows that this average hides unstable days.

This is one of the main messages: an aggregate score can make a configuration look robust even when it fails in particular deployment contexts.

**Click 3.** The default configuration is good only on a few easier days. On other days, it drops sharply, and on day 13 it is close to zero.

So defaults are not uniformly robust when the network context changes.

**Click 4.** The 10 percent sample BO strategy reduces optimization effort, but it does not remove instability. It still has low values on several days, including early days, day 7, and day 13.

This means that under-sampling can lower optimization cost, but the sample may not preserve the information needed to choose a robust configuration.

**Click 5.** The deployment view makes the risk visible. The same risky days appear across strategies, but the performance penalty of using the wrong configuration differs.

The answer to the second research question is that simple low-budget strategies do not reliably match full reconfiguration.

## Slide 16: Takeaway

To conclude, the message is visual here.

On the left, transfer did not reliably work. A configuration optimized in one context can lose robustness when reused in another context.

On the right, the simple low-budget strategies reduce configuration effort, but they are not reliably close to full reconfiguration.

So the operational lesson is simple: for reliable AD IDS performance, it is better to reconfigure for each network context, or at least trigger reconfiguration when the context changes enough.

**Click.** As a final pointer, this related paper gives one way to make low-budget reconfiguration more guided. Instead of trying defaults or blind reuse, meta-learning suggests promising configurations to test first.

## Slide 17: Acknowledgments

I would like to acknowledge the funding support for this work.

This work received partial support from the French National Research Agency through the France 2030 initiative, under the Superviz project, ANR-22-PECY-0008.

It also received support from the Luxembourg National Research Fund under the COCTEL project.

The opinions expressed are those of the authors and do not necessarily reflect the views of the French government.

## Questions

Thank you for your attention. I would be happy to take your questions.
