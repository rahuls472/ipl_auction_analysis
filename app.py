from flask import Flask,render_template,request
from mydb import ipl_auction
ipl= ipl_auction()
import plotly.io as pio


app = Flask(__name__)


@app.route('/')
def Home():
    return render_template('index.html')

@app.route('/Player_list',methods = ['post'])
def player_list():
    player_name = request.form.get('Player_name')
    result = ipl.PlayerDetail(player_name)

    return render_template('index.html',message = result)


@app.route('/Top_Player')
def Top_Player():
    return render_template('top_players.html')



@app.route('/fetch_top_player', methods=['post'])
def fetch_top_player():
    year = request.form.get('Year')
    result = ipl.TopPlayersINYear(int(year))
    result2 = ipl.camparison(int(year)).to_html(full_html=False)  # Convert the plotly figure to HTML
    result3 = ipl.HighestPaidPlayerPerTeam(int(year)).to_dict(orient="records")  # Ensure dictionary format

    return render_template('top_players.html', message=result, chart=result2, highest=result3)




@app.route('/TotalSpending')
def TotalSpending():
    return render_template('team_spending.html')



@app.route('/fetch_teams',methods = ['post'])
def fetch_teams():
    year = request.form.get('Year')
    result = ipl.TeamSpending(int(year))
    result2 = ipl.yearly_auction_trends().to_html(full_html=False)


    return render_template('team_spending.html', message = result,bar = result2)


@app.route('/budget_split')
def Budget_split():
    return render_template('BudgetSplit.html')



@app.route('/budget_split_Origin', methods=['POST'])
def Budget_split__origin():
    year = int(request.form.get('Year'))
    TeamName = request.form.get('TeamName')
    
    # Get the data table and both figures
    result = ipl.SpendingDistribution(year, TeamName)
    fig_role, fig_origin = ipl.SpendingDistributionGraph(year, TeamName)
    
    # Convert figures to HTML for embedding in the template
    chart_role = pio.to_html(fig_role, full_html=False)
    chart_origin = pio.to_html(fig_origin, full_html=False)
    
    return render_template('BudgetSplit.html', message=result, chart_role=chart_role, chart_origin=chart_origin)
