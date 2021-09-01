Deployment:

    Start the program:
         in folder Stellar-explorer/
         execute: python app.py
            -> go to http://localhost:8050/
    Additional configuration will be required to deploy this app on a public server. For more information, see https://dash.plotly.com/deployment
    
    Dependencies:
        All python packages are listed in setup.bat   
        - Stellar-explorer/data/ needs to contain the data
        ModuleNotFoundError: No module named dash
        => pip install dash 
        ModuleNotFoundError: No module named 'dash_bootstrap_components'
        => pip install dash_bootstrap_components
        
    
For future reference:
Mistakes during development:
    -if there is only one output of a callback, dont put [Output("obj","prop")] but only Output("obj","prop")
            -> omit the brackets otherwise error not the right shape or something
    -the dbc.Col columns need to be in a row, otherwise they will stack on top of eachother
    -children needs to be a list, so if only one child is returned, put it between brackets []
