import React from "react";
import { Navigate } from "react-router-dom";

const Authmiddleware = (props) => {
  if (!localStorage.getItem("authUser")) {
    return (
      <Navigate to={{ pathname: "/login" }} />
    );
  }
  return (
    <React.Fragment>
    {props.children}
  </React.Fragment>);
};

export default Authmiddleware;
