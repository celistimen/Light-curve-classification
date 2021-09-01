#### Deployment:
Go to the folder Stellar-explorer/ with Anaconda (It does not work without Anaconda)  
 execute: python app.py  
    -> go to http://localhost:8050/ in your browser  
Additional configuration will be required to deploy this app on a public server. For more information, see https://dash.plotly.com/deployment

#### Dependencies:
The app requires following packages to be installed:  (and others)
- pip install dash==1.12.0 # although newer versions might work, only dash 1.12 was tested
- pip install dash-bootstrap-components
- pip install dash-extensions
- pip install scipy  

The data (in csv format) needs to be placed in the Stellar-explorer/data/ folder.
