#!/usr/bin/env python3

import re
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.gridspec import GridSpec, GridSpecFromSubplotSpec
import numpy as np
import sys
import os
mpl.use('svg')
import seaborn as sns

LABELS = {
    10: ['NH3', 'CAB1', 'PHE1', 'AMD1', 'CAB2',
         'PHE2', 'AMD2', 'CAB3', 'PHE3', 'COO'],
    11: ['NH3', 'CA1', 'PHA1', 'PHB1', 'PHC1', 'AMD1',
         'CA2', 'PHA2', 'PHB2', 'PHC2', 'COO'],
    16: ['NH3', 'CA1', 'PHA1', 'PHB1', 'PHC1', 'AMD1',
         'CA2', 'PHA2', 'PHB2', 'PHC2', 'AMD2',
         'CA3', 'PHA3', 'PHB3', 'PHC3', 'COO'],
    21: ['NH3', 'CA1', 'PHA1', 'PHB1', 'PHC1', 'AMD1',
         'CA2', 'PHA2', 'PHB2', 'PHC2', 'AMD2',
         'CA3', 'PHA3', 'PHB3', 'PHC3', 'AMD3',
         'CA4', 'PHA4', 'PHB4', 'PHC4', 'COO'],
}

F2_SIZES = {10, 11}
F4_SIZES = {16, 21}

F2_CMAP = sns.color_palette("plasma_r", as_cmap=True)
F2_CMAP.set_under('w')
F4_CMAP = sns.color_palette("mako_r", as_cmap=True)
F4_CMAP.set_under('w')

TICK_FONTSIZE   =  7   # regular axis tick labels
PH_FONTSIZE     =  8   # condensed PHE ring labels (bold)
HEADER_FONTSIZE = 10   # AA/CG/BA, 32/64 headers
PEP_ID_FONTSIZE = 13   # F2/F4 group headers
CBAR_FONTSIZE   = 10   # colorbar tick labels and axis label

# Annotation offsets in points (absolute), tuned for 8.5×11" canvas
OFFSET_PEP_ID   = 15   # peptide-ID header above axes top
OFFSET_RES      = 3   # resolution header between pep-ID and axes
OFFSET_ROW      = -38  # row-count label left of axes left edge


def condense_labels(labels):
    """Replace PHA*/PHC* with '' and PHB* with 'PH<n>'."""
    result = []
    for lbl in labels:
        m = re.match(r'PH([ABC])(\d+)', lbl)
        if m:
            letter, num = m.group(1), m.group(2)
            result.append(f'PHE{num}' if letter == 'B' else '')
        else:
            result.append(lbl)
    return result


def style_ph_labels(texts):
    """Make condensed PH<n> tick-label Text objects bold and larger."""
    for text in texts:
        if re.match(r'PHE\d+', text.get_text()):
            text.set_fontsize(PH_FONTSIZE)
            text.set_fontweight('bold')


files = sys.argv[1:]

cmaps_data = []
for path in files:
    with open(path) as f:
        cmaps_data.append(np.loadtxt(f, dtype='<i4'))

# Log-transform for display: compresses dynamic range across resolutions.
# log1p(0) = 0, so zero-contact cells remain below vmin and render white.
cmaps_log = [np.log1p(cm.astype(float)) for cm in cmaps_data]

nrows, ncols = 4, 3

f2_idx = [i for i, cm in enumerate(cmaps_data) if len(cm) in F2_SIZES]
f4_idx = [i for i, cm in enumerate(cmaps_data) if len(cm) in F4_SIZES]


def group_range(indices):
    # vmin = log1p(1) so cells with count 0 fall below and render white
    vmin = np.log1p(1.0)
    vmax = max(np.max(cmaps_log[i]) for i in indices)
    return float(vmin), float(vmax)


f2_vmin, f2_vmax = group_range(f2_idx)
f4_vmin, f4_vmax = group_range(f4_idx)

