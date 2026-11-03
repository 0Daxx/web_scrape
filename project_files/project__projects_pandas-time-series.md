Pandas Time Series
beginner

Pandas Time Series
==================

Learn how Pandas handles dates and times using a vehicle sales dataset.

Start building, submit solution and get feedback from the community.

Start Working
### Project Description

In this project, you will learn how Pandas handles dates and times by working with a **light vehicle sales dataset** from FRED (Federal Reserve Economic Data). You will not build any model; the focus is entirely on understanding time series data structures and the Pandas tools that come with them.

### Project Requirements

* Load the vehicle sales CSV from [FRED](https://fred.stlouisfed.org/series/LTOTALNSA) into a Pandas DataFrame
* Parse the date column and set it as the index
* Create a date range using `pd.date_range()` and understand frequency strings (`D`, `W`, `M`)
* Resample the data to monthly and quarterly totals
* Shift the series by one period and compute period-over-period differences
* Plot the original series and the rolling mean on the same chart

### Technologies to Use

* Python
* Pandas
* Matplotlib
* Jupyter Notebook

### What You Will Learn

You will understand how `DatetimeIndex` works, how to use `.resample()`, `.shift()`, `.rolling()`, and `.diff()`, and why differencing is useful when working with financial or sales data. This project prepares you to work on any time series problem.

### Want to See a Solution?

A full walkthrough of this project, including different tools to conduct time series in Python, is available on Towards Data Science: 🔗 [Time Series From Scratch — Introduction with Pandas](https://towardsdatascience.com/time-series-from-scratch-introduction-to-time-series-with-pandas-347ac9c6b451/?utm_source=roadmap&utm_medium=Referral&utm_campaign=TDS+roadmap+integration)

