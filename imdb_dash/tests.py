import dash
from dash import Dash, dcc, html, dash_table, Input, Output, State
import pandas as pd

# Load the data
df = pd.read_csv("/Users/grow/Documents/DashLearning/assets/payments.csv")

# Step 1: Aggregate Parent and Child Data
parent_data = df.groupby("segment", as_index=False).agg({"sum": "sum"})
parent_data["level"] = "parent"
parent_data["id"] = parent_data["segment"]  # Unique ID for parent rows

child_data = df.groupby(["segment", "user_id"], as_index=False).agg({"sum": "sum"})
child_data["level"] = "child"
child_data["id"] = child_data["segment"] + "_" + child_data["user_id"].astype(str)

# Add a "parent_id" column to link children to their parent
child_data["parent_id"] = child_data["segment"]

# Combine parent and child data
combined_data = pd.concat([parent_data, child_data], ignore_index=True)

# Step 2: Dash App
app = Dash(__name__)

# Initial table data (only parents visible)
initial_data = combined_data[combined_data["level"] == "parent"]

app.layout = html.Div(
    style={
        "maxWidth": "900px",
        "margin": "auto",
        "padding": "20px",
        "fontFamily": "Arial, sans-serif",
        "backgroundColor": "#f8f9fa",
    },
    children=[
        html.H1(
            "Collapsible Dash DataTable",
            style={
                "textAlign": "center",
                "color": "#343a40",
                "marginBottom": "20px",
            },
        ),
        dash_table.DataTable(
            id="collapsible-table",
            columns=[
                {"name": "Segment", "id": "segment"},
                {"name": "Sum", "id": "sum"},
                {"name": "User ID", "id": "user_id"},
            ],
            data=initial_data.to_dict("records"),
            style_data={
                "border": "1px solid #dee2e6",
                "backgroundColor": "#ffffff",
                "color": "#343a40",
            },
            style_data_conditional=[
                # Style child rows
                {
                    "if": {"filter_query": "{level} = 'child'"},
                    "padding-left": "30px",
                    "backgroundColor": "#f1f3f5",
                    "color": "#495057",
                    "fontStyle": "italic",
                },
                # Style parent rows
                {
                    "if": {"filter_query": "{level} = 'parent'"},
                    "backgroundColor": "#e9ecef",
                    "fontWeight": "bold",
                    "color": "#212529",
                },
                # Highlight on hover
                {
                    "if": {"state": "active"},
                    "backgroundColor": "#d1ecf1",
                    "color": "#0c5460",
                },
            ],
            style_header={
                "backgroundColor": "#343a40",
                "color": "#ffffff",
                "fontWeight": "bold",
                "border": "1px solid #dee2e6",
            },
            style_table={
                "overflowX": "auto",
                "border": "1px solid #ced4da",
                "borderRadius": "5px",
            },
            style_cell={
                "padding": "10px",
                "textAlign": "left",
                "fontSize": "14px",
            },
        ),
        html.Div(
            id="debug-output",
            style={"marginTop": "20px", "fontSize": "12px", "color": "#6c757d"},
        ),
    ],
)

# Callback to manage collapsible rows
@app.callback(
    Output("collapsible-table", "data"),
    Input("collapsible-table", "active_cell"),
    State("collapsible-table", "data"),
)
def update_table(active_cell, current_data):
    if not active_cell:
        return current_data  # No cell clicked

    # Get the clicked row
    clicked_row = current_data[active_cell["row"]]
    if clicked_row["level"] == "parent":
        # Determine if children are already visible
        segment = clicked_row["segment"]
        children = combined_data[(combined_data["parent_id"] == segment)]
        children_visible = any(row in current_data for row in children.to_dict("records"))

        if children_visible:
            # Remove children from the table
            return [row for row in current_data if row["parent_id"] != segment]
        else:
            # Add children to the table
            children_rows = children.to_dict("records")
            row_index = current_data.index(clicked_row) + 1
            return current_data[:row_index] + children_rows + current_data[row_index:]

    return current_data


if __name__ == "__main__":
    app.run_server(debug=True)
