import pandas as pd
import numpy as np
import plotly.express as px

class ipl_auction:
   def PlayerDetail(self, name):
    ipl = pd.read_csv('/home/ghost/Python DS/Ipl_auction/IPLPlayerAuctionData.csv')
    # Filter players based on the provided name, case-insensitive
    detail = ipl[ipl['Player'].str.contains(name, case=False, na=False)]
    
    # Convert to a list of dictionaries for easy rendering in templates
    return detail.to_dict(orient="records")


   def TopPlayersINYear(self,year):
      ipl = pd.read_csv('/home/ghost/Python DS/Ipl_auction/IPLPlayerAuctionData.csv')
      # Filter by the specified year
      data = ipl[ipl['Year'] == year]
      # Sort by Amount in descending order and take the top 10
      top_players = data.sort_values(by='Amount', ascending=False).head(10)
      return top_players.to_dict(orient="records")
   


   def TeamSpending(self,year):
    ipl = pd.read_csv('/home/ghost/Python DS/Ipl_auction/IPLPlayerAuctionData.csv')
    
    # Filter data by the specified year
    data = ipl[ipl['Year'] == year]
    
    # Group by 'Team' and calculate total spending per team
    df2 = data.groupby('Team')['Amount'].sum().reset_index()
    df2.columns = ['Team', 'TotalAmountSpent']
    df2['Year'] = year  # Add the year as a column for context

    # Convert to list of dictionaries for easy rendering in template
    return df2.to_dict(orient="records")

   def camparison(self,year):
    ipl = pd.read_csv('/home/ghost/Python DS/Ipl_auction/IPLPlayerAuctionData.csv')
    data = ipl[ipl['Year'] == year]
    df1 = data.groupby(['Year','Player Origin'])['Amount'].mean().reset_index()
    fig = px.pie(
        df1,
        values='Amount',
        names='Player Origin',
        title="Average Amount Spent on Players by Origin ({year})",
        color_discrete_sequence=['skyblue', 'orange']  # Custom colors for each category
    )
    return fig
   

   def yearly_auction_trends(self):
    ipl = pd.read_csv('/home/ghost/Python DS/Ipl_auction/IPLPlayerAuctionData.csv')
    # Group by 'Year' and sum the 'Amount' for each year
    df2 = ipl.groupby('Year')['Amount'].sum().reset_index()

    # Plot with Plotly
    fig = px.bar(
        df2,
        x='Year',
        y='Amount',
        title="Yearly Auction Spending Trends in IPL",
        labels={'Amount': 'Total Amount Spent (₹)', 'Year': 'Year'},
        color_discrete_sequence=['#1f77b4']  # Custom color for the bars
    )

    fig.update_layout(
        xaxis=dict(dtick=1),  # Ensure one bar per year on the x-axis if all years are integers
        yaxis_title="Total Amount Spent (₹)"
    )
    
    return fig
   


   def SpendingDistribution(self,year, name):
    ipl = pd.read_csv('/home/ghost/Python DS/Ipl_auction/IPLPlayerAuctionData.csv')

    # Filter data for the specified year and team
    df1 = ipl[(ipl['Year'] == year) & (ipl['Team'] == name)]
    
    # Group by 'Player Origin', 'Team', and 'Role' to get the spending amount
    df2 = df1.groupby(['Player Origin','Team', 'Role'])['Amount'].sum().reset_index()
    
    return df2.to_dict(orient="records")
   




   def SpendingDistributionGraph(self, year, name):
    ipl = pd.read_csv('/home/ghost/Python DS/Ipl_auction/IPLPlayerAuctionData.csv')

    # Filter data for the specified year and team
    df1 = ipl[(ipl['Year'] == year) & (ipl['Team'] == name)]
    
    # Group by 'Player Origin', 'Team', and 'Role' to get the spending amount by role
    df2 = df1.groupby(['Player Origin', 'Team', 'Role'])['Amount'].sum().reset_index()

    # Create the Plotly pie chart for spending by role
    fig_role = px.pie(
        df2,
        values='Amount',
        names='Role',
        title=f"Spending Distribution by Role for {name} in {year}",
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig_role.update_traces(textinfo='percent+label')
    fig_role.update_layout(
        legend_title_text='Player Role',
        title_x=0.5
    )

    # Group by 'Player Origin' to get spending amount by origin
    df_origin = df1.groupby('Player Origin')['Amount'].sum().reset_index()

    # Create the Plotly pie chart for spending by player origin
    fig_origin = px.pie(
        df_origin,
        values='Amount',
        names='Player Origin',
        title=f"Spending Distribution by Player Origin for {name} in {year}",
        color_discrete_sequence=['skyblue', 'orange']
    )
    fig_origin.update_traces(textinfo='percent+label')
    fig_origin.update_layout(
        legend_title_text='Player Origin',
        title_x=0.5
    )

    # Return both figures
    return fig_role, fig_origin
   

   def HighestPaidPlayerPerTeam(self,year):
    # Load data
    ipl = pd.read_csv('/home/ghost/Python DS/Ipl_auction/IPLPlayerAuctionData.csv')

    # Filter for the specified year
    filter1 = ipl[ipl['Year'] == year]
    
    # Sort by Amount in descending order to get the highest paid players at the top
    sorted_data = filter1.sort_values(by='Amount', ascending=False)
    
    # Drop duplicate entries for each team to keep only the highest-paid player per team
    highest_paid = sorted_data.drop_duplicates(subset='Team', keep='first')
    
    # Select only relevant columns for clarity
    result = highest_paid[['Team', 'Player', 'Amount']].reset_index(drop=True)
    
    return result