f2_rows = sorted({i // ncols for i in f2_idx})
f4_rows = sorted({i // ncols for i in f4_idx})
f2_bottom    = max(f2_rows)
f4_bottom    = max(f4_rows)
f2_first_row = min(f2_rows)
f4_first_row = min(f4_rows)


def parse_stem(file_idx):
    stem = os.path.splitext(os.path.basename(files[file_idx]))[0]
    pep_count, _ = stem.split('_', 1)
    peptide_id, count = pep_count.split('x')
    return peptide_id, count


# ── Layout ────────────────────────────────────────────────────────────────────
fig = plt.figure(figsize=(8.5, 10))
outer_gs = GridSpec(2, 1, hspace=0.32, figure=fig)
f2_gs = GridSpecFromSubplotSpec(2, ncols, subplot_spec=outer_gs[0],
                                hspace=0.05, wspace=0.05)
f4_gs = GridSpecFromSubplotSpec(2, ncols, subplot_spec=outer_gs[1],
                                hspace=0.05, wspace=0.05)

axes = np.empty((nrows, ncols), dtype=object)
for c in range(ncols):
    axes[0, c] = fig.add_subplot(f2_gs[0, c])
    axes[1, c] = fig.add_subplot(f2_gs[1, c])
    axes[2, c] = fig.add_subplot(f4_gs[0, c])
    axes[3, c] = fig.add_subplot(f4_gs[1, c])

f2_last_im = None
f4_last_im = None

for idx in range(nrows * ncols):
    row = idx // ncols
    col = idx % ncols
    ax  = axes[row, col]

    if idx >= len(files):
        ax.set_visible(False)
        continue

    contactmap = cmaps_data[idx]
    n = len(contactmap)
    user_labels = LABELS[n]
    is_f2 = n in F2_SIZES

    cmap = F2_CMAP if is_f2 else F4_CMAP
    vmin = f2_vmin if is_f2 else f4_vmin
    vmax = f2_vmax if is_f2 else f4_vmax

    im = ax.imshow(cmaps_log[idx], origin="lower", cmap=cmap, vmin=vmin, vmax=vmax)

    if is_f2:
        f2_last_im = im
    else:
        f4_last_im = im

    # Remove all tick marks, keep labels.
    ax.tick_params(axis='both', length=0)

    # X tick labels: bottom row of each group only, condensed, PH styled.
    show_x = (is_f2 and row == f2_bottom) or (not is_f2 and row == f4_bottom)
    ax.set_xticks(np.arange(n))
    x_texts = ax.set_xticklabels(condense_labels(user_labels) if show_x else [],
                                  rotation=90, fontsize=TICK_FONTSIZE)
    if show_x:
        style_ph_labels(x_texts)

    # Y tick labels: leftmost column only, condensed, PH styled.
    ax.set_yticks(np.arange(n))
    y_texts = ax.set_yticklabels(condense_labels(user_labels) if col == 0 else [],
                                  fontsize=TICK_FONTSIZE)
    if col == 0:
        style_ph_labels(y_texts)

# ── Column resolution headers — below each peptide ID header ─────────────────
for first_row in [f2_first_row, f4_first_row]:
    for col, label in enumerate(['AA', 'CG', 'BA']):
        axes[first_row, col].annotate(
            label,
            xy=(0.5, 1.0), xycoords='axes fraction',
            xytext=(0, OFFSET_RES), textcoords='offset points',
            ha='center', va='bottom', fontsize=HEADER_FONTSIZE, fontweight='bold',
            annotation_clip=False,
        )

# ── Peptide ID group headers — topmost, above resolution headers ──────────────
for first_row in [f2_first_row, f4_first_row]:
    peptide_id, _ = parse_stem(first_row * ncols)
    axes[first_row, 1].annotate(
        peptide_id,
        xy=(0.5, 1.0), xycoords='axes fraction',
        xytext=(0, OFFSET_PEP_ID), textcoords='offset points',
        ha='center', va='bottom', fontsize=PEP_ID_FONTSIZE, fontweight='bold',
        annotation_clip=False,
    )

# ── Row subheaders (peptide count) ────────────────────────────────────────────
for row_idx in range(nrows):
    file_idx = row_idx * ncols
    if file_idx >= len(files):
        continue
    _, count = parse_stem(file_idx)
    axes[row_idx, 0].annotate(
        count,
        xy=(0, 0.5), xycoords='axes fraction',
        xytext=(OFFSET_ROW, 0), textcoords='offset points',
        ha='right', va='center', fontsize=HEADER_FONTSIZE, fontweight='bold',
        annotation_clip=False,
    )

# ── Shared colorbars ──────────────────────────────────────────────────────────
def add_colorbar(fig, im, ax_list, vmin, vmax):
    # Ticks at log1p of round original counts; labels show the original counts.
    orig_max = int(np.round(np.expm1(vmax)))
    raw_ticks = np.unique(np.round(np.linspace(1, orig_max, 6)).astype(int))
    log_ticks = np.log1p(raw_ticks.astype(float))
    cbar = fig.colorbar(im, ax=ax_list, ticks=log_ticks, use_gridspec=False)
    cbar.ax.set_yticklabels([str(t) for t in raw_ticks])
    cbar.ax.tick_params(labelsize=CBAR_FONTSIZE, length=0)
    cbar.ax.get_yaxis().labelpad = 8
    cbar.ax.set_ylabel('# of contacts', rotation=270, fontsize=CBAR_FONTSIZE)


add_colorbar(fig, f2_last_im, list(axes[:2, :].flat), f2_vmin, f2_vmax)
add_colorbar(fig, f4_last_im, list(axes[2:, :].flat), f4_vmin, f4_vmax)

plt.savefig('contactmap.png', dpi=300, bbox_inches='tight')
