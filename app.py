# -*- coding: utf-8 -*-
"""
Created on Mon Jul 15 22:42:49 2024

@author: Mafu
"""

from flask import Flask, render_template, request
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json

app = Flask(__name__)

def generate_break_even_chart(initial_investment, profit, profit_type):
    if profit_type == "Monthly":
        periods = initial_investment / profit
        time_unit = "Months"
        x = np.arange(1, int(periods) + 12)
    else:
        periods = initial_investment / profit
        time_unit = "Years"
        x = np.arange(1, int(periods) + 2)
    
    y = profit * x
    roi = y - initial_investment

    # Convert numpy arrays to lists for JSON serialization
    x = x.tolist()
    y = y.tolist()
    roi = roi.tolist()

    fig = go.Figure()
    
    # Add traces for accumulated profit and ROI
    fig.add_trace(
        go.Scatter(x=x, y=y, name="Accumulated Profit", line=dict(color='blue'))
    )
    fig.add_trace(
        go.Scatter(x=x, y=roi, name="ROI", line=dict(color='orange', dash='dash'))
    )
    
    # Add horizontal line for initial investment
    fig.add_hline(y=initial_investment, line_dash="dash", line_color="red",
                  annotation_text=f"Initial Investment (${initial_investment:,.2f})")
    
    # Add vertical line for break-even point
    fig.add_vline(x=periods, line_dash="dash", line_color="green",
                  annotation_text=f"Break-even point ({periods:.2f} {time_unit})")

    fig.update_layout(
        title='Break-Even Analysis',
        xaxis_title=time_unit,
        yaxis_title='Amount ($)',
        hovermode='x unified',
        showlegend=True,
        plot_bgcolor='white',
        xaxis=dict(showgrid=True, gridcolor='lightgray'),
        yaxis=dict(showgrid=True, gridcolor='lightgray')
    )

    return json.dumps(fig.to_dict())

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            initial_investment = float(request.form['initial_investment'])
            profit = float(request.form['profit'])
            profit_type = request.form['profit_type']

            periods = initial_investment / profit
            period_label = f"{periods:.2f} {'Months' if profit_type == 'Monthly' else 'Years'}"
            
            chart_data = generate_break_even_chart(initial_investment, profit, profit_type)
            
            return render_template('index.html', 
                                break_even_period=period_label,
                                chart_data=chart_data)
        except ValueError:
            return render_template('index.html', error="Please enter valid numbers")
        except ZeroDivisionError:
            return render_template('index.html', error="Profit cannot be zero")
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
