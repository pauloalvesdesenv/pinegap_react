import React from 'react';
import { Link } from 'react-router-dom';

const CustomerId = (cell) => {
    return (
        <Link to="#" className="text-reset fw-bold">{cell.value ? cell.value : ''}</Link>
    );
};

const CustomerName = (cell) => {
    return cell.value ? cell.value : '';
};

const Date = (cell) => {
    return cell.value ? cell.value : '';
};

const Email = (cell) => {
    return cell.value ? cell.value : '';
};

const CustomerStatus = (cell) => {
    return (
        <span
          className={"badge bg-pill font-size-12 bg-" + 
          (cell.value === "Active" ? "success" : "danger" && cell.value === "Deactive" ? "danger" : "") + "-subtle text-" + 
          (cell.value === "Active" ? "success" : "danger" && cell.value === "Deactive" ? "danger" : "")
        }
        >
          {cell.value}
        </span>
    )
};

export {
    CustomerId,
    CustomerName,
    Date,
    Email,
    CustomerStatus,
};