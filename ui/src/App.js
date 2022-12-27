import './App.css';
import * as React from 'react';
import Button from '@mui/material/Button';

function App() {

    return (
        <div className="App">
            <Button variant="contained" color="primary" onClick={() => fetch("/on",{method:'PUT'})}>
              On
            </Button>

            <Button variant="outlined" color="primary" onClick={() => fetch("/off",{method:'PUT'})}>
              Off
            </Button>
        </div>
    );
}

export default App;
