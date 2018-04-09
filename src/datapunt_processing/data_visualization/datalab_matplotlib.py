# For setting parameters, use matplotlib (mpl) directly
import matplotlib as mpl
import matplotlib.image as image # for Gemeente logo
import matplotlib.pyplot as plt
from matplotlib.rcsetup import cycler # 
import brewer2mpl # pip install brewer2mpl

# look at the map @http://colorbrewer2.org, pick a set and map to a variable
gmap = brewer2mpl.get_map('YlOrRd', 'Sequential', 7)
colors= gmap.mpl_colors

# Pretty plotting settings
mpl.rcParams['figure.figsize'] = (10, 6)
mpl.rcParams['figure.dpi'] = 150
mpl.rcParams['axes.color_cycle'] = colors
mpl.rcParams['lines.linewidth'] = 2
mpl.rcParams['axes.facecolor'] = 'white'
mpl.rcParams['font.size'] = 14
mpl.rcParams['patch.edgecolor'] = 'white'
mpl.rcParams['patch.facecolor'] = colors[0]
mpl.rcParams['font.family'] = 'StixGeneral'


def datalab_default(axes=None, top=False, right=False, left=True, bottom=True, 
                  grid=None, title=None, add_datalab_logo = None):
    """
    Produces a clean default Matplotlib plot with minimize chartjunk 
    Args:
        axes: axes to be used for the plot
        top, right, left, bottom: keywords toggle whether the corresponding plot border is drawn
        grid : grid to be shown in plot. Default is False
        title: title to be shon on top of the plot. Default is False
        add_datalab_logo: if True places Gemeente logo in the plot (bottom_left)
    returns
        an empty axes object on which data can be plotted
    """
    ax = axes or plt.gca()
    ax.spines['top'].set_visible(top)
    ax.spines['right'].set_visible(right)
    ax.spines['left'].set_visible(left)
    ax.spines['bottom'].set_visible(bottom)
    
    #turn off all ticks
    ax.yaxis.set_ticks_position('none')
    ax.xaxis.set_ticks_position('none')
    
    #re-enable visibles for tweaking
    if top:
        ax.xaxis.tick_top()
    if bottom:
        ax.xaxis.tick_bottom()
    if left:
        ax.yaxis.tick_left()
    if right:
        ax.yaxis.tick_right()
    
    if grid is not None:
        for g in grid:
            assert g in ('x', 'y')
            ax.grid(axis=grid, color='gray', linestyle='--', linewidth=0.3, alpha=.6)
    
    if title:
        ax.set_title(label = title)
    
    if add_datalab_logo:
        # adding Gemeente Watermark Image on the bottom-left of the plot
        logo = image.imread('AMS.jpg')
        ax.figure.figimage(logo, 60, -20, alpha=.2, zorder=1)
    
    return ax