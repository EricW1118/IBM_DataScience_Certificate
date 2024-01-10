import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

# Initialize the Dash app
app = dash.Dash(__name__)

# Load the data using pandas
data = pd.read_csv(
    "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv"
)

# List of years
year_list = [i for i in range(1980, 2024, 1)]

# Create the layout of the app
app.layout = html.Div(
    [
        # TASK 2.1 Add title to the dashboard
        html.H1(
            children="Automobile Sales Statistics Dashboard",
            style={"textAlign": "center", "color": "#503D36", "font-size": 24},
        ),  # May include style for title
        html.Div(
            [  # TASK 2.2: Add two dropdown menus
                html.Label("Select Statistics:"),
                dcc.Dropdown(
                    id="dropdown-statistics",
                    options=[
                        {"label": "Yearly Statistics", "value": "Yearly Statistics"},
                        {
                            "label": "Recession Period Statistics",
                            "value": "Recession Period Statistics",
                        },
                    ],
                    value="Select Statistics",
                    placeholder="Select a report type",
                    style={
                        "padding": 3,
                        "width": "80vw",
                        "font-size": 20,
                        "text-align-last": "center",
                    },
                ),
            ]
        ),
        html.Div(
            dcc.Dropdown(
                id="select-year",
                options=[{"label": i, "value": i} for i in year_list],
                # value="...................",
                style={
                    "padding": 3,
                    "width": "80vw",
                    "font-size": 20,
                    "text-align-last": "center",
                },
            )
        ),
        html.Div(
            [  # TASK 2.3: Add a division for output display
                html.Div(
                    id="output-container",
                    className="chart-grid",
                    style={"display": "flex"},
                ),
            ]
        ),
    ]
)


# Callback for first dropdown statistics
@app.callback(
    Output(component_id="select-year", component_property="disabled"),
    Input(component_id="dropdown-statistics", component_property="value"),
)
def update_input_container(selected_item):
    """callback logic"""
    if selected_item == "Yearly Statistics":
        return False
    return True


# ---------------------------------
@app.callback(
    Output(component_id="output-container", component_property="children"),
    [
        Input(component_id="select-year", component_property="value"),
        Input(component_id="dropdown-statistics", component_property="value"),
    ],
)
def update_output_container(year, statistic_type):
    """callback logic"""
    if statistic_type == "Recession Period Statistics":
        # Filter the data for recession periods
        recession_data = data[data["Recession"] == 1]
        yearly_rec = (
            recession_data.groupby("Year")["Automobile_Sales"].sum().reset_index()
        )
        rchart1 = dcc.Graph(
            figure=px.line(
                yearly_rec,
                x="Year",
                y="Automobile_Sales",
                title="Automobile Sales fluctuation over Recession Period",
            )
        )

        # Plot 2 Calculate the average number of vehicles sold by vehicle type
        # use groupby to create relevant data for plotting

        average_sales = (
            recession_data.groupby(["Year", "Vehicle_Type"])["Automobile_Sales"]
            .mean()
            .reset_index()
        )
        rchart2 = dcc.Graph(
            figure=px.line(
                average_sales,
                x="Year",
                y="Automobile_Sales",
                color="Vehicle_Type",
                title="Avarage Automobile Sales fluctuation over Recession Period",
            )
        )

        # Plot 3 Pie chart for total expenditure share by vehicle type during recessions
        # use groupby to create relevant data for plotting
        exp_rec = (
            recession_data.groupby(["Vehicle_Type"])["Advertising_Expenditure"]
            .sum()
            .reset_index()
        )
        rchart3 = dcc.Graph(
            figure=px.pie(
                exp_rec,
                values="Advertising_Expenditure",
                names="Vehicle_Type",
                title="Total advertising expenditure of vehicle type over recessions",
            )
        )

        # Plot 4 bar chart for the effect of unemployment rate on vehicle type and sales
        unemployment_rec = (
            recession_data.groupby(["Vehicle_Type", "unemployment_rate"])[
                "Automobile_Sales"
            ]
            .sum()
            .reset_index()
        )
        rchart4 = dcc.Graph(
            figure=px.bar(
                unemployment_rec,
                x="unemployment_rate",
                y="Automobile_Sales",
                color="Vehicle_Type",
                title="Effect of unemployment rate on vehicle type and sales",
                # barmode="group"
            )
        )
        return [
            html.Div(
                className="recession_figures1",
                children=[html.Div(children=rchart1), html.Div(children=rchart2)],
            ),
            html.Div(
                className="recession_figures2",
                children=[html.Div(children=rchart3), html.Div(children=rchart4)],
            ),
        ]
    # TASK 2.6: Create and display graphs for Yearly Report Statistics
    # Yearly Statistic Report Plots
    elif year and statistic_type == "Yearly Statistics":
        # plot 1 Yearly Automobile sales using line chart for the whole period.
        yas = data.groupby("Year")["Automobile_Sales"].sum().reset_index()
        y_chart1 = dcc.Graph(
            figure=px.line(
                yas,
                x="Year",
                y="Automobile_Sales",
                title="Automobile Sales fluctuation over whole Period",
            )
        )
        yearly_data = data[data["Year"] == year]

        month_dict = {
            "Jan": 1,
            "Feb": 2,
            "Mar": 3,
            "Apr": 4,
            "May": 5,
            "Jun": 6,
            "Jul": 7,
            "Aug": 8,
            "Sep": 9,
            "Oct": 10,
            "Nov": 11,
            "Dec": 12,
        }
        month_sale = (
            yearly_data.groupby("Month")["Automobile_Sales"].sum().reset_index()
        )

        month_sale = month_sale.sort_values(
            "Month", key=lambda x: x.apply(lambda x: month_dict[x])
        )
        y_chart2 = dcc.Graph(
            figure=px.line(
                month_sale,
                x="Month",
                y="Automobile_Sales",
                title=f"Automobile Sales fluctuation in {year}".format(year=year),
            )
        )

        # Plot bar chart for average number of vehicles sold during the given year
        avr_vdata = (
            yearly_data.groupby("Month")["Automobile_Sales"].mean().reset_index()
        )
        avr_vdata = avr_vdata.sort_values(
            "Month", key=lambda x: x.apply(lambda x: month_dict[x])
        )

        y_chart3 = dcc.Graph(
            figure=px.bar(
                avr_vdata,
                x="Month",
                y="Automobile_Sales",
                title=f"Average Vehicles Sold by Vehicle Type in the year {year}".format(
                    year
                ),
                # barmode="group"
            )
        )

        # Total Advertisement Expenditure for each vehicle using pie chart
        exp_data = (
            yearly_data.groupby(["Vehicle_Type"])["Advertising_Expenditure"]
            .sum()
            .reset_index()
        )
        y_chart4 = dcc.Graph(
            figure=px.pie(
                exp_data,
                values="Advertising_Expenditure",
                names="Vehicle_Type",
                title=f"Total advertising expenditure of vehicle type in {year}".format(
                    year=year
                ),
            )
        )
        # TASK 2.6: Returning the graphs for displaying Yearly data
        return [
            html.Div(className="Year_figure1", children=[y_chart1, y_chart2]),
            html.Div(className="Year_figure2", children=[y_chart3, y_chart4]),
        ]

    return None


if __name__ == "__main__":
    app.run_server(debug=True)
