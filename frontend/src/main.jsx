import React, {useEffect, useState} from "react";
import {createRoot} from "react-dom/client";
import "./style.css";

const API = import.meta.env.VITE_API_URL || "http://localhost:8000";

function App(){
  const [token,setToken]=useState(localStorage.getItem("token")||"");
  const [login,setLogin]=useState({username:"",password:""});
  const [employee,setEmployee]=useState({name:"",email:"",department:"",designation:""});
  const [employees,setEmployees]=useState([]);
  const [message,setMessage]=useState("");

  async function doLogin(e){
    e.preventDefault();
    const r=await fetch(API+"/auth/login",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(login)});
    const d=await r.json();
    if(r.ok){localStorage.setItem("token",d.access_token);setToken(d.access_token);setMessage("Login successful");}
    else setMessage(d.detail||"Login failed");
  }
  async function load(){
    const r=await fetch(API+"/employees",{headers:{Authorization:`Bearer ${token}`}});
    if(r.ok)setEmployees(await r.json());
  }
  async function add(e){
    e.preventDefault();
    const r=await fetch(API+"/employees",{method:"POST",headers:{"Content-Type":"application/json",Authorization:`Bearer ${token}`},body:JSON.stringify(employee)});
    if(r.ok){setEmployee({name:"",email:"",department:"",designation:""});setMessage("Employee added");load();}
    else setMessage("Could not add employee");
  }
  async function remove(id){
    await fetch(API+`/employees/${id}`,{method:"DELETE",headers:{Authorization:`Bearer ${token}`}});
    load();
  }
  useEffect(()=>{if(token)load()},[token]);

  if(!token) return <main><div className="card"><h1>Employee Management</h1><p>JWT Authentication</p>
    <form onSubmit={doLogin}><input placeholder="Username" value={login.username} onChange={e=>setLogin({...login,username:e.target.value})}/><input type="password" placeholder="Password" value={login.password} onChange={e=>setLogin({...login,password:e.target.value})}/><button>Login</button></form><p>{message}</p><p className="hint">Register through POST /auth/register first.</p></div></main>;

  return <main><div className="top"><h1>Employee Management</h1><button onClick={()=>{localStorage.removeItem("token");setToken("")}}>Logout</button></div>
    <div className="card"><h2>Add Employee</h2><form onSubmit={add} className="grid">{Object.keys(employee).map(k=><input key={k} placeholder={k} value={employee[k]} onChange={e=>setEmployee({...employee,[k]:e.target.value})}/>)}<button>Add Employee</button></form><p>{message}</p></div>
    <div className="card"><h2>Employees</h2>{employees.map(x=><div className="row" key={x.id}><span><b>{x.name}</b><br/>{x.email} · {x.department} · {x.designation}</span><button onClick={()=>remove(x.id)}>Delete</button></div>)}</div>
  </main>
}
createRoot(document.getElementById("root")).render(<App/>);
