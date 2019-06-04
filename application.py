import flask

import numpy as np
import pandas as pd
import datetime

from flask import Flask, render_template, jsonify, request
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.io import show
from bokeh.models import ColumnDataSource

app = flask.Flask(__name__)

def GenerateGanttChartData(projectData, InputWorkPackageStatus, InputDepartment, InputFromDate, InputToDate):
    df = projectData.loc[(projectData['Work Package Status'] == InputWorkPackageStatus) &
       ((projectData['Dpt 1 Department'] == InputDepartment) | (projectData['Dpt 2 Department'] == InputDepartment)  | 
            (projectData['Dpt 3 Department'] == InputDepartment) | (projectData['Dpt 4 Department'] == InputDepartment) )]
    df = df[['Name', 'Project Number', 'Project Manager', 'Program Manager', 'Location', 'CS Contact', 'Work Package Status',
         'Dpt 1 Department', 'Dpt 1 Committed Hrs',
         'Dpt 1 Start Date Placeholder', 'Dpt 1 Start Date Original Planned', 'Dpt 1 Start Date Forecast', 'Dpt 1 Start Date Actual',
         'Dpt 1 End Date Placeholder', 'Dpt 1 End Date Original Planned', 'Dpt 1 End Date Forecast', 'Dpt 1 End Date Actual',
         'Dpt 2 Department', 'Dpt 2 Committed Hrs',
         'Dpt 2 Start Date Placeholder', 'Dpt 2 Start Date Original Planned', 'Dpt 2 Start Date Forecast', 'Dpt 2 Start Date Actual',
         'Dpt 2 End Date Placeholder', 'Dpt 2 End Date Original Planned', 'Dpt 2 End Date Forecast', 'Dpt 2 End Date Actual',
         'Dpt 3 Department', 'Dpt 3 Committed Hrs',
         'Dpt 3 Start Date Placeholder', 'Dpt 3 Start Date Original Planned', 'Dpt 3 Start Date Forecast', 'Dpt 3 Start Date Actual',
         'Dpt 3 End Date Placeholder', 'Dpt 3 End Date Original Planned', 'Dpt 3 End Date Forecast', 'Dpt 3 End Date Actual',
         'Dpt 4 Department', 'Dpt 4 Committed Hrs',
         'Dpt 4 Start Date Placeholder', 'Dpt 4 Start Date Original Planned', 'Dpt 4 Start Date Forecast', 'Dpt 4 Start Date Actual',
         'Dpt 4 End Date Placeholder', 'Dpt 4 End Date Original Planned', 'Dpt 4 End Date Forecast', 'Dpt 4 End Date Actual',
         'Overall Committed Hrs', 
         'Overall Start Date Placeholder', 'Overall Start Date Original Planned', 'Overall Start Date Forecast', 'Overall Start Date Actual',
         'Overall Completion Date Placeholder', 'Overall Completion Date Original Planned', 'Overall Completion Date Forecast', 'Overall Completion Date Actual'         
        ]]
    df1 = df
    df1['Commited Hours'] = 0
    df1['Start Date'] = pd.NaT
    df1['End Date'] = pd.NaT
    df1['Department Number'] = 0
    df1['Start Date Type'] = ''
    df1['End Date Type'] = ''

    for i in df.index:
        if df.at[i, 'Dpt 1 Department'] == InputDepartment: 

            if not pd.isnull(df.at[i, 'Dpt 1 Start Date Actual']):
                df.at[i, 'Start Date'] = df.at[i, 'Dpt 1 Start Date Actual']
                df.at[i, 'Start Date Type'] = DateTypeActual            
            elif not pd.isnull(df.at[i, 'Dpt 1 Start Date Forecast']):
                df.at[i, 'Start Date'] = df.at[i, 'Dpt 1 Start Date Forecast']    
                df.at[i, 'Start Date Type'] = DateTypeForecast                
            elif not pd.isnull(df.at[i, 'Dpt 1 Start Date Original Planned']):
                df.at[i, 'Start Date'] = df.at[i, 'Dpt 1 Start Date Original Planned']        
                df.at[i, 'Start Date Type'] = DateTypeOriginalPlanned                
            elif not pd.isnull(df.at[i, 'Dpt 1 Start Date Placeholder']):
                df.at[i, 'Start Date'] = df.at[i, 'Dpt 1 Start Date Placeholder']     
                df.at[i, 'Start Date Type'] = DateTypePlaceholder                
            elif not pd.isnull(df.at[i, 'Overall Start Date Actual']):
                df.at[i, 'Start Date'] = df.at[i, 'Overall Start Date Actual']
                df.at[i, 'Start Date Type'] = DateTypeActual                
            elif not pd.isnull(df.at[i, 'Overall Start Date Forecast']):
                df.at[i, 'Start Date'] = df.at[i, 'Overall Start Date Forecast']        
                df.at[i, 'Start Date Type'] = DateTypeForecast                
            elif not pd.isnull(df.at[i, 'Overall Start Date Original Planned']):
                df.at[i, 'Start Date'] = df.at[i, 'Overall Start Date Original Planned']        
                df.at[i, 'Start Date Type'] = DateTypeOriginalPlanned                
            else:
                df.at[i, 'Start Date'] = df.at[i, 'Overall Start Date Placeholder']            
                df.at[i, 'Start Date Type'] = DateTypePlaceholder                

            if not pd.isnull(df.at[i, 'Dpt 1 End Date Actual']):
                df.at[i, 'End Date'] = df.at[i, 'Dpt 1 End Date Actual']
                df.at[i, 'End Date Type'] = DateTypeActual   
            elif not pd.isnull(df.at[i, 'Dpt 1 End Date Forecast']):
                df.at[i, 'End Date'] = df.at[i, 'Dpt 1 End Date Forecast']      
                df.at[i, 'End Date Type'] = DateTypeForecast               
            elif not pd.isnull(df.at[i, 'Dpt 1 End Date Original Planned']):
                df.at[i, 'End Date'] = df.at[i, 'Dpt 1 End Date Original Planned']        
                df.at[i, 'End Date Type'] = DateTypeOriginalPlanned               
            elif not pd.isnull(df.at[i, 'Dpt 1 End Date Placeholder']):
                df.at[i, 'End Date'] = df.at[i, 'Dpt 1 End Date Placeholder']     
                df.at[i, 'End Date Type'] = DateTypePlaceholder               
            elif not pd.isnull(df.at[i, 'Overall Completion Date Actual']):
                df.at[i, 'End Date'] = df.at[i, 'Overall Completion Date Actual']
                df.at[i, 'End Date Type'] = DateTypeActual               
            elif not pd.isnull(df.at[i, 'Overall Completion Date Forecast']):
                df.at[i, 'End Date'] = df.at[i, 'Overall Completion Date Forecast']        
                df.at[i, 'End Date Type'] = DateTypeForecast               
            elif not pd.isnull(df.at[i, 'Overall Completion Date Original Planned']):
                df.at[i, 'End Date'] = df.at[i, 'Overall Completion Date Original Planned']        
                df.at[i, 'End Date Type'] = DateTypeOriginalPlanned               
            else:
                df.at[i, 'End Date'] = df.at[i, 'Overall Completion Date Placeholder']                  
                df.at[i, 'End Date Type'] = DateTypePlaceholder               

            df.at[i, 'Department Number'] = 1

            if not pd.isnull(df.at[i, 'Dpt 1 Committed Hrs']):
                df.at[i, 'Commited Hours'] = df.at[i, 'Dpt 1 Committed Hrs']
            else:
                df.at[i, 'Commited Hours'] = df.at[i, 'Overall Committed Hrs']                    

        elif df.at[i, 'Dpt 2 Department'] == InputDepartment: 

            if not pd.isnull(df.at[i, 'Dpt 2 Start Date Actual']):
                df.at[i, 'Start Date'] = df.at[i, 'Dpt 2 Start Date Actual']
                df.at[i, 'Start Date Type'] = DateTypeActual                        
            elif not pd.isnull(df.at[i, 'Dpt 2 Start Date Forecast']):
                df.at[i, 'Start Date'] = df.at[i, 'Dpt 2 Start Date Forecast']        
                df.at[i, 'Start Date Type'] = DateTypeForecast                        
            elif not pd.isnull(df.at[i, 'Dpt 2 Start Date Original Planned']):
                df.at[i, 'Start Date'] = df.at[i, 'Dpt 2 Start Date Original Planned']        
                df.at[i, 'Start Date Type'] = DateTypeOriginalPlanned                        
            elif not pd.isnull(df.at[i, 'Dpt 2 Start Date Placeholder']):
                df.at[i, 'Start Date'] = df.at[i, 'Dpt 2 Start Date Placeholder']     
                df.at[i, 'Start Date Type'] = DateTypePlaceholder                        
            elif not pd.isnull(df.at[i, 'Overall Start Date Actual']):
                df.at[i, 'Start Date'] = df.at[i, 'Overall Start Date Actual']
                df.at[i, 'Start Date Type'] = DateTypeActual                        
            elif not pd.isnull(df.at[i, 'Overall Start Date Forecast']):
                df.at[i, 'Start Date'] = df.at[i, 'Overall Start Date Forecast']        
                df.at[i, 'Start Date Type'] = DateTypeForecast                        
            elif not pd.isnull(df.at[i, 'Overall Start Date Original Planned']):
                df.at[i, 'Start Date'] = df.at[i, 'Overall Start Date Original Planned']     
                df.at[i, 'Start Date Type'] = DateTypeOriginalPlanned                        
            else:
                df.at[i, 'Start Date'] = df.at[i, 'Overall Start Date Placeholder']            
                df.at[i, 'Start Date Type'] = DateTypePlaceholder                        

            if not pd.isnull(df.at[i, 'Dpt 2 End Date Actual']):
                df.at[i, 'End Date'] = df.at[i, 'Dpt 2 End Date Actual']
                df.at[i, 'End Date Type'] = DateTypeActual              
            elif not pd.isnull(df.at[i, 'Dpt 2 End Date Forecast']):
                df.at[i, 'End Date'] = df.at[i, 'Dpt 2 End Date Forecast']        
                df.at[i, 'End Date Type'] = DateTypeForecast              
            elif not pd.isnull(df.at[i, 'Dpt 2 End Date Original Planned']):
                df.at[i, 'End Date'] = df.at[i, 'Dpt 2 End Date Original Planned']        
                df.at[i, 'End Date Type'] = DateTypeOriginalPlanned              
            elif not pd.isnull(df.at[i, 'Dpt 2 End Date Placeholder']):
                df.at[i, 'End Date'] = df.at[i, 'Dpt 2 End Date Placeholder']     
                df.at[i, 'End Date Type'] = DateTypePlaceholder              
            elif not pd.isnull(df.at[i, 'Overall Completion Date Actual']):
                df.at[i, 'End Date'] = df.at[i, 'Overall Completion Date Actual']
                df.at[i, 'End Date Type'] = DateTypeActual              
            elif not pd.isnull(df.at[i, 'Overall Completion Date Forecast']):
                df.at[i, 'End Date'] = df.at[i, 'Overall Completion Date Forecast']        
                df.at[i, 'End Date Type'] = DateTypeForecast              
            elif not pd.isnull(df.at[i, 'Overall Completion Date Original Planned']):
                df.at[i, 'End Date'] = df.at[i, 'Overall Completion Date Original Planned']        
                df.at[i, 'End Date Type'] = DateTypeOriginalPlanned              
            else:
                df.at[i, 'End Date'] = df.at[i, 'Overall Completion Date Placeholder']                       
                df.at[i, 'End Date Type'] = DateTypePlaceholder              

            df.at[i, 'Department Number'] = 2        

            if not pd.isnull(df.at[i, 'Dpt 2 Committed Hrs']):
                df.at[i, 'Commited Hours'] = df.at[i, 'Dpt 2 Committed Hrs']
            else:
                df.at[i, 'Commited Hours'] = df.at[i, 'Overall Committed Hrs']            

        elif df.at[i, 'Dpt 3 Department'] == InputDepartment: 

            if not pd.isnull(df.at[i, 'Dpt 3 Start Date Actual']):
                df.at[i, 'Start Date'] = df.at[i, 'Dpt 3 Start Date Actual']
                df.at[i, 'Start Date Type'] = DateTypeActual               
            elif not pd.isnull(df.at[i, 'Dpt 3 Start Date Forecast']):
                df.at[i, 'Start Date'] = df.at[i, 'Dpt 3 Start Date Forecast']     
                df.at[i, 'Start Date Type'] = DateTypeForecast                             
            elif not pd.isnull(df.at[i, 'Dpt 3 Start Date Original Planned']):
                df.at[i, 'Start Date'] = df.at[i, 'Dpt 3 Start Date Original Planned']
                df.at[i, 'Start Date Type'] = DateTypeOriginalPlanned
            elif not pd.isnull(df.at[i, 'Dpt 3 Start Date Placeholder']):
                df.at[i, 'Start Date'] = df.at[i, 'Dpt 3 Start Date Placeholder']     
                df.at[i, 'Start Date Type'] = DateTypePlaceholder            
            elif not pd.isnull(df.at[i, 'Overall Start Date Actual']):
                df.at[i, 'Start Date'] = df.at[i, 'Overall Start Date Actual']
                df.at[i, 'Start Date Type'] = DateTypeActual
            elif not pd.isnull(df.at[i, 'Overall Start Date Forecast']):
                df.at[i, 'Start Date'] = df.at[i, 'Overall Start Date Forecast']        
                df.at[i, 'Start Date Type'] = DateTypeForecast            
            elif not pd.isnull(df.at[i, 'Overall Start Date Original Planned']):
                df.at[i, 'Start Date'] = df.at[i, 'Overall Start Date Original Planned']        
                df.at[i, 'Start Date Type'] = DateTypeOriginalPlanned            
            else:
                df.at[i, 'Start Date'] = df.at[i, 'Overall Start Date Placeholder']            
                df.at[i, 'Start Date Type'] = DateTypePlaceholder            

            if not pd.isnull(df.at[i, 'Dpt 3 End Date Actual']):
                df.at[i, 'End Date'] = df.at[i, 'Dpt 3 End Date Actual']
                df.at[i, 'End Date Type'] = DateTypeActual               
            elif not pd.isnull(df.at[i, 'Dpt 3 End Date Forecast']):
                df.at[i, 'End Date'] = df.at[i, 'Dpt 3 End Date Forecast']        
                df.at[i, 'End Date Type'] = DateTypeForecast               
            elif not pd.isnull(df.at[i, 'Dpt 3 End Date Original Planned']):
                df.at[i, 'End Date'] = df.at[i, 'Dpt 3 End Date Original Planned']        
                df.at[i, 'End Date Type'] = DateTypeOriginalPlanned               
            elif not pd.isnull(df.at[i, 'Dpt 3 End Date Placeholder']):
                df.at[i, 'End Date'] = df.at[i, 'Dpt 3 End Date Placeholder']     
                df.at[i, 'End Date Type'] = DateTypePlaceholder               
            elif not pd.isnull(df.at[i, 'Overall Completion Date Actual']):
                df.at[i, 'End Date'] = df.at[i, 'Overall Completion Date Actual']
                df.at[i, 'End Date Type'] = DateTypeActual               
            elif not pd.isnull(df.at[i, 'Overall Completion Date Forecast']):
                df.at[i, 'End Date'] = df.at[i, 'Overall Completion Date Forecast']        
                df.at[i, 'End Date Type'] = DateTypeForecast               
            elif not pd.isnull(df.at[i, 'Overall Completion Date Original Planned']):
                df.at[i, 'End Date'] = df.at[i, 'Overall Completion Date Original Planned']        
                df.at[i, 'End Date Type'] = DateTypeOriginalPlanned               
            else:
                df.at[i, 'End Date'] = df.at[i, 'Overall Completion Date Placeholder']            
                df.at[i, 'End Date Type'] = DateTypePlaceholder               

            df.at[i, 'Department Number'] = 3

            if not pd.isnull(df.at[i, 'Dpt 3 Committed Hrs']):
                df.at[i, 'Commited Hours'] = df.at[i, 'Dpt 3 Committed Hrs']
            else:
                df.at[i, 'Commited Hours'] = df.at[i, 'Overall Committed Hrs']            

        elif df.at[i, 'Dpt 4 Department'] == InputDepartment: 

            if not pd.isnull(df.at[i, 'Dpt 4 Start Date Actual']):
                df.at[i, 'Start Date'] = df.at[i, 'Dpt 4 Start Date Actual']
                df.at[i, 'Start Date Type'] = DateTypeActual                 
            elif not pd.isnull(df.at[i, 'Dpt 4 Start Date Forecast']):
                df.at[i, 'Start Date'] = df.at[i, 'Dpt 4 Start Date Forecast']        
                df.at[i, 'Start Date Type'] = DateTypeForecast                 
            elif not pd.isnull(df.at[i, 'Dpt 4 Start Date Original Planned']):
                df.at[i, 'Start Date'] = df.at[i, 'Dpt 4 Start Date Original Planned']        
                df.at[i, 'Start Date Type'] = DateTypeOriginalPlanned                 
            elif not pd.isnull(df.at[i, 'Dpt 4 Start Date Placeholder']):
                df.at[i, 'Start Date'] = df.at[i, 'Dpt 4 Start Date Placeholder']     
                df.at[i, 'Start Date Type'] = DateTypePlaceholder                 
            elif not pd.isnull(df.at[i, 'Overall Start Date Actual']):
                df.at[i, 'Start Date'] = df.at[i, 'Overall Start Date Actual']
                df.at[i, 'Start Date Type'] = DateTypeActual                 
            elif not pd.isnull(df.at[i, 'Overall Start Date Forecast']):
                df.at[i, 'Start Date'] = df.at[i, 'Overall Start Date Forecast']        
                df.at[i, 'Start Date Type'] = DateTypeForecast                 
            elif not pd.isnull(df.at[i, 'Overall Start Date Original Planned']):
                df.at[i, 'Start Date'] = df.at[i, 'Overall Start Date Original Planned']        
                df.at[i, 'Start Date Type'] = DateTypeOriginalPlanned                 
            else:
                df.at[i, 'Start Date'] = df.at[i, 'Overall Start Date Placeholder']            
                df.at[i, 'Start Date Type'] = DateTypePlaceholder            

            if not pd.isnull(df.at[i, 'Dpt 4 End Date Actual']):
                df.at[i, 'End Date'] = df.at[i, 'Dpt 4 End Date Actual']
                df.at[i, 'End Date Type'] = DateTypeActual            
            elif not pd.isnull(df.at[i, 'Dpt 4 End Date Forecast']):
                df.at[i, 'End Date'] = df.at[i, 'Dpt 4 End Date Forecast']
                df.at[i, 'End Date Type'] = DateTypeForecast            
            elif not pd.isnull(df.at[i, 'Dpt 4 End Date Original Planned']):
                df.at[i, 'End Date'] = df.at[i, 'Dpt 4 End Date Original Planned']
                df.at[i, 'End Date Type'] = DateTypeOriginalPlanned            
            elif not pd.isnull(df.at[i, 'Dpt 4 End Date Placeholder']):
                df.at[i, 'End Date'] = df.at[i, 'Dpt 4 End Date Placeholder']
                df.at[i, 'End Date Type'] = DateTypePlaceholder            
            elif not pd.isnull(df.at[i, 'Overall Completion Date Actual']):
                df.at[i, 'End Date'] = df.at[i, 'Overall Completion Date Actual']
                df.at[i, 'End Date Type'] = DateTypeActual            
            elif not pd.isnull(df.at[i, 'Overall Completion Date Forecast']):
                df.at[i, 'End Date'] = df.at[i, 'Overall Completion Date Forecast']
                df.at[i, 'End Date Type'] = DateTypeForecast            
            elif not pd.isnull(df.at[i, 'Overall Completion Date Original Planned']):
                df.at[i, 'End Date'] = df.at[i, 'Overall Completion Date Original Planned']
                df.at[i, 'End Date Type'] = DateTypeOriginalPlanned            
            else:
                df.at[i, 'End Date'] = df.at[i, 'Overall Completion Date Placeholder']
                df.at[i, 'End Date Type'] = DateTypePlaceholder            

            df.at[i, 'Department Number'] = 4

            if not pd.isnull(df.at[i, 'Dpt 4 Committed Hrs']):
                df.at[i, 'Commited Hours'] = df.at[i, 'Dpt 4 Committed Hrs']
            else:
                df.at[i, 'Commited Hours'] = df.at[i, 'Overall Committed Hrs']            

        else:     

            df.at[i, 'Department Number'] = 0   

    return df1[['Name', 'Project Number', 'Project Manager', 'Program Manager', 'Location', 'CS Contact', 'Work Package Status',
        'Commited Hours', 'Start Date', 'End Date', 'Department Number', 'Start Date Type', 'End Date Type']]

