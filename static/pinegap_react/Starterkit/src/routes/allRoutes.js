import React from "react"
import { Navigate } from "react-router-dom"

// Dashboard
import Dashboard from "../pages/Dashboard/index"


//Pages
import PagesStarter from "../pages/Utility/pages-starter"
import PagesMaintenance from "../pages/Utility/pages-maintenance"
import PagesComingsoon from "../pages/Utility/pages-comingsoon"
import Pages404 from "../pages/Utility/pages-404"
import Pages500 from "../pages/Utility/pages-500"


// Authentication related pages
import Login from "../pages/Authentication/Login"
import Logout from "../pages/Authentication/Logout"
import Register from "../pages/Authentication/Register"
import ForgetPwd from "../pages/Authentication/ForgetPassword"

//  // Inner Authentication
import Login1 from "../pages/AuthenticationInner/Login"
import Register1 from "../pages/AuthenticationInner/Register"
import Recoverpw from "../pages/AuthenticationInner/Recoverpw"
import LockScreen from "../pages/AuthenticationInner/auth-lock-screen"


const userRoutes = [
  { path: "/dashboard", component: <Dashboard /> },
  

  //Utility
  { path: "/pages-starter", component: <PagesStarter/> },

  
  // this route should be at the end of all other routes
  // eslint-disable-next-line react/display-name
  {
    path: "/",
    exact: true,
    component: <Navigate to="/dashboard" />,
  },
  { path: "*", component: <Navigate to="/dashboard" /> },
];

const authRoutes = [

  { path: "/logout", component: <Logout/> },
  { path: "/login", component: <Login/> },
  { path: "/forgot-password", component: <ForgetPwd/> },
  { path: "/register", component: <Register/> },

  { path: "/pages-maintenance", component: <PagesMaintenance/> },
  { path: "/pages-comingsoon", component: <PagesComingsoon/> },
  { path: "/pages-404", component: <Pages404/> },
  { path: "/pages-500", component: <Pages500/> },

  // Authentication Inner
  { path: "/pages-login", component: <Login1/> },
  { path: "/pages-register", component: <Register1/> },
  { path: "/page-recoverpw", component: <Recoverpw/> },
  { path: "/auth-lock-screen", component: <LockScreen/> },
]

export { userRoutes, authRoutes }