import pandas as pd
import matplotlib
# We still set the backend to Agg, as Seaborn might otherwise try to use a GUI backend
matplotlib.use('Agg')
from matplotlib.figure import Figure  # <-- Import Figure directly
import seaborn as sns
import os

def visualize_data(input_file, full_report_file, leavers_report_file):
    """
    Generates and saves visualizations for the employee Churnover data.
    ... (rest of your docstring) ...
    """
    try:
        # Load all required dataframes
        df_input = pd.read_csv(input_file)
        df_full = pd.read_csv(full_report_file)
        df_leavers = pd.read_csv(leavers_report_file)
        df_input = df_input.drop(columns=['left'])
        
    except FileNotFoundError as e:
        return {"success": False, "error": f"Error loading required files during visualization: {e}"}

    try:
        # --- Aesthetic Improvements Start ---
        sns.set_style("whitegrid")
        sns.set_context("talk") # Increases font sizes and line weights for readability
        sns.set_palette("muted") # Sets a softer, professional default color palette
        # plt.rcParams is part of pyplot, so we set it on the matplotlib module
        matplotlib.rcParams['figure.dpi'] = 150
        # --- Aesthetic Improvements End ---
        
        dataset_name = os.path.splitext(os.path.basename(input_file))[0]
        output_folder = os.path.join('visualizations', dataset_name)
        os.makedirs(output_folder, exist_ok=True)

        image_paths = []
        
        df = df_full

        # 6. Total Churnover Cost KPI Card
        if 'Predicted_Churnover' in df.columns and 'Estimated_Churnover_Cost' in df.columns:
            print("Generating total Churnover cost KPI (from full_report_file)...")
            if df['Predicted_Churnover'].dtype == 'object':
                leavers_df = df[df['Predicted_Churnover'] == 'Yes']
            else:
                leavers_df = df[df['Predicted_Churnover'] == 1]
                
            total_cost = leavers_df['Estimated_Churnover_Cost'].sum()
            cost_text = f"${total_cost:,.2f}"

            # --- New OO Plot ---
            fig = Figure(figsize=(7, 3.5)) # Slightly adjusted size
            ax = fig.add_subplot(111)
            
            ax.text(0.5, 0.6, 'Total Predicted Churnover Cost',
                      ha='center', va='center', fontsize=22, color='#333333') # Darker gray
            ax.text(0.5, 0.3, cost_text,
                      ha='center', va='center', fontsize=42, color='#222222', weight='bold') # Darker black
            ax.axis('off')
            
            img_path = os.path.join(output_folder, 'total_Churnover_cost_kpi.png')
            fig.savefig(img_path, bbox_inches='tight', pad_inches=0.2) # Use fig.savefig
            abs_img_path = os.path.abspath(img_path)
            image_paths.append(abs_img_path)
            # No plt.close() needed
        else:
            print("Warning: 'Predicted_Churnover' or 'Churnover_Cost' column not found in full_report_file. Skipping KPI card.")
        
        if 'Predicted_Churnover' in df.columns:
            print("Generating Churnover percentage KPI (from full_report_file)...")
            Churnover_counts = df['Predicted_Churnover'].value_counts()
            
            if not Churnover_counts.empty:
                if df['Predicted_Churnover'].dtype == 'object':
                    leavers_count = Churnover_counts.get('Yes', 0)
                    stayers_count = Churnover_counts.get('No', 0)
                else:
                    leavers_count = Churnover_counts.get(1, 0)
                    stayers_count = Churnover_counts.get(0, 0)

                total_count = leavers_count + stayers_count
                
                if total_count > 0:
                    percent_leavers = (leavers_count / total_count) * 100
                    percent_stayers = (stayers_count / total_count) * 100
                else:
                    percent_leavers = 0.0
                    percent_stayers = 0.0

                # --- New OO Plot ---
                fig = Figure(figsize=(8, 4)) # Adjusted size
                ax = fig.add_subplot(111)
                
                ax.text(0.5, 0.75, 'Predicted Churnover Percentage',
                        ha='center', va='center', fontsize=22, color='#333333')
                ax.text(0.25, 0.45, 'To Leave',
                        ha='center', va='center', fontsize=20, color='black')
                ax.text(0.25, 0.2, f"{percent_leavers:.1f}%",
                        ha='center', va='center', fontsize=34, color='#d9534f', weight='bold') # Red color
                ax.text(0.75, 0.45, 'To Stay',
                        ha='center', va='center', fontsize=20, color='black')
                ax.text(0.75, 0.2, f"{percent_stayers:.1f}%",
                        ha='center', va='center', fontsize=34, color='#5cb85c', weight='bold') # Green color
                ax.axis('off')
                
                img_path = os.path.join(output_folder, 'Churnover_percentage_kpi.png')
                fig.savefig(img_path, bbox_inches='tight', pad_inches=0.2) # Use fig.savefig
                abs_img_path = os.path.abspath(img_path)
                image_paths.append(abs_img_path)
                # No plt.close() needed
            else:
                    print("Warning: 'Predicted_Churnover' column is empty in full_report_file. Skipping percentage KPI.")
        else:
            print("Warning: 'Predicted_Churnover' column not found in full_report_file. Skipping percentage KPI.")
            
        if 'Predicted_Churnover' in df.columns and 'efficiency_score' in df.columns:
            print("Generating efficiency vs. Churnover boxplot (from full_report_file)...")
            
            # --- New OO Plot ---
            fig = Figure(figsize=(8, 6)) # Slightly taller for readability
            ax = fig.add_subplot(111)
            # Define a semantic palette
            semantic_palette = {"Yes": "#d9534f", "No": "#5cb85c", 1: "#d9534f", 0: "#5cb85c"}
            
            # *** ADDED linewidth=1.5 ***
            sns.boxplot(x='Predicted_Churnover', y='efficiency_score', data=df, 
            hue='Predicted_Churnover',  # <-- Add this (using your x-variable)
            palette=semantic_palette, 
            ax=ax, 
            linewidth=1.5,
            legend=False)             # <-- Add this
            
            ax.set_title('Efficiency Score vs Predicted Churnover', pad=15) # Use ax.set_title
            ax.set_xlabel("Predicted Churnover") # Cleaner label
            ax.set_ylabel("Efficiency Score") # Cleaner label
            
            # *** ADDED sns.despine() for a cleaner look ***
            sns.despine(ax=ax, offset=10, trim=True)
            
            img_path = os.path.join(output_folder, 'efficiency_vs_Churnover.png')
            fig.tight_layout() # Use fig.tight_layout
            fig.savefig(img_path) # Use fig.savefig
            abs_img_path = os.path.abspath(img_path)
            image_paths.append(abs_img_path)
            # No plt.close() needed
        else:
            print("Warning: 'Predicted_Churnover' or 'efficiency_score' column not found in full_report_file. Skipping boxplot.")
            
        df = df_input
        numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
        
        # 1. Distribution plots for numeric columns
        print("Generating distribution plots (from input_file)...")
        for i, col in enumerate(numeric_cols):
            # --- New OO Plot ---
            fig = Figure(figsize=(8, 5))
            ax = fig.add_subplot(111)
            
            # *** MODIFIED histplot for better color definition ***
            # Use a base color for the bars and a thicker, default-next color for the KDE line
            sns.histplot(df[col], bins=30, kde=True, ax=ax, 
                         color=sns.color_palette("muted")[0], # Specific color for bars
                         edgecolor='w', linewidth=0.5, alpha=0.7,
                         line_kws={'linewidth': 2.5}) # Make KDE line stand out
                         
            ax.set_title(f'Distribution of {col}', pad=15) # Use ax.set_title
            ax.set_xlabel(col) # Cleaner label
            ax.set_ylabel("Frequency") # Cleaner label
            
            # *** ADDED sns.despine() for a cleaner look ***
            sns.despine(ax=ax)
            
            img_path = os.path.join(output_folder, f'distribution_{col}.png')
            fig.tight_layout() # Use fig.tight_layout
            fig.savefig(img_path) # Use fig.savefig
            abs_img_path = os.path.abspath(img_path)
            image_paths.append(abs_img_path)
            # No plt.close() needed

        # 2. Correlation heatmap
        if not numeric_cols.empty:
            print("Generating correlation heatmap (from input_file)...")
            
            # --- New OO Plot ---
            fig = Figure(figsize=(12, 10)) # Slightly larger for readability
            ax = fig.add_subplot(111)
            corr = df[numeric_cols].corr()
            
            # *** ADDED cbar_kws and annot_kws ***
            sns.heatmap(corr, annot=True, cmap='vlag', fmt=".2f", ax=ax, 
                        center=0, linewidths=.5,
                        cbar_kws={'shrink': .8}, # Make color bar slightly smaller
                        annot_kws={"size": 10}) # Control annotation font size
                        
            ax.set_title('Correlation Heatmap', pad=20) # Use ax.set_title
            
            img_path = os.path.join(output_folder, 'correlation_heatmap.png')
            fig.tight_layout() # Use fig.tight_layout
            fig.savefig(img_path) # Use fig.savefig
            abs_img_path = os.path.abspath(img_path)
            image_paths.append(abs_img_path)
            # No plt.close() needed

        print(f"Visualization plots saved in: {output_folder}")
        
        return image_paths

    except Exception as e:
        return {"success": False, "error": f"An error occurred during plot generation: {e}"}