import numpy as np
import pandas as pd
from bokeh.models import Slope
from bokeh.plotting import figure, show
from bokeh.models import  ColumnDataSource, PrintfTickFormatter, DatetimeTickFormatter
from bokeh.layouts import column
from bokeh.models.tickers import MonthsTicker

# Load the dataset from a CSV file into a pandas DataFrame
df_kl = pd.read_csv('dataset/Kaiserslautern_new.csv', parse_dates=['date'], index_col='date')

# Function to create a temperature chart
def create_temperature_chart(df, width=900):
    # Create a Bokeh figure with specified width and height
    p = figure(width=width, height=400, title='Temperature Chart',
               tools=['xwheel_zoom'],
               x_axis_type="datetime", x_axis_location="above", y_range=(-15, 40))

    # Create a ColumnDataSource from the DataFrame
    source = ColumnDataSource(df)

    # Customize the appearance of the temperature chart
    p.title.text_color = "navy"
    p.title.text_font = "times"

    # Plot maximum and minimum temperatures with legend labels
    p.line(source=source, x='date', y='tempmax', legend_label="Maximum Temperature",
           line_color="red", line_width=1)
    p.line(source=source, x='date', y='tempmin', legend_label="Minimum Temperature", line_color="navy",
           line_width=1)

    # Customize the legend
    p.legend.location = "top_left"
    p.varea(source=source, x='date', y1='feelslikemax', y2='feelslikemin', color="green", alpha=0.3,
            legend_label="Feels Like Range")
    p.legend.title = "Temperature Legend"
    p.legend.label_text_font = "times"
    p.legend.label_text_font_style = "italic"
    p.legend.label_text_color = "navy"
    p.legend.border_line_width = 3
    p.legend.border_line_color = "navy"
    p.legend.border_line_alpha = 0.8
    p.legend.background_fill_color = "navy"
    p.legend.background_fill_alpha = 0.001

    # Customize the x-axis, y-axis, and overall appearance
    p.xaxis.ticker = MonthsTicker(months=list(range(1, 13)))
    p.xgrid.ticker = MonthsTicker(months=list(range(1, 13)))
    p.xaxis.formatter = DatetimeTickFormatter(months="%b")
    p.xaxis.major_label_text_align = 'right'
    p.yaxis[0].formatter = PrintfTickFormatter(format="%2i°")
    p.yaxis.axis_label = "Temperature [°C]"
    p.yaxis.axis_label_text_font = "times"
    p.yaxis.axis_label_text_font_style = "italic"
    p.title.text_font_size = "18pt"
    p.title.align = "center"
    p.yaxis.axis_label_text_font_size = "14pt"

    return p

# Function to create a humidity chart
def create_humidity_chart(df, width=900):
    # Create a Bokeh figure with specified width and height
    p = figure(title="Humidity", width=width, height=200, tools=['xwheel_zoom'], x_axis_type="datetime")

    # Plot humidity over time
    p.line(source=df, x='date', y='humidity')

    # Customize the appearance of the humidity chart
    p.title.text_color = "navy"
    p.title.text_font = "times"
    p.xaxis.ticker = MonthsTicker(months=list(range(1, 13)))
    p.xgrid.ticker = MonthsTicker(months=list(range(1, 13)))
    p.xaxis.formatter = DatetimeTickFormatter(months="%b")
    p.xaxis.major_label_text_align = 'right'
    p.yaxis.axis_label = "Humidity"
    p.yaxis.axis_label_text_font = "times"
    p.yaxis.axis_label_text_font_style = "italic"
    p.yaxis.axis_label_text_font_size = "14pt"
    p.title.text_font_size = "19pt"
    p.title.align = "center"

    return p

# Function to create a scatter plot
def create_scatter_plot(df, width=900):
    # Create a Bokeh figure with specified width and height
    p = figure(width=width, height=800, title='Wind Speed vs. Feels Like Temperature Difference',
               tools=['pan', 'box_zoom', 'reset'],
               x_axis_label="Wind Speed ",
               y_axis_label="Feels Like Temperature Difference [°C]")

    # Create a ColumnDataSource from the DataFrame
    source = ColumnDataSource(df)
    source.data['temp_diff'] = abs(df['feelslike'] - df['temp'])
    source.data['month'] = df.index.month
    source.data['color'] = np.where(source.data['month'].isin(range(4, 10)), 'yellow', 'blue')

    # Scatter plot
    p.circle(x='windspeedmean', y='temp_diff', source=source, size=8, color='color', alpha=0.5)
    p.add_layout(Slope(gradient=0.17, y_intercept=0,
                     line_color='orange', line_dash='dashed', line_width=2.5
                    ))

    # Formatting
    p.title.text_color = "navy"
    p.title.text_font = "times"
    p.title.text_font_size = "16pt"
    p.title.align = "center"
    p.yaxis[0].formatter = PrintfTickFormatter(format="%2i°")
    p.x_range.start = 0
    p.x_range.end = 40
    p.yaxis.axis_label_text_font = "times"
    p.yaxis.axis_label_text_font_style = "italic"
    p.yaxis.axis_label_text_font_size = "14pt"
    p.yaxis.axis_label_text_font = "times"
    p.xaxis.axis_label_text_font_style = "italic"
    p.xaxis.axis_label_text_font_size = "14pt"

    return p

# Show the plots in a column layout
show(column(create_temperature_chart(df_kl), create_humidity_chart(df_kl), create_scatter_plot(df_kl)))
