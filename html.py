import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pathlib import Path

def create_interactive_html(data_root='PHMDC2019_Data', output_html='signal_plots.html'):
    """Create interactive HTML with signal plots and toggle buttons"""
    data_path = Path(data_root)
    
    # Find all directories containing signal files
    signal_dirs = set()
    for signal_file in data_path.glob('**/signal_*.csv'):
        signal_dirs.add(signal_file.parent)
    
    signal_dirs = sorted(signal_dirs)
    print(f"Found {len(signal_dirs)} directories with signal files")
    
    # Calculate appropriate vertical spacing
    num_rows = len(signal_dirs)
    vertical_spacing = 0.01 if num_rows > 10 else 0.02
    
    # Create subplots (one row per folder)
    fig = make_subplots(
        rows=num_rows, 
        cols=1,
        subplot_titles=[f"{d.parent.name}/{d.name}" for d in signal_dirs],
        vertical_spacing=vertical_spacing
    )
    
    # Track trace indices for each subplot
    trace_mapping = {}
    
    for idx, signal_dir in enumerate(signal_dirs, 1):
        signal_1 = signal_dir / 'signal_1.csv'
        signal_2 = signal_dir / 'signal_2.csv'
        
        # Store the starting trace index for this subplot
        current_trace_idx = len(fig.data)
        
        # Add Signal 1 traces (visible by default)
        if signal_1.exists():
            df1 = pd.read_csv(signal_1)
            fig.add_trace(
                go.Scatter(x=df1['time'], y=df1['ch1'], 
                          name=f'CH1', 
                          line=dict(color='blue', width=1), 
                          visible=True,
                          showlegend=False),
                row=idx, col=1
            )
            fig.add_trace(
                go.Scatter(x=df1['time'], y=df1['ch2'], 
                          name=f'CH2', 
                          line=dict(color='red', width=1), 
                          visible=True,
                          showlegend=False),
                row=idx, col=1
            )
        
        # Add Signal 2 traces (hidden by default)
        if signal_2.exists():
            df2 = pd.read_csv(signal_2)
            fig.add_trace(
                go.Scatter(x=df2['time'], y=df2['ch1'], 
                          name=f'CH1', 
                          line=dict(color='darkblue', width=1), 
                          visible=False,
                          showlegend=False),
                row=idx, col=1
            )
            fig.add_trace(
                go.Scatter(x=df2['time'], y=df2['ch2'], 
                          name=f'CH2', 
                          line=dict(color='darkred', width=1), 
                          visible=False,
                          showlegend=False),
                row=idx, col=1
            )
        
        # Store indices: [signal1_ch1, signal1_ch2, signal2_ch1, signal2_ch2]
        trace_mapping[idx] = list(range(current_trace_idx, len(fig.data)))
    
    # Create buttons for toggling between Signal 1 and Signal 2
    buttons = []
    
    # Button for Signal 1
    visible_signal1 = []
    for idx in range(1, num_rows + 1):
        indices = trace_mapping[idx]
        # Show first 2 traces (Signal 1), hide last 2 (Signal 2)
        visible_signal1.extend([True, True, False, False] if len(indices) == 4 else [True, True])
    
    buttons.append(dict(
        label="Signal 1",
        method="update",
        args=[{"visible": visible_signal1}]
    ))
    
    # Button for Signal 2
    visible_signal2 = []
    for idx in range(1, num_rows + 1):
        indices = trace_mapping[idx]
        # Hide first 2 traces (Signal 1), show last 2 (Signal 2)
        visible_signal2.extend([False, False, True, True] if len(indices) == 4 else [False, False])
    
    buttons.append(dict(
        label="Signal 2",
        method="update",
        args=[{"visible": visible_signal2}]
    ))
    
    # Update layout with buttons
    fig.update_layout(
        height=300 * num_rows,
        title_text="Signal Plots - Use buttons to switch between Signal 1 and Signal 2",
        updatemenus=[
            dict(
                type="buttons",
                direction="left",
                buttons=buttons,
                pad={"r": 10, "t": 10},
                showactive=True,
                x=0.0,
                xanchor="left",
                y=1.02,
                yanchor="bottom"
            )
        ]
    )
    
    # Update axes labels
    fig.update_xaxes(title_text="Time (s)")
    fig.update_yaxes(title_text="Signal Value")
    
    fig.write_html(output_html)
    print(f"Interactive HTML saved to: {output_html}")
    print(f"Total height: {300 * num_rows}px")
    print(f"Added toggle buttons for Signal 1/Signal 2")

if __name__ == "__main__":
    create_interactive_html(
        data_root="/Users/darrylad/Darryl/Research/18. Fatigue Crack Growth in Aluminum Lap Joint",
        output_html="signal_plots.html"
    )