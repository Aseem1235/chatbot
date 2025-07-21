import { useState } from "react";
import './Login.css'


function Login() {

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  
  
    

  const handleSubmit = async (e) => {
    e.preventDefault();
    try{
        const res = await fetch("http://127.0.0.1:8000/api/custom-login/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
        });

        const data = await res.json();
        if (res.ok) {
            if(data.status==="admin"){
                window.location.href = "http://localhost:8000/admin/";
            }else if(data.status==="user"){
                localStorage.setItem("username",username);
                sessionStorage.setItem("access", data.token);
                alert("Login successful!");
                window.location.href="/app"
            }else{
                alert(data.error||"Login failed");
            }
        
        }else {
        alert("Login failed: " + JSON.stringify(data));
        }
    } catch(error){
        console.error("Login error:",error);
        alert("Login request failed.");
        }
    };

  return (
    <div className = "container">
        <div className="left">
            <h1 className="welcome">Welcome-Login</h1>
            
            <img className = "img"
            src="https://i.imgur.com/bX4rcIG.jpeg"
            alt="Login background"
            />
        </div>
        <div className="right">
            <form className="login-form" onSubmit={handleSubmit}>
                <input
                className="user-input"
                type="text"
                placeholder="Username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                />
                <input
                className="pass-input"
                type="password"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                />
                <button className = "submit-button" type="submit">Log In</button>
            </form>
        </div>
    </div>
  );
}


export default Login;
