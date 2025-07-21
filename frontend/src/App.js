import MainApp from './MainApp';
import './App.css';
import React from 'react';
import Login from './Login';
import {BrowserRouter as Router, Routes, Route, Navigate} from "react-router-dom";







function App() {

  
  const isLoggedIn = !!sessionStorage.getItem("access");
  

  
  if (isLoggedIn == null){
    return <div>Loading...</div>
  }
  
  
    

 
  
  return (
    <Router>
      <Routes>
        <Route path ="/" element = {<Navigate to = {isLoggedIn ? "/app" : "/login"}/>}/>
        <Route path="/login" element={<Login />} />
        <Route
        path="/app"
        element={isLoggedIn ? <MainApp/> : (<Navigate to ="/login" />)}
       />
       <Route path = "*" element = {<Navigate to ="/"/>}/>
      </Routes>
    </Router>
  );
}    
        
        
        

        
      

export default App;
