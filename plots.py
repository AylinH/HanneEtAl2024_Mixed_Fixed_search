from matplotlib.pylab import plt
from matplotlib.lines import Line2D
import pandas as pd


# Adapted from https://bambinos.github.io/bambi/notebooks/hierarchical_binomial_bambi.html

def plot_prior_predictive(data, prior, axes=None, color='blue', draw_data=True):
    if "correct" in data.columns:
        count = data["count"].values
        correct = data["correct"].values
        name = "Observed proportion"
        titlename = "Prior probability of correct reports"
    elif "yes_number" in data.columns:
        count = data["count"].values
        yes_number = data["yes_number"].values
        name = "Observed proportion"
        titlename = "Prior probability of reports"
    elif "difference" in data.columns:
        data["difference"] = pd.to_numeric(data["difference"])
        data['difference'] = data['difference'].apply(lambda x: round(x, 2))
        difference = data["difference"].values
        name = "Observed difference"
        titlename = "Prior probability of the difference"

    fig = None
    if axes is None:
        if "yes_number" in data.columns:
            fig, axes = plt.subplots(1, 3, figsize=(10, 2), sharex="col")
        else:
            fig, axes = plt.subplots(7, 3, figsize=(10, 10), sharex="col") #5, 6
    

    for idx, ax in enumerate(axes.ravel()):
        if "correct" in data.columns:
            pps = prior.sel({"p(correct, count)_obs": idx})
            ct = count[idx]
            c = correct[idx]
            hist = ax.hist(pps / ct, bins=25, color=color, alpha=0.3)
            if draw_data:
                ax.axvline(c / ct, color="red", lw=2)
        elif "yes_number" in data.columns:
            pps = prior.sel({"p(yes_number, count)_obs": idx})
            ct = count[idx]
            c = yes_number[idx]
            hist = ax.hist(pps / ct, bins=25, color=color, alpha=0.3)
            if draw_data:
                ax.axvline(c / ct, color="red", lw=2)
        else:
            pps = prior.sel({"difference_obs": idx})
            diff = difference[idx]
            hist = ax.hist(pps, bins=25, color=color, alpha=0.3)
            if draw_data:
                ax.axvline(diff, color="red", lw=2)
            
            
        ax.set_yticks([])
        ax.tick_params(labelsize=12)
        
    if fig is not None:
        if "yes_number" in data.columns:
            fig.subplots_adjust(left=0.025, right=0.975, hspace=0.05, wspace=0.05, bottom=0.125)
            custom_lines = [Line2D([0], [0], color="red", lw=4, label= name),
                    Line2D([0], [0], color="blue", lw=4, label='Default prior'),
                    Line2D([0], [0], color="green", lw=4, label='Custom prior')]
            fig.legend(                   
                handles= custom_lines,
                handlelength=1.5,
                handletextpad=0.8,
                borderaxespad=0,
                frameon=True,
                fontsize=11, 
                bbox_to_anchor=(0.975, 1.1),
                loc="right"

            )
        elif "difference" in data.columns:
            fig.subplots_adjust(left=0.025, right=0.975, hspace=0.05, wspace=0.05, bottom=0.1)
            custom_lines = [Line2D([0], [0], color="red", lw=4, label= name),
                    Line2D([0], [0], color="blue", lw=4, label='Default prior')]
            fig.legend(                   
                handles= custom_lines,
                handlelength=1.5,
                handletextpad=0.8,
                borderaxespad=0,
                frameon=True,
                fontsize=11, 
                bbox_to_anchor=(0.975, 0.95),
                loc="right"

            )
        else:
            fig.subplots_adjust(left=0.025, right=0.975, hspace=0.05, wspace=0.05, bottom=0.1)
            custom_lines = [Line2D([0], [0], color="red", lw=4, label= name),
                    Line2D([0], [0], color="blue", lw=4, label='Default prior'),
                    Line2D([0], [0], color="green", lw=4, label='Custom prior')]
            fig.legend(                   
                handles= custom_lines,
                handlelength=1.5,
                handletextpad=0.8,
                borderaxespad=0,
                frameon=True,
                fontsize=11, 
                bbox_to_anchor=(0.975, 0.95),
                loc="right"

            )
            
        title = titlename
        if "yes_number" in data.columns:
            fig.text(0.5, -0.15, title, fontsize=15, ha="center", va="baseline")
        else:
            fig.text(0.5, 0.025, title, fontsize=15, ha="center", va="baseline")
    return axes
