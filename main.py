import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

def plot_signal_file(csv_path):
    """Plot a single signal CSV file with time on x-axis and ch1, ch2 on y-axis"""
    # Read the CSV
    df = pd.read_csv(csv_path)
    
    # Create the plot
    plt.figure(figsize=(12, 6))
    plt.plot(df['time'], df['ch1'], label='CH1', color='blue', linewidth=0.8)
    plt.plot(df['time'], df['ch2'], label='CH2', color='red', linewidth=0.8)
    
    plt.xlabel('Time (s)')
    plt.ylabel('Signal Value')
    plt.title(f'Signal Plot: {csv_path.parent.parent.name}/{csv_path.parent.name}/{csv_path.name}')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    return plt.gcf()

def plot_all_signals(data_root='PHMDC2019_Data', save_plots=True, show_plots=False):
    """
    Plot all signal files in the dataset
    
    Parameters:
    - data_root: Root directory of the dataset
    - save_plots: If True, save plots to 'plots' folder
    - show_plots: If True, display plots interactively (slower)
    """
    data_path = Path(data_root)
    
    # Create output directory
    if save_plots:
        output_dir = Path('plots')
        output_dir.mkdir(exist_ok=True)
    
    # Find all signal CSV files
    signal_files = list(data_path.glob('**/signal_*.csv'))
    
    print(f"Found {len(signal_files)} signal files")
    
    for i, signal_file in enumerate(signal_files, 1):
        print(f"Processing {i}/{len(signal_files)}: {signal_file}")
        
        try:
            # Plot the signal
            fig = plot_signal_file(signal_file)
            
            # Save the plot
            if save_plots:
                # Create organized output path
                relative_path = signal_file.relative_to(data_path)
                output_path = output_dir / f"{relative_path.parent.parent.name}_{relative_path.parent.name}_{signal_file.stem}.png"
                output_path.parent.mkdir(parents=True, exist_ok=True)
                fig.savefig(output_path, dpi=150, bbox_inches='tight')
                print(f"  Saved to: {output_path}")
            
            # Show the plot
            if show_plots:
                plt.show()
            
            plt.close(fig)
            
        except KeyboardInterrupt:
            print("\nStopped by user")
            plt.close('all')
            break

        except Exception as e:
            print(f"  Error processing {signal_file}: {e}")

if __name__ == "__main__":
    # Plot all signals and save to 'plots' folder
    plot_all_signals(data_root="/Users/darrylad/Darryl/Research/18. Fatigue Crack Growth in Aluminum Lap Joint", save_plots=True, show_plots=False)