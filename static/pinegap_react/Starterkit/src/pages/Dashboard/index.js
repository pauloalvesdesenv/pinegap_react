import React from "react";
import { Container } from "reactstrap";



//Import Breadcrumb
import Breadcrumbs from "../../components/Common/Breadcrumb";





const Dashboard = () => {

  document.title=" Dashboard | Minible - Responsive Bootstrap 5 Admin Dashboard"


  

  return (
    <React.Fragment>
      <div className="page-content">
        <Container fluid>
          <Breadcrumbs title="Minible" breadcrumbItem="Dashboard" />
          
        </Container>
      </div>
    </React.Fragment>
  );
};

export default Dashboard;