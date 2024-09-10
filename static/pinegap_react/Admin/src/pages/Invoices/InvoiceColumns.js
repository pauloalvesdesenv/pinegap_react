import React from "react";
import {
  Badge,
  Button
} from "reactstrap";
import { Link } from "react-router-dom";

const InvoiceColumns = () => [
  {
    dataField: "invoiceID",
    text: "Invoice ID",
    sort: true,
  },
  {
    dataField: "date",
    text: "Date",
    sort: true,
  },
  {
    dataField: "billingName",
    text: "Billing Name",
    sort: true,
  },
  {
    dataField: "Amount",
    text: "Amount",
    sort: true,
  },
  {
    dataField: "status",
    text: "Status",
    sort: true,
    formatter: (cellContent, row) => (
      <div className={"badge bg-" + row.color + "-subtle text-success font-size-12"}>{row.status}</div>
    ),
  },
  {
    dataField: "DownloadPdf",
    text: "Download Pdf",
    sort: true,
    formatter: () => (
      <>
        <div>
          <Button color="light" className="btn-sm w-xs">Pdf <i className="uil uil-download-alt ms-2"></i></Button>
        </div>
      </>
    ),
  },
  {
    dataField: "menu",
    isDummyField: true,
    text: "Action",
    formatter: () => (
      <>
        <Link to="#" className="px-3 text-primary"><i className="uil uil-pen font-size-18"></i></Link>
        <Link to="#" className="px-3 text-danger"><i className="uil uil-trash-alt font-size-18"></i></Link>
      </>
    ),
  },
];

export default InvoiceColumns;
