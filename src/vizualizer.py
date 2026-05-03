import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D


def create_visual() -> None:
    """
    Generates an aesthetic Probability Scale graphic using source file colors.

    The function reads the aggregated results, maps colors to source files,
    and plots them on a 0.0-1.0 horizontal axis with formatted labels.
    """
    # Define paths relative to the script location
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    prob_file = os.path.join(base_dir, 'output', 'probabilities.csv')

    if not os.path.exists(prob_file):
        print("Error: output/probabilities.csv not found. Please run processor.py first!")
        return

    # Load and sort data for a cleaner vertical progression on the plot
    df = pd.read_csv(prob_file).sort_values(by='probability')

    # Setup the visual style
    plt.figure(figsize=(13, 7))
    plt.style.use('ggplot')  # Using a clean, modern grid style

    # Assign distinct colors to each unique source file
    unique_files = df['source_file'].unique()
    colors_list = ['#2ecc71', '#3498db', '#e67e22', '#9b59b6']
    file_to_color = {file: colors_list[i % len(colors_list)] for i, file in enumerate(unique_files)}
    point_colors = [file_to_color[f] for f in df['source_file']]

    # Draw horizontal guide lines for each data point
    plt.hlines(y=range(len(df)), xmin=0, xmax=1, color='lightgray', linestyle='--', zorder=1)

    # Plot the probability points
    plt.scatter(
        df['probability'],
        range(len(df)),
        s=250,
        c=point_colors,
        edgecolors='white',
        linewidth=1.5,
        zorder=3
    )

    # Annotate points with event descriptions and percentage values
    for i, (idx, row) in enumerate(df.iterrows()):
        # Event title above the point
        plt.text(row['probability'], i + 0.15, f"{row['event']}",
                 ha='center', va='bottom', fontsize=10, fontweight='bold')
        # Percentage value below the point
        plt.text(row['probability'], i - 0.3, f"{row['probability']:.1%}",
                 ha='center', va='top', fontsize=9, color='dimgray')

    # Configure axes and labels
    plt.xlim(-0.05, 1.05)
    plt.ylim(-1, len(df))
    plt.xlabel('Probability (0.0 to 1.0)', fontsize=12, fontweight='bold', labelpad=15)
    plt.title('RMK Internship Challenge: Probability Scale', fontsize=16, pad=25, fontweight='bold')
    plt.yticks([])  # Hide Y-axis as it's used only for vertical spacing

    # Create a custom legend for source file tracking (Data Provenance)
    legend_elements = [
        Line2D([0], [0], marker='o', color='w', label=f,
               markerfacecolor=color, markersize=12)
        for f, color in file_to_color.items()
    ]
    plt.legend(handles=legend_elements, title="Source Files", loc='lower right', frameon=True)

    # Add intuitive zones (Rare, Possible, Likely)
    plt.axvspan(0, 0.33, color='grey', alpha=0.05)
    plt.text(0.16, len(df) - 0.5, 'UNLIKELY', color='grey', alpha=0.4,
             ha='center', fontsize=14, fontweight='bold')
    plt.text(0.5, len(df) - 0.5, 'POSSIBLE', color='grey', alpha=0.4,
             ha='center', fontsize=14, fontweight='bold')
    plt.text(0.84, len(df) - 0.5, 'HIGHLY LIKELY', color='grey', alpha=0.4,
             ha='center', fontsize=14, fontweight='bold')

    plt.tight_layout()

    # Export the final graphic
    output_path = os.path.join(base_dir, 'output', 'probability_scale.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Scale successfully saved to: {output_path}")
    plt.show()


if __name__ == "__main__":
    create_visual()