import React from "react";

import { Col, Row, Container, Card, CardBody } from "reactstrap";
//Import Breadcrumb
import Breadcrumbs from "../../components/Common/Breadcrumb";

const UiColors = () => {

  document.title=" Colors | Minible - Responsive Bootstrap 5 Admin Dashboard"

  return (
    <React.Fragment>
      <div className="page-content">
        <Container fluid={true}>
          <Breadcrumbs title="UI Elements" breadcrumbItem="Colors" />

          <Row>
            <Col xl={4}>
              <Card>
                <CardBody>
                  <h5 className="mb-3 font-size-18 text-center">Hex : #5b73e8</h5>
                  <Row>

                    <Col lg={4}>
                      <div className="text-center">
                        <div className="avatar-md bg-primary-subtle mx-auto rounded my-2"></div>
                        <h6 className="text-muted mt-3">bg-primary-subtle</h6>
                      </div>
                    </Col>

                    <Col lg={4}>
                      <div className="text-center">
                        <div className="avatar-md bg-gradient-primary mx-auto rounded my-2"></div>
                        <h6 className="text-muted mt-3">bg-gradient-primary</h6>
                      </div>
                    </Col>

                    <Col lg={4}>
                      <div className="text-center">
                        <div className="avatar-md bg-primary mx-auto rounded my-2"></div>
                        <h6 className="text-muted mt-3">bg-primary</h6>
                      </div>
                    </Col>
                  </Row>
                </CardBody>
              </Card>
            </Col>
            <Col xl={4}>
              <Card>
                <CardBody className="text-center">
                  <h5 className="mb-3 text-center">Hex : #34c38f</h5>
                  <Row>

                    <Col lg={4}>
                      <div className="text-center">
                        <div className="avatar-md bg-soft-success mx-auto rounded my-2"></div>
                        <h6 className="text-muted mt-3">bg-soft-success</h6>
                      </div>
                    </Col>

                    <Col lg={4}>
                      <div className="text-center">
                        <div className="avatar-md bg-gradient-success mx-auto rounded my-2"></div>
                        <h6 className="text-muted mt-3">bg-gradient-success</h6>

                      </div>
                    </Col>

                    <Col lg={4}>
                      <div className="text-center">
                        <div className="avatar-md bg-success mx-auto rounded my-2"></div>
                        <h6 className="text-muted mt-3">bg-success</h6>
                      </div>
                    </Col>

                  </Row>
                </CardBody>
              </Card>
            </Col>
            <Col xl={4}>
              <Card>
                <CardBody className="text-center">
                  <h5 className="mb-3 text-center">Hex : #50a5f1</h5>
                  <Row>

                    <Col lg={4}>
                      <div className="text-center">
                        <div className="avatar-md bg-soft-info mx-auto rounded my-2"></div>
                        <h6 className="text-muted mt-3">bg-soft-info</h6>
                      </div>
                    </Col>

                    <Col lg={4}>
                      <div className="text-center">
                        <div className="avatar-md bg-gradient-info mx-auto rounded my-2"></div>
                        <h6 className="text-muted mt-3">bg-gradient-info</h6>

                      </div>
                    </Col>

                    <Col lg={4}>
                      <div className="text-center">
                        <div className="avatar-md bg-info mx-auto rounded my-2"></div>
                        <h6 className="text-muted mt-3">bg-info</h6>
                      </div>
                    </Col>

                  </Row>
                </CardBody>
              </Card>
            </Col>
            <Col xl={4}>
              <Card>
                <CardBody className="text-center">
                  <h5 className="mb-3 text-center">Hex : #f1b44c</h5>
                  <Row>

                    <Col lg={4}>
                      <div className="text-center">
                        <div className="avatar-md bg-warning-subtle mx-auto rounded my-2"></div>
                        <h6 className="text-muted mt-3">bg-warning-subtle</h6>
                      </div>
                    </Col>

                    <Col lg={4}>
                      <div className="text-center">
                        <div className="avatar-md bg-gradient-warning mx-auto rounded my-2"></div>
                        <h6 className="text-muted mt-3">bg-gradient-warning</h6>

                      </div>
                    </Col>

                    <Col lg={4}>
                      <div className="text-center">
                        <div className="avatar-md bg-warning mx-auto rounded my-2"></div>
                        <h6 className="text-muted mt-3">bg-warning</h6>
                      </div>
                    </Col>
                  </Row>
                </CardBody>
              </Card>
            </Col>
            <Col xl={4}>
              <Card>
                <CardBody className="text-center">
                  <h5 className="mb-3 text-center">Hex : #f46a6a</h5>
                  <Row>

                    <Col lg={4}>
                      <div className="text-center">
                        <div className="avatar-md bg-soft-danger mx-auto rounded my-2"></div>
                        <h6 className="text-muted mt-3">bg-soft-danger</h6>
                      </div>
                    </Col>

                    <Col lg={4}>
                      <div className="text-center">
                        <div className="avatar-md bg-gradient-danger mx-auto rounded my-2"></div>
                        <h6 className="text-muted mt-3">bg-gradient-danger</h6>

                      </div>
                    </Col>

                    <Col lg={4}>
                      <div className="text-center">
                        <div className="avatar-md bg-danger mx-auto rounded my-2"></div>
                        <h6 className="text-muted mt-3">bg-danger</h6>
                      </div>
                    </Col>
                  </Row>
                </CardBody>
              </Card>
            </Col>
            <Col xl={4}>
              <Card>
                <CardBody className="text-center">
                  <h5 className="mb-3 text-center">Hex : #343a40</h5>
                  <Row>

                    <Col lg={4}>
                      <div className="text-center">
                        <div className="avatar-md bg-soft-dark mx-auto rounded my-2"></div>
                        <h6 className="text-muted mt-3">bg-soft-dark</h6>
                      </div>
                    </Col>

                    <Col lg={4}>
                      <div className="text-center">
                        <div className="avatar-md bg-gradient-dark mx-auto rounded my-2"></div>
                        <h6 className="text-muted mt-3">bg-gradient-dark</h6>

                      </div>
                    </Col>

                    <Col lg={4}>
                      <div className="text-center">
                        <div className="avatar-md bg-dark mx-auto rounded my-2"></div>
                        <h6 className="text-muted mt-3">bg-dark</h6>
                      </div>
                    </Col>
                  </Row>
                </CardBody>
              </Card>
            </Col>
            <Col xl={4}>
              <Card>
                <CardBody className="text-center">
                  <h5 className="mb-3 text-center">Hex : #f5f6f8</h5>
                  <Row>

                    <Col lg={4}>
                      <div className="text-center">
                        <div className="avatar-md bg-soft-light mx-auto rounded my-2"></div>
                        <h6 className="text-muted mt-3">bg-soft-light</h6>
                      </div>
                    </Col>

                    <Col lg={4}>
                      <div className="text-center">
                        <div className="avatar-md bg-gradient-light mx-auto rounded my-2"></div>
                        <h6 className="text-muted mt-3">bg-gradient-light</h6>

                      </div>
                    </Col>

                    <Col lg={4}>
                      <div className="text-center">
                        <div className="avatar-md bg-light mx-auto rounded my-2"></div>
                        <h6 className="text-muted mt-3">bg-light</h6>
                      </div>
                    </Col>
                  </Row>
                </CardBody>
              </Card>
            </Col>
            <Col xl={4}>
              <Card>
                <CardBody className="text-center">
                  <h5 className="mb-3 text-center">Hex : #74788d</h5>
                  <Row>

                    <Col lg={4}>
                      <div className="text-center">
                        <div className="avatar-md bg-soft-secondary mx-auto rounded my-2"></div>
                        <h6 className="text-muted mt-3">bg-soft-secondary</h6>
                      </div>
                    </Col>

                    <Col lg={4}>
                      <div className="text-center">
                        <div className="avatar-md bg-gradient-secondary mx-auto rounded my-2"></div>
                        <h6 className="text-muted mt-3">bg-gradient-secondary</h6>

                      </div>
                    </Col>

                    <Col lg={4}>
                      <div className="text-center">
                        <div className="avatar-md bg-secondary mx-auto rounded my-2"></div>
                        <h6 className="text-muted mt-3">bg-secondary</h6>
                      </div>
                    </Col>
                  </Row>
                </CardBody>
              </Card>
            </Col>
            <Col xl={4}>
              <Card>
                <CardBody>
                  <h5 className="mb-3 text-center">Body</h5>
                  <Row>
                    <Col lg={4}>
                      <div className="text-center">
                        <div className="avatar-md bg-body mx-auto rounded my-2"></div>
                        <h6 className="text-muted mt-3">bg-body</h6>
                      </div>
                    </Col>

                    <Col lg={4}>
                      <div className="text-center">
                        <div className="avatar-md bg-body-tertiary mx-auto rounded my-2"></div>
                        <h6 className="text-muted mt-3">bg-body-tertiary</h6>

                      </div>
                    </Col>

                    <Col lg={4}>
                      <div className="text-center">
                        <div className="avatar-md bg-body-secondary mx-auto rounded my-2"></div>
                        <h6 className="text-muted mt-3">bg-body-secondary</h6>
                      </div>
                    </Col>
                  </Row>
                </CardBody>
              </Card>
            </Col>

            <Col xl={4}>
              <Card>
                <CardBody>
                  <h5 className="mb-3 text-center">Opacity</h5>
                  <Row>
                    <Col lg={4}>
                      <div className="text-center">
                        <div className="avatar-md bg-primary opacity-75 mx-auto rounded my-2"></div>
                        <h6 className="text-muted mt-3">opacity-75</h6>
                      </div>
                    </Col>

                    <Col lg={4}>
                      <div className="text-center">
                        <div className="avatar-md bg-primary opacity-50 mx-auto rounded my-2"></div>
                        <h6 className="text-muted mt-3">opacity-50</h6>

                      </div>
                    </Col>

                    <Col lg={4}>
                      <div className="text-center">
                        <div className="avatar-md bg-primary opacity-25 mx-auto rounded my-2"></div>
                        <h6 className="text-muted mt-3">opacity-25</h6>
                      </div>
                    </Col>
                  </Row>
                </CardBody>
              </Card>
            </Col>

            <Col xl={4}>
              <Card>
                <CardBody>
                  <h5 className="mb-3 text-center">Other</h5>
                  <Row>
                    <Col lg={4}>
                      <div className="text-center">
                        <div className="avatar-md bg-black mx-auto rounded my-2"></div>
                        <h6 className="text-muted mt-3">bg-black</h6>
                      </div>
                    </Col>

                    <Col lg={4}>
                      <div className="text-center">
                        <div className="avatar-md bg-white mx-auto rounded my-2 border"></div>
                        <h6 className="text-muted mt-3">bg-white</h6>

                      </div>
                    </Col>

                    <Col lg={4}>
                      <div className="text-center">
                        <div className="avatar-md bg-transparent mx-auto rounded my-2 border"></div>
                        <h6 className="text-muted mt-3">bg-transparent</h6>
                      </div>
                    </Col>
                  </Row>
                </CardBody>
              </Card>
            </Col>

            <Col xl={12}>
              <Card>
                <CardBody>
                  <h5 className="mb-3 text-center">Text Color</h5>
                  <Row>
                    <div className="col">
                      <div className="">
                        <h6 className="text-primary mt-3">text-primary</h6>
                        <h6 className="text-primary-emphasis mt-3">text-primary-emphasis</h6>
                        <h6 className="text-secondary mt-3">text-secondary</h6>
                        <h6 className="text-secondary-emphasis mt-3">text-secondary-emphasis</h6>
                        <h6 className="text-success mt-3">text-success</h6>
                      </div>
                    </div>

                    <div className="col">
                      <h6 className="text-success-emphasis mt-3">text-success-emphasis</h6>
                      <h6 className="text-info mt-3">text-info</h6>
                      <h6 className="text-info-emphasis mt-3">text-info-emphasis</h6>
                      <h6 className="text-warning mt-3">text-warning</h6>
                    </div>

                    <div className="col">
                      <div className="">
                        <h6 className="text-warning-emphasis mt-3">text-warning-emphasis</h6>
                        <h6 className="text-danger mt-3">text-danger</h6>
                        <h6 className="text-danger-emphasis mt-3">text-danger-emphasis</h6>
                        <h6 className="text-reset mt-3">text-dark</h6>
                      </div>
                    </div>

                    <div className="col">
                      <h6 className="text-dark-emphasis mt-3">text-dark-emphasis</h6>
                      <h6 className="text-white bg-dark mt-3">text-light</h6>
                      <h6 className="text-light-emphasis mt-3">text-light-emphasis</h6>
                      <h6 className="text-body mt-3">text-body</h6>
                    </div>

                    <div className="col">
                      <div className="">
                        <h6 className="text-muted mt-3">text-muted</h6>
                        <h6 className="text-body-emphasis mt-3">text-body-emphasis</h6>
                        <h6 className="text-body-secondary mt-3">text-body-secondary</h6>
                        <h6 className="text-body-tertiary mt-3">text-body-tertiary</h6>
                      </div>
                    </div>

                    <div className="col">
                      <h6 className="text-black mt-3">text-black</h6>
                      <h6 className="text-white bg-dark mt-3">text-white</h6>
                      <h6 className="text-black-50 mt-3">text-black-50</h6>
                      <h6 className="text-white-50 b bg-dark mt-3">text-white-50</h6>
                    </div>

                    <div className="col">
                      <div>
                        <h6 className="text-body text-opacity-100 mt-3">text-opacity-100</h6>
                        <h6 className="text-body text-opacity-75 mt-3">text-opacity-75</h6>
                        <h6 className="text-body text-opacity-50 mt-3">text-opacity-50</h6>
                        <h6 className="text-body text-opacity-25 mt-3">text-opacity-25</h6>
                      </div>
                    </div>
                  </Row>
                </CardBody>
              </Card>
            </Col>
          </Row>
        </Container>
      </div>
    </React.Fragment>
  );
};

export default UiColors;
