# -*- coding: utf-8 -*-
#layout and callbacks of components:
from layout.layout import getLayout

import globals

# Initialize the global variables
if __name__ == '__main__':
    globals.initialize()

# Get layout
globals.app.layout = getLayout(globals.app)
 
# Register callbacks
globals.dcb.register(globals.app)

# start app
if __name__ == '__main__':
    # The app can use multithreading with the processes parameter
    # use debug = False for a production environment
    globals.app.run_server(debug=True, processes = 1)
    
