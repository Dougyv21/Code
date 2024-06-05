# Libraries #
import pandas
import getpass
import datetime

# Credentials #
Username = getpass.getuser()

# Utility #
Year = datetime.date.today().year

# Filepaths #
InputPath = rf'C:\Users\{Username}\RSM\Audit Innovation - Documents (1)\Pipeline\Stock Volatility Calculator\Python Input.xlsx'
OutputPath = rf'C:\Users\{Username}\RSM\Audit Innovation - Documents (1)\Pipeline\Stock Volatility Calculator\Python Output.xlsx'

# Sheet name with current year #
SheetName = f'{Year} - Volatility Updates (6)'

# Input Data #
DF = pandas.read_excel(InputPath)
DF['Date'] = pandas.to_datetime(DF['Date']).dt.date

# Pulling list from dataframe column #
Tickers = DF['Ticker'].drop_duplicates().to_list()

# Getting volatility for each stock #
AllVolatilityDF = DF[['Ticker', 'Observations Per Year', 'Historical Volatility']].drop_duplicates()

# Removing columns #
DF = DF.drop(columns = ['Observations Per Year', 'Historical Volatility'])

# Initialize start positon #
StartPos = 0

# Create a Pandas Excel writer using XlsxWriter as the engine.
with pandas.ExcelWriter(OutputPath, engine = 'xlsxwriter') as Writer:
    
    # Workbook object #
    Workbook = Writer.book    
    
    # Formats #
    InfoFmt = Workbook.add_format({'align': 'left', 'border': 1})

    ProceeduresFmt = Workbook.add_format({'align': 'left', 'left': 1, 'right': 1})
    
    StockFmt = Workbook.add_format({'align': 'center'})
    
    TickerFmt = Workbook.add_format({'bold': True, 'bg_color': '#C6E0B4', 'align': 'center', 'bottom': 1})
    
    RedStrFmt = Workbook.add_format({'bold': True, 'font_color': 'red'})
    
    ObservationsFmt = Workbook.add_format({'bg_color': '#FFFF00'})
    
    VolatilityFmt = Workbook.add_format({'bg_color': '#00FFFF', 'num_format': '0.00%'})
    
    # Adding data and formatting for all tickers #
    for Ticker in Tickers:
        
        # Filter to current ticker #
        TickerDF = DF[DF['Ticker'] == Ticker].drop(columns = ['Ticker'])
        
        # Number of columns + accounting for index #
        ColCount = TickerDF.shape[1] - 1
        
        # Getting volatility for current ticker #
        VolatilityDF = AllVolatilityDF[AllVolatilityDF['Ticker'] == Ticker]
        Observations = VolatilityDF['Observations Per Year'].values[0]
        Volatility = VolatilityDF['Historical Volatility'].values[0]
        
        # Write the data tp excel and get worksheet object #
        TickerDF.to_excel(Writer, sheet_name = SheetName, index = False, startrow = 18, startcol = StartPos)
        Worksheet = Writer.sheets[SheetName]        
        
        # Observations Per Year #
        Worksheet.write(12, StartPos, 'Observations Per Year')
        Worksheet.write(12, StartPos + ColCount, Observations, ObservationsFmt)
        
        # Computed Volatility #
        Worksheet.write(13, StartPos, 'Computed Volatility')
        Worksheet.write(13, StartPos + ColCount, Volatility, VolatilityFmt)
        
        # Stock name/ticker header #
        Worksheet.merge_range(16, StartPos, 16, StartPos + ColCount, 'Placeholder for company name', StockFmt)
        Worksheet.merge_range(17, StartPos, 17, StartPos + ColCount, f'Ticker: {Ticker}', TickerFmt)
        
        # Update column start position #
        StartPos += ColCount + 2
    
    # Finding aggregate values if there are more than one ticker #
    if len(Tickers) > 1:
        
        # Aggregates #
        Max = AllVolatilityDF['Historical Volatility'].max()
        Min = AllVolatilityDF['Historical Volatility'].min()
        Mean = AllVolatilityDF['Historical Volatility'].mean()
        Median = AllVolatilityDF['Historical Volatility'].median()
        
        # Aggregates Header #
        Worksheet.merge_range('O3:P3', 'Volatility KPIs', StockFmt)
        
        # Mean #
        Worksheet.write('O4', 'Mean')
        Worksheet.write('P4', Mean)
        
        # Median #
        Worksheet.write('O5', 'Median')
        Worksheet.write('P5', Median)
        
        # Max #
        Worksheet.write('O6', 'High')
        Worksheet.write('P6', Max)
        
        # Min #
        Worksheet.write('O7', 'Low')
        Worksheet.write('P7', Min)
    
    # Purpose String #
    Worksheet.merge_range('B2:M2', 'Purpose: The purpose of this workpaper is to conduct the Black sholes model for options granted in 2021.', InfoFmt)
    
    # Proceedures String #
    Worksheet.merge_range('B3:M3', 'Procedures: The purpose of this workpaper is to conduct the Black sholes model for options granted in 2021.')
    Worksheet.merge_range('B4:M4', '1) RSM went to Yahoo finance.com and obtained historical weekly data from the grant date going back 4 years from that date.')
    Worksheet.merge_range('B5:M5', '2) RSM exported this data and inserted the dates and cost below.')
    Worksheet.merge_range('B6:M6', '3) RSM exported all dividends issued over the time period and entered them below.')
    Worksheet.merge_range('B7:M7', '4) RSM used the results of this model to populate table on tab (3)')
    
    # Conclusion String #
    Worksheet.merge_range('B8:M8', 'Conclusion: See Summary Tab (1) for conclusions reached.', InfoFmt)
    
    # Red String #
    Worksheet.merge_range('A10:I10', '** Pull historical data from Yahoo Finance - Need Weekly Data of prices and Dividends **', RedStrFmt)