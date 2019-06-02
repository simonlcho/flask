import flask
from flask import request, jsonify

import numpy as np
import pandas as pd
import datetime

app = flask.Flask(__name__)
#app.config["DEBUG"] = True

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

books = [
    {'id': 0,
     'title': 'A Fire Upon the Deep',
     'author': 'Vernor Vinge',
     'first_sentence': 'The coldsleep itself was dreamless.',
     'year_published': '1992'},
    {'id': 1,
     'title': 'The Ones Who Walk Away From Omelas',
     'author': 'Ursula K. Le Guin',
     'first_sentence': 'With a clamor of bells that set the swallows soaring, the Festival of Summer came to the city Omelas, bright-towered by the sea.',
     'published': '1973'},
    {'id': 2,
     'title': 'Dhalgren',
     'author': 'Samuel R. Delany',
     'first_sentence': 'to wound the autumnal city.',
     'published': '1975'}
]

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
books = ganttChartData.to_json(orient='records')

@app.route('/', methods=['GET'])
def api():
    return "<h1>!!Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"

@app.route('/api/GetGanttChartData', methods=['GET'])
def api_all():
    return jsonify(books)		
	
@app.route('/api/v1/resources/books', methods=['GET'])
def api_id():
    # Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    # If no ID is provided, display an error in the browser.
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        return "Error: No id field provided. Please specify an id."

    # Create an empty list for our results
    results = []

    # Loop through the data and match results that fit the requested ID.
    # IDs are unique, but other fields might return many results
    for book in books:
        if book['id'] == id:
            results.append(book)

    # Use the jsonify function from Flask to convert our list of
    # Python dictionaries to the JSON format.
    return jsonify(results)	
	
#app.run()