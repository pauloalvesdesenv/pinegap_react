import React from 'react';
import { Link } from 'react-router-dom';

const OrderId = (cell) => {
    return (
        <Link to="#" className="text-body fw-bold">{cell.value ? cell.value : ''}</Link>
    );
};

const BillingName = (cell) => {
    return cell.value ? cell.value : '';
};

const Date = (cell) => {
    return cell.value ? cell.value : '';
};

const Total = (cell) => {
    return cell.value ? cell.value : '';
};

const PaymentStatus = (cell) => {
    return (
        // badge bg-pill bg-success-subtle text-success font-size-12
        <div
          className={"badge bg-pill font-size-12 bg-" + 
          (cell.value === "Paid" ? "success" : "danger" && cell.value === "unpaid" ? "warning" : "danger") + "-subtle text-" + 
          (cell.value === "Paid" ? "success" : "danger" && cell.value === "unpaid" ? "warning" : "danger")
        }
        >
          {cell.value}
        </div>
    )
};

export {
    OrderId,
    BillingName,
    Date,
    Total,
    PaymentStatus,
};