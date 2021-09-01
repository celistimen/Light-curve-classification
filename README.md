# Light-curve-classification
For my second dissertation, I worked with Kepler/TESS data to classify stars based on their variability type. 

## Feature extraction
This folder contains a file with minimal code to extract the 24 most effective features for light curve classification, based on tsfresh, TSFEL, and Cesium, using forward feature selection. Additionally, an example is included to show the usage.

## Stellar explorer
Using the Dash framework, I developed a web application to visualize light curves and their features. The code can be found in this folder.
The app uses the data in a different format (csv). The data can be downloaded [here](https://drive.google.com/file/d/1GBpZpAPH_u5mWztzTYrxCTVElWcLn1Ah/view?usp=sharing), and needs to be placed in the Stellar-explorer/data/ folder. However, because the data is proprietary permission is required first. Contact me at celistimen@gmail.com if you want to use the data or if you have any questions.

Note that the web app has not been tested in a production environment.