def GenerateGanttChart(ganttChartData):
    source = ColumnDataSource(ganttChartData)

    plot = figure(y_range=ganttChartData.Name,
               x_axis_type='datetime',
               x_range=(InputFromDate, InputToDate), 
               plot_width=900, plot_height=800, toolbar_location=None,
               title="Project Gantt Chart")
    plot.hbar(y="Name", right="End Date", left="Start Date", height=0.5, source=source, color="firebrick")

    script, div = components(plot)
    return script, div

def make_plot():
    plot = figure(plot_height=300, sizing_mode='scale_width')

    x = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    y = [2**v for v in x]

    plot.line(x, y, line_width=4)

    script, div = components(plot)
    return script, div

projectData = pd.read_excel('construction.xlsx', 'Construction')

InputWorkPackageStatus = 'Construction'
InputDepartment = 'SI Civil'
InputFromDate = datetime.date(2019, 3, 1)
InputToDate = datetime.date(2021, 2, 28)

DateTypeActual = "Actual"
DateTypeForecast = "Forecast"
DateTypeOriginalPlanned = "OriginalPlanned"
DateTypePlaceholder = "PlaceHolder"

ganttChartData = GenerateGanttChartData(projectData, InputWorkPackageStatus, InputDepartment, InputFromDate, InputToDate)
ganttChartDataJson = ganttChartData.to_json(orient='records')

@app.route('/', methods=['GET'])
def api():
    return "<h1>!!Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"

@app.route('/api/GetGanttChartData', methods=['GET'])
def api_all():
    return jsonify(ganttChartDataJson)		

@app.route('/api/dashboard')
def show_dashboard():
    plots = []
    plots.append(GenerateGanttChart(ganttChartData))

    return render_template('dashboard.html', plots=plots)
    