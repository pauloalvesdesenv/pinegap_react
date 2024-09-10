import React, { useState } from "react";
import { Card, CardBody, Col, Container, DropdownItem, DropdownMenu, DropdownToggle, Form, Progress, Row, UncontrolledCollapse, UncontrolledDropdown } from "reactstrap";

//Import Breadcrumb
import Breadcrumbs from "../../components/Common/Breadcrumb";
import { Link } from "react-router-dom";
import SimpleBar from "simplebar-react";
import ActivityCharts from "./charts";
import Dropzone from "react-dropzone";

// Images
import upgradeImg from "../../assets/images/upgrade-img.png";
import avatar1 from "../../assets/images/users/avatar-1.jpg";
import avatar2 from "../../assets/images/users/avatar-2.jpg";
import avatar3 from "../../assets/images/users/avatar-3.jpg";
import avatar4 from "../../assets/images/users/avatar-4.jpg";
import avatar5 from "../../assets/images/users/avatar-5.jpg";
import avatar6 from "../../assets/images/users/avatar-6.jpg";
import avatar7 from "../../assets/images/users/avatar-7.jpg";
import avatar8 from "../../assets/images/users/avatar-8.jpg";

const FileManager = () => {

    document.title=" File Manager | Minible - Responsive Bootstrap 5 Admin Dashboard"

    const [selectedFiles, setselectedFiles] = useState([]);

    function handleAcceptedFiles(files) {
        files.map(file =>
            Object.assign(file, {
                preview: URL.createObjectURL(file),
                formattedSize: formatBytes(file.size),
            })
        );
        setselectedFiles(files);
    }

    /**
     * Formats the size
     */
    function formatBytes(bytes, decimals = 2) {
        if (bytes === 0) return "0 Bytes";
        const k = 1024;
        const dm = decimals < 0 ? 0 : decimals;
        const sizes = ["Bytes", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"];

        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + " " + sizes[i];
    }

    return (
        <React.Fragment>
            <div className="page-content">
                <Container fluid>
                    <Breadcrumbs title="Apps" breadcrumbItem="File Manager" />
                    <div className="d-xl-flex">
                        <div className="w-100">
                            <div className="d-xl-flex">
                                <Card className="filemanager-sidebar me-md-3">
                                    <CardBody>
                                        <div className="d-flex flex-column h-100">
                                            <div className="mb-4">
                                                <div className="mb-3">
                                                    <UncontrolledDropdown>
                                                        <DropdownToggle className="btn btn-primary w-100" tag="button">
                                                            <i className="mdi mdi-plus me-1">Create New</i>
                                                        </DropdownToggle>
                                                        <DropdownMenu>
                                                            <DropdownItem href="#"><i className="bx bx-folder me-1"></i> Folder</DropdownItem>
                                                            <DropdownItem href="#"><i className="bx bx-file me-1"></i> File</DropdownItem>
                                                        </DropdownMenu>
                                                    </UncontrolledDropdown>
                                                </div>
                                                <ul className="list-unstyled categories-list">
                                                    <li>
                                                        <div className="custom-accordion">
                                                            <Link className="text-body fw-medium py-1 d-flex align-items-center" data-bs-toggle="collapse" to="#categories-collapse" role="button" aria-expanded="false" aria-controls="categories-collapse" id="categories-collapse">
                                                                <i className="mdi mdi-folder font-size-20 text-warning me-2"></i> My Files <i className="mdi mdi-chevron-up accor-down-icon ms-auto"></i>
                                                            </Link>
                                                            <UncontrolledCollapse toggler="#categories-collapse" defaultOpen={true}>
                                                                <Card className="border-0 shadow-none ps-2 mb-0">
                                                                    <ul className="list-unstyled mb-0">
                                                                        <li><Link to="#" className="d-flex align-items-center"><span className="me-auto">Analytics</span></Link></li>
                                                                        <li><Link to="#" className="d-flex align-items-center"><span className="me-auto">Design</span></Link></li>
                                                                        <li><Link to="#" className="d-flex align-items-center"><span className="me-auto">Development</span> <i className="mdi mdi-pin ms-auto"></i></Link></li>
                                                                        <li><Link to="#" className="d-flex align-items-center"><span className="me-auto">Project A</span></Link></li>
                                                                        <li><Link to="#" className="d-flex align-items-center"><span className="me-auto">Admin</span> <i className="mdi mdi-pin ms-auto"></i></Link></li>
                                                                    </ul>
                                                                </Card>
                                                            </UncontrolledCollapse>
                                                        </div>
                                                    </li>
                                                    <li>
                                                        <Link to="#" className="text-body d-flex align-items-center">
                                                            <i className="mdi mdi-google-drive font-size-20 text-muted me-2"></i> <span className="me-auto">Google Drive</span>
                                                        </Link>
                                                    </li>
                                                    <li>
                                                        <Link to="#" className="text-body d-flex align-items-center">
                                                            <i className="mdi mdi-dropbox font-size-20 me-2 text-primary"></i> <span className="me-auto">Dropbox</span>
                                                        </Link>
                                                    </li>
                                                    <li>
                                                        <Link to="#" className="text-body d-flex align-items-center">
                                                            <i className="mdi mdi-share-variant font-size-20 me-2"></i> <span className="me-auto">Shared</span> <i className="mdi mdi-circle-medium text-danger ms-2"></i>
                                                        </Link>
                                                    </li>
                                                    <li>
                                                        <Link to="#" className="text-body d-flex align-items-center">
                                                            <i className="mdi mdi-star-outline text-muted font-size-20 me-2"></i> <span className="me-auto">Starred</span>
                                                        </Link>
                                                    </li>
                                                    <li>
                                                        <Link to="#" className="text-body d-flex align-items-center">
                                                            <i className="mdi mdi-trash-can text-danger font-size-20 me-2"></i> <span className="me-auto">Trash</span>
                                                        </Link>
                                                    </li>
                                                    <li>
                                                        <Link to="#" className="text-body d-flex align-items-center">
                                                            <i className="mdi mdi-cog text-muted font-size-20 me-2"></i> <span className="me-auto">Setting</span><span className="badge bg-success rounded-pill ms-2">01</span>
                                                        </Link>
                                                    </li>
                                                </ul>
                                            </div>

                                            <div className="mt-4 pt-3 mt-auto text-center">
                                                <Card className="mb-0">
                                                    <CardBody>
                                                        <div className="px-4">
                                                            <img src={upgradeImg} className="img-fluid" alt="" />
                                                        </div>
                                                        <h5 className="mt-4">Upgrade Features</h5>
                                                        <p className="pt-1">4 integrations, 30 team members, advanced features </p>
                                                        <div className="text-center pt-2">
                                                            <button type="button" className="btn btn-primary w-100">Upgrade <i className="mdi mdi-arrow-right ms-1"></i></button>
                                                        </div>
                                                    </CardBody>
                                                </Card>
                                            </div>

                                        </div>
                                    </CardBody>
                                </Card>

                                <div className="w-100">
                                    <Card>
                                        <CardBody>
                                            <h5 className="font-size-16 me-3 mb-0">My Files</h5>

                                            <Row className="mt-4">
                                                <Col xl={4} sm={6}>
                                                    <Card>
                                                        <CardBody className="p-3">
                                                            <div className="">
                                                                <UncontrolledDropdown className="float-end">
                                                                    <DropdownToggle tag="a" className="text-muted font-size-16">
                                                                        <i className="bx bx-dots-vertical-rounded font-size-20"></i>
                                                                    </DropdownToggle>
                                                                    <DropdownMenu className="dropdown-menu-end">
                                                                        <DropdownItem href="#">Edit</DropdownItem>
                                                                        <DropdownItem href="#">Action</DropdownItem>
                                                                        <DropdownItem href="#">Remove</DropdownItem>
                                                                    </DropdownMenu>
                                                                </UncontrolledDropdown>
                                                                <div className="d-flex align-items-center overflow-hidden">

                                                                    <div className="flex-shrink-0 me-3">
                                                                        <div className="avatar align-self-center">
                                                                            <div className="avatar-title rounded bg-primary-subtle text-primary font-size-24">
                                                                                <i className="mdi mdi-google-drive"></i>
                                                                            </div>
                                                                        </div>
                                                                    </div>

                                                                    <div className="flex-grow-1">
                                                                        <h5 className="font-size-15 mb-1 text-truncate">Google Drive</h5>
                                                                        <Link to="#" className="font-size-14 text-muted text-truncate"><u>View Folder</u></Link>
                                                                    </div>
                                                                </div>
                                                                <div className="mt-3 pt-1">
                                                                    <div className="d-flex justify-content-between">
                                                                        <p className="text-muted font-size-13 mb-1">15GB</p>
                                                                        <p className="text-muted font-size-13 mb-1 text-truncate">25GB used</p>
                                                                    </div>

                                                                    <Progress className="animated-progess custom-progress" multi >
                                                                        <Progress animated className="bg-gradient" bar value="90" />
                                                                    </Progress>
                                                                </div>
                                                            </div>
                                                        </CardBody>
                                                    </Card>
                                                </Col>

                                                <Col xl={4} sm={6}>
                                                    <Card>
                                                        <CardBody className="p-3">

                                                            <div className="">
                                                                <UncontrolledDropdown className="float-end">
                                                                    <DropdownToggle tag="a" className="text-muted font-size-16">
                                                                        <i className="bx bx-dots-vertical-rounded font-size-20"></i>
                                                                    </DropdownToggle>
                                                                    <DropdownMenu className="dropdown-menu-end">
                                                                        <DropdownItem href="#">Edit</DropdownItem>
                                                                        <DropdownItem href="#">Action</DropdownItem>
                                                                        <DropdownItem href="#">Remove</DropdownItem>
                                                                    </DropdownMenu>
                                                                </UncontrolledDropdown>
                                                                <div className="d-flex align-items-center overflow-hidden">

                                                                    <div className="flex-shrink-0 me-3">
                                                                        <div className="avatar align-self-center">
                                                                            <div className="avatar-title rounded bg-info-subtle text-info font-size-24">
                                                                                <i className="mdi mdi-dropbox"></i>
                                                                            </div>
                                                                        </div>
                                                                    </div>

                                                                    <div className="flex-grow-1">
                                                                        <h5 className="font-size-15 mb-1 text-truncate">Dropbox</h5>
                                                                        <Link to="#" className="font-size-14 text-muted text-truncate"><u>View Folder</u></Link>
                                                                    </div>
                                                                </div>
                                                                <div className="mt-3 pt-1">
                                                                    <div className="d-flex justify-content-between">
                                                                        <p className="text-muted font-size-13 mb-1">20GB</p>
                                                                        <p className="text-muted font-size-13 mb-1 text-truncate">50GB used</p>
                                                                    </div>
                                                                    <Progress className="animated-progess custom-progress" multi >
                                                                        <Progress animated className="bg-gradient" bar value="90" />
                                                                    </Progress>
                                                                </div>
                                                            </div>
                                                        </CardBody>
                                                    </Card>
                                                </Col>

                                                <Col xl={4} sm={6}>
                                                    <Card>
                                                        <CardBody className="p-3">
                                                            <div className="">
                                                                <UncontrolledDropdown className="float-end">
                                                                    <DropdownToggle tag="a" className="text-muted font-size-16">
                                                                        <i className="bx bx-dots-vertical-rounded font-size-20"></i>
                                                                    </DropdownToggle>
                                                                    <DropdownMenu className="dropdown-menu-end">
                                                                        <DropdownItem href="#">Edit</DropdownItem>
                                                                        <DropdownItem href="#">Action</DropdownItem>
                                                                        <DropdownItem href="#">Remove</DropdownItem>
                                                                    </DropdownMenu>
                                                                </UncontrolledDropdown>
                                                                <div className="d-flex align-items-center overflow-hidden">

                                                                    <div className="flex-shrink-0 me-3">
                                                                        <div className="avatar align-self-center me-3">
                                                                            <div className="avatar-title rounded bg-primary-subtle text-primary font-size-24">
                                                                                <i className="mdi mdi-apple-icloud"></i>
                                                                            </div>
                                                                        </div>
                                                                    </div>

                                                                    <div className="flex-grow-1">
                                                                        <h5 className="font-size-15 mb-1 text-truncate">One Drive</h5>
                                                                        <Link to="#" className="font-size-14 text-muted text-truncate"><u>View Folder</u></Link>
                                                                    </div>

                                                                </div>
                                                                <div className="mt-3 pt-1">
                                                                    <div className="d-flex justify-content-between">
                                                                        <p className="text-muted font-size-13 mb-1">10GB</p>
                                                                        <p className="text-muted font-size-13 mb-1 text-truncate">20GB used</p>
                                                                    </div>
                                                                    <Progress className="animated-progess custom-progress" multi >
                                                                        <Progress animated className="bg-gradient" bar value="90" />
                                                                    </Progress>
                                                                </div>
                                                            </div>
                                                        </CardBody>
                                                    </Card>
                                                </Col>

                                            </Row>

                                            <h5 className="font-size-16 me-3 mb-0">Folders</h5>

                                            <Row className="mt-4">
                                                <Col xl={4} sm={6}>
                                                    <Card>
                                                        <CardBody className="p-3">
                                                            <div className="">
                                                                <div className="d-flex justify-content-between align-items-center">
                                                                    <div>
                                                                        <i className="bx bxs-folder h2 mb-0 text-warning"></i>
                                                                    </div>
                                                                    <div className="avatar-group">
                                                                        <div className="avatar-group-item">
                                                                            <Link to="#" className="d-inline-block">
                                                                                <img src={avatar4} alt="" className="rounded-circle avatar-xs" />
                                                                            </Link>
                                                                        </div>
                                                                        <div className="avatar-group-item">
                                                                            <Link to="#" className="d-inline-block">
                                                                                <div className="avatar-xs">
                                                                                    <span className="avatar-title rounded-circle bg-success text-white font-size-15">
                                                                                        A
                                                                                    </span>
                                                                                </div>
                                                                            </Link>
                                                                        </div>
                                                                    </div>
                                                                </div>
                                                                <div className="d-flex mt-3">
                                                                    <div className="overflow-hidden me-auto">
                                                                        <h5 className="font-size-15 text-truncate mb-1"><Link to="#" className="text-body">Analytics</Link></h5>
                                                                        <p className="text-muted text-truncate mb-0">12 Files</p>
                                                                    </div>
                                                                    <div className="align-self-end ms-2">
                                                                        <p className="text-muted mb-0 font-size-13"><i className="bx bx-time-five align-middle me-1"></i> 15 min ago</p>
                                                                    </div>
                                                                </div>
                                                            </div>
                                                        </CardBody>
                                                    </Card>
                                                </Col>

                                                <Col xl={4} sm={6}>
                                                    <Card>
                                                        <CardBody className="p-3">
                                                            <div className="">
                                                                <div className="d-flex justify-content-between align-items-center">
                                                                    <div>
                                                                        <i className="bx bxs-folder h2 mb-0 text-warning"></i>
                                                                    </div>
                                                                    <div className="avatar-group">
                                                                        <div className="avatar-group-item">
                                                                            <Link to="#" className="d-inline-block">
                                                                                <img src={avatar3} alt="" className="rounded-circle avatar-xs" />
                                                                            </Link>
                                                                        </div>
                                                                        <div className="avatar-group-item">
                                                                            <Link to="#" className="d-inline-block">
                                                                                <img src={avatar6} alt="" className="rounded-circle avatar-xs" />
                                                                            </Link>
                                                                        </div>
                                                                    </div>
                                                                </div>
                                                                <div className="d-flex mt-3">
                                                                    <div className="overflow-hidden me-auto">
                                                                        <h5 className="font-size-15 text-truncate mb-1"><Link to="#" className="text-body">Sketch Design</Link></h5>
                                                                        <p className="text-muted text-truncate mb-0">235 Files</p>
                                                                    </div>
                                                                    <div className="align-self-end ms-2">
                                                                        <p className="text-muted mb-0 font-size-13"><i className="bx bx-time-five align-middle me-1"></i> 23 min ago</p>
                                                                    </div>
                                                                </div>
                                                            </div>
                                                        </CardBody>
                                                    </Card>
                                                </Col>

                                                <Col xl={4} sm={6}>
                                                    <Card>
                                                        <CardBody className="p-3">
                                                            <div className="">
                                                                <div className="d-flex justify-content-between align-items-center">
                                                                    <div>
                                                                        <i className="bx bxs-folder h2 mb-0 text-warning"></i>
                                                                    </div>
                                                                    <div className="avatar-group">
                                                                        <div className="avatar-group-item">
                                                                            <Link to="#" className="d-inline-block">
                                                                                <div className="avatar-xs">
                                                                                    <span className="avatar-title rounded-circle bg-info text-white font-size-15">
                                                                                        K
                                                                                    </span>
                                                                                </div>
                                                                            </Link>
                                                                        </div>
                                                                        <div className="avatar-group-item">
                                                                            <Link to="#" className="d-inline-block">
                                                                                <img src={avatar2} alt="" className="rounded-circle avatar-xs" />
                                                                            </Link>
                                                                        </div>
                                                                    </div>
                                                                </div>
                                                                <div className="d-flex mt-3">
                                                                    <div className="overflow-hidden me-auto">
                                                                        <h5 className="font-size-15 text-truncate mb-1"><Link to="#" className="text-body">Applications</Link></h5>
                                                                        <p className="text-muted text-truncate mb-0">20 Files</p>
                                                                    </div>
                                                                    <div className="align-self-end ms-2">
                                                                        <p className="text-muted mb-0 font-size-13"><i className="bx bx-time-five align-middle me-1"></i> 45 min ago</p>
                                                                    </div>
                                                                </div>
                                                            </div>
                                                        </CardBody>
                                                    </Card>
                                                </Col>

                                            </Row>

                                            <h5 className="font-size-16 me-3 mb-0">Co-owners</h5>

                                            <Row className="mt-4">
                                                <Col xl={4} sm={6}>
                                                    <Card className="border">
                                                        <CardBody>
                                                            <div className="">
                                                                <div className="d-flex align-items-center">
                                                                    <div className="avatar align-self-center me-3">
                                                                        <img src={avatar3} alt="" className="avatar rounded" />
                                                                    </div>
                                                                    <div className="flex-1">
                                                                        <h5 className="font-size-15 mb-1">Sadie Stanfield</h5>
                                                                        <Link to="#" className="font-size-14 text-muted"><u>Con Edit</u></Link>
                                                                    </div>
                                                                </div>
                                                            </div>
                                                        </CardBody>
                                                    </Card>
                                                </Col>

                                                <Col xl={4} sm={6}>
                                                    <Card className="border">
                                                        <CardBody>
                                                            <div className="">
                                                                <div className="d-flex align-items-center">
                                                                    <div className="avatar align-self-center me-3">
                                                                        <img src={avatar5} alt="" className="avatar rounded" />
                                                                    </div>

                                                                    <div className="flex-1">
                                                                        <h5 className="font-size-15 mb-1">Dustin Westrick</h5>
                                                                        <Link to="#" className="font-size-14 text-muted"><u>Con View</u></Link>
                                                                    </div>
                                                                </div>
                                                            </div>
                                                        </CardBody>
                                                    </Card>
                                                </Col>

                                                <Col xl={4} sm={6}>
                                                    <Card className="border">
                                                        <CardBody>
                                                            <div className="">
                                                                <div className="d-flex align-items-center">
                                                                    <div className="avatar align-self-center me-3">
                                                                        <img src={avatar6} alt="" className="avatar rounded" />
                                                                    </div>

                                                                    <div className="flex-1">
                                                                        <h5 className="font-size-15 mb-1">Patrick Parker</h5>
                                                                        <Link to="#" className="font-size-14 text-muted"><u>Con Edit</u></Link>
                                                                    </div>

                                                                </div>
                                                            </div>
                                                        </CardBody>
                                                    </Card>
                                                </Col>

                                            </Row>

                                            <h5 className="font-size-16 me-3 mb-0">Recent Files</h5>


                                            <SimpleBar className="mx-n4 px-4 mt-4" style={{ maxHeight: "350px" }}>
                                                <div className="table-responsive">

                                                    <table className="table align-middle table-nowrap table-hover mb-0">
                                                        <thead className="bg-light">
                                                            <tr>
                                                                <th scope="col">Name</th>
                                                                <th scope="col">Date modified</th>
                                                                <th scope="col">Size</th>
                                                                <th scope="col" colSpan="2">Members</th>
                                                            </tr>
                                                        </thead>
                                                        <tbody>
                                                            <tr>
                                                                <td><Link to="#" className="text-dark fw-medium"><i className="mdi mdi-file-document font-size-20 align-middle text-primary me-2"></i> index.html</Link></td>
                                                                <td>12-10-2021</td>
                                                                <td>09 KB</td>
                                                                <td>
                                                                    <div className="avatar-group">
                                                                        <div className="avatar-group-item">
                                                                            <Link href="#" className="d-inline-block">
                                                                                <img src={avatar4} alt="" className="rounded-circle avatar-xs" />
                                                                            </Link>
                                                                        </div>
                                                                        <div className="avatar-group-item">
                                                                            <Link href="#" className="d-inline-block">
                                                                                <img src={avatar5} alt="" className="rounded-circle avatar-xs" />
                                                                            </Link>
                                                                        </div>
                                                                        <div className="avatar-group-item">
                                                                            <Link href="#" className="d-inline-block">
                                                                                <div className="avatar-xs">
                                                                                    <span className="avatar-title rounded-circle bg-success text-white font-size-15">
                                                                                        A
                                                                                    </span>
                                                                                </div>
                                                                            </Link>
                                                                        </div>
                                                                    </div>
                                                                </td>
                                                                <td>
                                                                    <UncontrolledDropdown>
                                                                        <DropdownToggle tag="a" className="font-size-16 text-muted">
                                                                            <i className="mdi mdi-dots-horizontal"></i>
                                                                        </DropdownToggle>
                                                                        <DropdownMenu className="dropdown-menu-end">
                                                                            <DropdownItem href="#">Open</DropdownItem>
                                                                            <DropdownItem href="#">Edit</DropdownItem>
                                                                            <DropdownItem href="#">Rename</DropdownItem>
                                                                            <DropdownItem divider />
                                                                            <DropdownItem href="#">Remove</DropdownItem>
                                                                        </DropdownMenu>
                                                                    </UncontrolledDropdown>
                                                                </td>
                                                            </tr>
                                                            <tr>
                                                                <td><Link to="#" className="text-dark fw-medium"><i className="mdi mdi-folder-zip font-size-20 align-middle text-warning me-2"></i> Project-A.zip</Link></td>
                                                                <td>11-10-2021</td>
                                                                <td>115 KB</td>
                                                                <td>
                                                                    <div className="avatar-group">
                                                                        <div className="avatar-group-item">
                                                                            <Link href="#" className="d-inline-block">
                                                                                <img src={avatar8} alt="" className="rounded-circle avatar-xs" />
                                                                            </Link>
                                                                        </div>
                                                                        <div className="avatar-group-item">
                                                                            <Link href="#" className="d-inline-block">
                                                                                <img src={avatar2} alt="" className="rounded-circle avatar-xs" />
                                                                            </Link>
                                                                        </div>
                                                                    </div>
                                                                </td>
                                                                <td>
                                                                    <UncontrolledDropdown>
                                                                        <DropdownToggle tag="a" className="font-size-16 text-muted">
                                                                            <i className="mdi mdi-dots-horizontal"></i>
                                                                        </DropdownToggle>
                                                                        <DropdownMenu className="dropdown-menu-end">
                                                                            <DropdownItem href="#">Open</DropdownItem>
                                                                            <DropdownItem href="#">Edit</DropdownItem>
                                                                            <DropdownItem href="#">Rename</DropdownItem>
                                                                            <DropdownItem divider />
                                                                            <DropdownItem href="#">Remove</DropdownItem>
                                                                        </DropdownMenu>
                                                                    </UncontrolledDropdown>
                                                                </td>
                                                            </tr>
                                                            <tr>
                                                                <td><Link to="#" className="text-dark fw-medium"><i className="mdi mdi-image font-size-20 align-middle text-muted me-2"></i> Img-1.jpeg</Link></td>
                                                                <td>11-10-2021</td>
                                                                <td>86 KB</td>
                                                                <td>
                                                                    <div className="avatar-group">
                                                                        <div className="avatar-group-item">
                                                                            <Link to="#" className="d-inline-block">
                                                                                <div className="avatar-xs">
                                                                                    <span className="avatar-title rounded-circle bg-info text-white font-size-15">
                                                                                        K
                                                                                    </span>
                                                                                </div>
                                                                            </Link>
                                                                        </div>
                                                                        <div className="avatar-group-item">
                                                                            <Link to="#" className="d-inline-block">
                                                                                <img src={avatar2} alt="" className="rounded-circle avatar-xs" />
                                                                            </Link>
                                                                        </div>
                                                                    </div>
                                                                </td>
                                                                <td>
                                                                    <UncontrolledDropdown>
                                                                        <DropdownToggle tag="a" className="font-size-16 text-muted">
                                                                            <i className="mdi mdi-dots-horizontal"></i>
                                                                        </DropdownToggle>
                                                                        <DropdownMenu className="dropdown-menu-end">
                                                                            <DropdownItem href="#">Open</DropdownItem>
                                                                            <DropdownItem href="#">Edit</DropdownItem>
                                                                            <DropdownItem href="#">Rename</DropdownItem>
                                                                            <DropdownItem divider />
                                                                            <DropdownItem href="#">Remove</DropdownItem>
                                                                        </DropdownMenu>
                                                                    </UncontrolledDropdown>
                                                                </td>
                                                            </tr>
                                                            <tr>
                                                                <td><Link to="#" className="text-dark fw-medium"><i className="mdi mdi-text-box font-size-20 align-middle text-muted me-2"></i> update list.txt</Link></td>
                                                                <td>10-10-2021</td>
                                                                <td>08 KB</td>
                                                                <td>
                                                                    <div className="avatar-group">
                                                                        <div className="avatar-group-item">
                                                                            <Link to="#" className="d-inline-block">
                                                                                <img src={avatar1} alt="" className="rounded-circle avatar-xs" />
                                                                            </Link>
                                                                        </div>
                                                                        <div className="avatar-group-item">
                                                                            <Link to="#" className="d-inline-block">
                                                                                <img src={avatar6} alt="" className="rounded-circle avatar-xs" />
                                                                            </Link>
                                                                        </div>
                                                                        <div className="avatar-group-item">
                                                                            <Link to="#" className="d-inline-block">
                                                                                <img src={avatar7} alt="" className="rounded-circle avatar-xs" />
                                                                            </Link>
                                                                        </div>
                                                                    </div>
                                                                </td>
                                                                <td>
                                                                    <UncontrolledDropdown>
                                                                        <DropdownToggle tag="a" className="font-size-16 text-muted">
                                                                            <i className="mdi mdi-dots-horizontal"></i>
                                                                        </DropdownToggle>
                                                                        <DropdownMenu className="dropdown-menu-end">
                                                                            <DropdownItem href="#">Open</DropdownItem>
                                                                            <DropdownItem href="#">Edit</DropdownItem>
                                                                            <DropdownItem href="#">Rename</DropdownItem>
                                                                            <DropdownItem divider />
                                                                            <DropdownItem href="#">Remove</DropdownItem>
                                                                        </DropdownMenu>
                                                                    </UncontrolledDropdown>
                                                                </td>
                                                            </tr>
                                                            <tr>
                                                                <td><Link to="#" className="text-dark fw-medium"><i className="mdi mdi-folder font-size-20 align-middle text-warning me-2"></i> Project B</Link></td>
                                                                <td>10-10-2021</td>
                                                                <td>72 KB</td>
                                                                <td>
                                                                    <div className="avatar-group">
                                                                        <div className="avatar-group-item">
                                                                            <Link to="#" className="d-inline-block">
                                                                                <img src={avatar1} alt="" className="rounded-circle avatar-xs" />
                                                                            </Link>
                                                                        </div>
                                                                        <div className="avatar-group-item">
                                                                            <Link to="#" className="d-inline-block">
                                                                                <img src={avatar3} alt="" className="rounded-circle avatar-xs" />
                                                                            </Link>
                                                                        </div>
                                                                        <div className="avatar-group-item">
                                                                            <Link to="#" className="d-inline-block">
                                                                                <div className="avatar-xs">
                                                                                    <span className="avatar-title rounded-circle bg-danger text-white font-size-15">
                                                                                        3+
                                                                                    </span>
                                                                                </div>
                                                                            </Link>
                                                                        </div>
                                                                    </div>
                                                                </td>
                                                                <td>
                                                                    <UncontrolledDropdown>
                                                                        <DropdownToggle tag="a" className="font-size-16 text-muted">
                                                                            <i className="mdi mdi-dots-horizontal"></i>
                                                                        </DropdownToggle>
                                                                        <DropdownMenu className="dropdown-menu-end">
                                                                            <DropdownItem href="#">Open</DropdownItem>
                                                                            <DropdownItem href="#">Edit</DropdownItem>
                                                                            <DropdownItem href="#">Rename</DropdownItem>
                                                                            <DropdownItem divider />
                                                                            <DropdownItem href="#">Remove</DropdownItem>
                                                                        </DropdownMenu>
                                                                    </UncontrolledDropdown>
                                                                </td>
                                                            </tr>
                                                            <tr>
                                                                <td><Link to="#" className="text-dark fw-medium"><i className="mdi mdi-text-box font-size-20 align-middle text-muted me-2"></i> Changes list.txt</Link></td>
                                                                <td>09-10-2021</td>
                                                                <td>07 KB</td>
                                                                <td>
                                                                    <div className="avatar-group">
                                                                        <div className="avatar-group-item">
                                                                            <Link to="#" className="d-inline-block">
                                                                                <img src={avatar4} alt="" className="rounded-circle avatar-xs" />
                                                                            </Link>
                                                                        </div>
                                                                        <div className="avatar-group-item">
                                                                            <Link to="#" className="d-inline-block">
                                                                                <img src={avatar5} alt="" className="rounded-circle avatar-xs" />
                                                                            </Link>
                                                                        </div>
                                                                    </div>
                                                                </td>
                                                                <td>
                                                                    <UncontrolledDropdown>
                                                                        <DropdownToggle tag="a" className="font-size-16 text-muted">
                                                                            <i className="mdi mdi-dots-horizontal"></i>
                                                                        </DropdownToggle>
                                                                        <DropdownMenu className="dropdown-menu-end">
                                                                            <DropdownItem href="#">Open</DropdownItem>
                                                                            <DropdownItem href="#">Edit</DropdownItem>
                                                                            <DropdownItem href="#">Rename</DropdownItem>
                                                                            <DropdownItem divider />
                                                                            <DropdownItem href="#">Remove</DropdownItem>
                                                                        </DropdownMenu>
                                                                    </UncontrolledDropdown>
                                                                </td>
                                                            </tr>
                                                            <tr>
                                                                <td><Link to="#" className="text-dark fw-medium"><i className="mdi mdi-image font-size-20 align-middle text-success me-2"></i> Img-2.png</Link></td>
                                                                <td>09-10-2021</td>
                                                                <td>31 KB</td>
                                                                <td>
                                                                    <div className="avatar-group">
                                                                        <div className="avatar-group-item">
                                                                            <Link to="#" className="d-inline-block">
                                                                                <div className="avatar-xs">
                                                                                    <span className="avatar-title rounded-circle bg-pink text-white font-size-15">
                                                                                        L
                                                                                    </span>
                                                                                </div>
                                                                            </Link>
                                                                        </div>
                                                                        <div className="avatar-group-item">
                                                                            <Link to="#" className="d-inline-block">
                                                                                <img src={avatar2} alt="" className="rounded-circle avatar-xs" />
                                                                            </Link>
                                                                        </div>
                                                                    </div>
                                                                </td>
                                                                <td>
                                                                    <UncontrolledDropdown>
                                                                        <DropdownToggle tag="a" className="font-size-16 text-muted">
                                                                            <i className="mdi mdi-dots-horizontal"></i>
                                                                        </DropdownToggle>
                                                                        <DropdownMenu className="dropdown-menu-end">
                                                                            <DropdownItem href="#">Open</DropdownItem>
                                                                            <DropdownItem href="#">Edit</DropdownItem>
                                                                            <DropdownItem href="#">Rename</DropdownItem>
                                                                            <DropdownItem divider />
                                                                            <DropdownItem href="#">Remove</DropdownItem>
                                                                        </DropdownMenu>
                                                                    </UncontrolledDropdown>
                                                                </td>
                                                            </tr>
                                                            <tr>
                                                                <td><Link to="#" className="text-dark fw-medium"><i className="mdi mdi-folder font-size-20 align-middle text-warning me-2"></i> Project C</Link></td>
                                                                <td>09-10-2021</td>
                                                                <td>20 KB</td>
                                                                <td>
                                                                    <div className="avatar-group">
                                                                        <div className="avatar-group-item">
                                                                            <Link to="#" className="d-inline-block">
                                                                                <img src={avatar4} alt="" className="rounded-circle avatar-xs" />
                                                                            </Link>
                                                                        </div>
                                                                        <div className="avatar-group-item">
                                                                            <Link to="#" className="d-inline-block">
                                                                                <img src={avatar5} alt="" className="rounded-circle avatar-xs" />
                                                                            </Link>
                                                                        </div>
                                                                        <div className="avatar-group-item">
                                                                            <Link to="#" className="d-inline-block">
                                                                                <div className="avatar-xs">
                                                                                    <span className="avatar-title rounded-circle bg-success text-white font-size-15">
                                                                                        A
                                                                                    </span>
                                                                                </div>
                                                                            </Link>
                                                                        </div>
                                                                    </div>
                                                                </td>
                                                                <td>
                                                                    <UncontrolledDropdown>
                                                                        <DropdownToggle tag="a" className="font-size-16 text-muted">
                                                                            <i className="mdi mdi-dots-horizontal"></i>
                                                                        </DropdownToggle>
                                                                        <DropdownMenu className="dropdown-menu-end">
                                                                            <DropdownItem href="#">Open</DropdownItem>
                                                                            <DropdownItem href="#">Edit</DropdownItem>
                                                                            <DropdownItem href="#">Rename</DropdownItem>
                                                                            <DropdownItem divider />
                                                                            <DropdownItem href="#">Remove</DropdownItem>
                                                                        </DropdownMenu>
                                                                    </UncontrolledDropdown>
                                                                </td>
                                                            </tr>
                                                            <tr>
                                                                <td><Link to="#" className="text-dark fw-medium"><i className="bx bxs-file font-size-20 align-middle text-primary me-2"></i> starter-page.html</Link></td>
                                                                <td>08-10-2021</td>
                                                                <td>11 KB</td>
                                                                <td>
                                                                    <div className="avatar-group">
                                                                        <div className="avatar-group-item">
                                                                            <Link to="#" className="d-inline-block">
                                                                                <img src={avatar8} alt="" className="rounded-circle avatar-xs" />
                                                                            </Link>
                                                                        </div>
                                                                        <div className="avatar-group-item">
                                                                            <Link to="#" className="d-inline-block">
                                                                                <img src={avatar2} alt="" className="rounded-circle avatar-xs" />
                                                                            </Link>
                                                                        </div>
                                                                    </div>
                                                                </td>
                                                                <td>
                                                                    <UncontrolledDropdown>
                                                                        <DropdownToggle tag="a" className="font-size-16 text-muted">
                                                                            <i className="mdi mdi-dots-horizontal"></i>
                                                                        </DropdownToggle>
                                                                        <DropdownMenu className="dropdown-menu-end">
                                                                            <DropdownItem href="#">Open</DropdownItem>
                                                                            <DropdownItem href="#">Edit</DropdownItem>
                                                                            <DropdownItem href="#">Rename</DropdownItem>
                                                                            <DropdownItem divider />
                                                                            <DropdownItem href="#">Remove</DropdownItem>
                                                                        </DropdownMenu>
                                                                    </UncontrolledDropdown>
                                                                </td>
                                                            </tr>
                                                        </tbody>
                                                    </table>
                                                </div>
                                            </SimpleBar>

                                        </CardBody>
                                    </Card>
                                </div>
                            </div>
                        </div>

                        <Card className="filemanager-sidebar ms-lg-3">
                            <CardBody>
                                <div className="d-flex flex-column h-100">

                                    <div className="mb-4">
                                        <h5 className="font-size-16 me-3 mb-0">Activity Chart</h5>
                                        <div className="text-center">
                                            <ActivityCharts />
                                        </div>

                                        <h5 className="font-size-16 mb-0">Recent Files</h5>

                                        <div className="mt-4">
                                            <div className="pb-2 mb-2">
                                                <Link to="#" className="text-body">
                                                    <div className="d-flex align-items-center">
                                                        <div className="avatar align-self-center me-3">
                                                            <div className="avatar-title rounded bg-success-subtle text-success font-size-24">
                                                                <i className="mdi mdi-image"></i>
                                                            </div>
                                                        </div>
                                                        <div className="overflow-hidden me-auto">
                                                            <h5 className="font-size-15 text-truncate mb-1">Images</h5>
                                                            <p className="text-muted text-truncate mb-0">1,876 Files</p>
                                                        </div>
                                                        <div className="ms-2">
                                                            <p className="text-muted font-size-14">8.4 GB</p>
                                                        </div>
                                                    </div>
                                                </Link>
                                            </div>

                                            <div className="py-2 mb-2">
                                                <Link to="#" className="text-body">
                                                    <div className="d-flex align-items-center">
                                                        <div className="avatar align-self-center me-3">
                                                            <div className="avatar-title rounded bg-danger-subtle text-danger font-size-24">
                                                                <i className="mdi mdi-play-circle-outline"></i>
                                                            </div>
                                                        </div>
                                                        <div className="overflow-hidden me-auto">
                                                            <h5 className="font-size-15 text-truncate mb-1">Video</h5>
                                                            <p className="text-muted text-truncate mb-0">45 Files</p>
                                                        </div>
                                                        <div className="ms-2">
                                                            <p className="text-muted font-size-14">4.1 GB</p>
                                                        </div>
                                                    </div>
                                                </Link>
                                            </div>

                                            <div className="py-2 mb-2">
                                                <Link to="#" className="text-body">
                                                    <div className="d-flex align-items-center">
                                                        <div className="avatar align-self-center me-3">
                                                            <div className="avatar-title rounded bg-info-subtle text-info font-size-24">
                                                                <i className="mdi mdi-music"></i>
                                                            </div>
                                                        </div>
                                                        <div className="overflow-hidden me-auto">
                                                            <h5 className="font-size-15 text-truncate mb-1">Music</h5>
                                                            <p className="text-muted text-truncate mb-0">21 Files</p>
                                                        </div>
                                                        <div className="ms-2">
                                                            <p className="text-muted font-size-14">3.2 GB</p>
                                                        </div>
                                                    </div>
                                                </Link>
                                            </div>

                                            <div className="py-2 mb-2">
                                                <Link to="#" className="text-body">
                                                    <div className="d-flex align-items-center">
                                                        <div className="avatar align-self-center me-3">
                                                            <div className="avatar-title rounded bg-primary-subtle text-primary font-size-24">
                                                                <i className="mdi mdi-file-document"></i>
                                                            </div>
                                                        </div>
                                                        <div className="overflow-hidden me-auto">
                                                            <h5 className="font-size-15 text-truncate mb-1">Document</h5>
                                                            <p className="text-muted text-truncate mb-0">21 Files</p>
                                                        </div>
                                                        <div className="ms-2">
                                                            <p className="text-muted font-size-14">2 GB</p>
                                                        </div>
                                                    </div>
                                                </Link>
                                            </div>

                                            <div className="py-2 mb-2">
                                                <Link to="#" className="text-body">
                                                    <div className="d-flex align-items-center">
                                                        <div className="avatar align-self-center me-3">
                                                            <div className="avatar-title rounded bg-warning-subtle text-warning font-size-24">
                                                                <i className="mdi mdi-folder"></i>
                                                            </div>
                                                        </div>
                                                        <div className="overflow-hidden me-auto">
                                                            <h5 className="font-size-15 text-truncate mb-1">Others</h5>
                                                            <p className="text-muted text-truncate mb-0">20 Files</p>
                                                        </div>
                                                        <div className="ms-2">
                                                            <p className="text-muted font-size-14">1.4 GB</p>
                                                        </div>
                                                    </div>
                                                </Link>
                                            </div>
                                        </div>
                                    </div>

                                    <div className="mt-5 mt-auto">

                                        <Form>
                                            <Dropzone
                                                onDrop={acceptedFiles => {
                                                    handleAcceptedFiles(acceptedFiles);
                                                }}
                                            >
                                                {({ getRootProps, getInputProps }) => (
                                                    <div className="dropzone">
                                                        <div
                                                            className="dz-message needsclick"
                                                            {...getRootProps()}
                                                        >
                                                            <input {...getInputProps()} />
                                                            <div className="mb-3">
                                                                <i className="display-4 text-muted mdi mdi-cloud-upload" />
                                                            </div>
                                                            <h4>Import Files</h4>
                                                        </div>
                                                    </div>
                                                )}
                                            </Dropzone>
                                            <div className="dropzone-previews mt-3" id="file-previews">
                                                {selectedFiles.map((f, i) => {
                                                    return (
                                                        <Card
                                                            className="mt-1 mb-0 shadow-none border dz-processing dz-image-preview dz-success dz-complete"
                                                            key={i + "-file"}
                                                        >
                                                            <div className="p-2">
                                                                <Row className="align-items-center">
                                                                    <Col className="col-auto">
                                                                        <img
                                                                            data-dz-thumbnail=""
                                                                            height="80"
                                                                            className="avatar-sm rounded bg-light"
                                                                            alt={f.name}
                                                                            src={f.preview}
                                                                        />
                                                                    </Col>
                                                                    <Col>
                                                                        <Link
                                                                            to="#"
                                                                            className="text-muted font-weight-bold"
                                                                        >
                                                                            {f.name}
                                                                        </Link>
                                                                        <p className="mb-0">
                                                                            <strong>{f.formattedSize}</strong>
                                                                        </p>
                                                                    </Col>
                                                                </Row>
                                                            </div>
                                                        </Card>
                                                    );
                                                })}
                                            </div>
                                        </Form>
                                    </div>
                                </div>
                            </CardBody>
                        </Card>
                    </div>
                </Container>
            </div>
        </React.Fragment>
    );
};

export default FileManager;
