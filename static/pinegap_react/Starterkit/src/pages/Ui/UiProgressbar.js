import React from "react";
import { Button, Card, CardBody, CardTitle, Col, Container, Progress, Row } from "reactstrap";

//Import Breadcrumb
import Breadcrumbs from "../../components/Common/Breadcrumb";

const UiProgressbar = () => {

  document.title=" Progressbar | Minible - Responsive Bootstrap 5 Admin Dashboard"

  return (
    <React.Fragment>
      <div className="page-content">
        <Container fluid={true}>
          <Breadcrumbs title="UI Elements" breadcrumbItem="Progress Bars" />

          <Row>
            <Col xl={6}>
              <Card>
                <CardBody>
                  <CardTitle className="h4">Default Examples</CardTitle>
                  <p className="card-title-desc">
                    Progress components are built with two HTML elements, some
                    CSS to set the width, and a few attributes.
                  </p>

                  <div>
                    <div className="mb-4">
                      <Progress color="primary" value={25} />
                    </div>

                    <div className="mb-4">
                      <Progress color="primary" value={50} />
                    </div>

                    <div className="mb-4">
                      <Progress color="primary" value={75} />
                    </div>

                    <div>
                      <Progress color="primary" value={100} />
                    </div>
                  </div>
                </CardBody>
              </Card>
            </Col>

            <Col xl={6}>
              <Card>
                <CardBody>
                  <CardTitle className="h4">Backgrounds</CardTitle>
                  <p className="card-title-desc">
                    Use background utility classes to change the appearance of
                    individual progress bars.
                  </p>

                  <div>
                    <div className="mb-4">
                      <Progress color="success" value={25} />
                    </div>

                    <div className="mb-4">
                      <Progress color="info" value={50} />
                    </div>

                    <div className="mb-4">
                      <Progress color="warning" value={75} />
                    </div>

                    <div>
                      <Progress color="danger" value={100} />
                    </div>
                  </div>
                </CardBody>
              </Card>
            </Col>
          </Row>

          <Row>
            <Col xl={6}>
              <Card>
                <CardBody>
                  <CardTitle className="h4">Labels Example</CardTitle>
                  <p className="card-title-desc">
                    Add labels to your progress bars by placing text within the{" "}
                    <code className="highlighter-rouge">.progress-bar</code>.
                  </p>

                  <div className="">
                    <div>
                      <Progress color="primary" value={25}>
                        25%
                      </Progress>
                    </div>
                  </div>
                </CardBody>
              </Card>
            </Col>

            <Col xl={6}>
              <Card>
                <CardBody>
                  <CardTitle className="h4">Multiple bars</CardTitle>
                  <p className="card-title-desc">
                    Include multiple progress bars in a progress component if
                    you need.
                  </p>

                  <div className="">
                    <Progress multi>
                      <Progress bar color="primary" value={15} />
                      <Progress bar color="success" value={30} />
                      <Progress bar color="info" value={20} />
                    </Progress>
                  </div>
                </CardBody>
              </Card>
            </Col>
          </Row>

          <Row>
            <Col xl={6}>
              <Card>
                <CardBody>
                  <CardTitle className="h4">Height</CardTitle>
                  <p className="card-title-desc">
                    We only set a{" "}
                    <code className="highlighter-rouge">height</code> value on
                    the <code className="highlighter-rouge">  .progress-bar</code>
                    , so if you change that value the outer{" "}
                    <code className="highlighter-rouge">.progress</code> will
                    automatically resize accordingly.
                  </p>

                  <div className="">
                    <div className="mb-3">
                      <Progress
                        className="mb-2 progress-sm"
                        value={25}
                        color="primary"
                        style={{ height: "3px" }}
                      />
                    </div>
                    <Progress
                      className="mb-2"
                      value={25}
                      color="primary"
                      style={{ height: "20px" }}
                    />
                  </div>
                </CardBody>
              </Card>
            </Col>

            <Col xl={6}>
              <Card>
                <CardBody>
                  <CardTitle className="h4">Animated stripes</CardTitle>
                  <p className="card-title-desc">
                    The striped gradient can also be animated. Add{" "}
                    <code className="highlighter-rouge">
                      {" "}
                      .progress-bar-animated{" "}
                    </code>{" "}  <code
                      className="highlighter-rouge">.progress-bar</code>
                    to animate the
                    stripes right to left via CSS3 animations.
                  </p>

                  <div className="">
                    <Progress striped animated color="primary" value="75" />
                  </div>
                </CardBody>
              </Card>
            </Col>
          </Row>

          <Row>
            <Col xl={6}>
              <Card>
                <CardBody>
                  <CardTitle className="h4">Striped</CardTitle>
                  <p className="card-title-desc">Add <code className="highlighter-rouge">.progress-bar-striped</code>
                    to any <code className="highlighter-rouge">.progress-bar</code> to apply a
                    stripe via CSS gradient over the progress bar’s background color.</p>

                  <div className="">
                    <div className="mb-4">
                      <Progress striped color="primary" value={10} />
                    </div>

                    <div className="mb-4">
                      <Progress striped color="success" value={25} />
                    </div>

                    <div className="mb-4">
                      <Progress striped color="info" value={50} />
                    </div>

                    <div className="mb-4">
                      <Progress striped color="warning" value={75} />
                    </div>

                    <div>
                      <Progress striped color="danger" value={100} />
                    </div>
                  </div>
                </CardBody>
              </Card>
            </Col>
            <Col xl={6}>
              <Card>
                <CardBody>
                  <CardTitle className="h4">Animated Progress</CardTitle>
                  <p className="card-title-desc">Add <code className="highlighter-rounge">.animated-progess</code> class with <code className="highlighter-rounge">.progress-bar</code> for animated progressbar.</p>

                  <div className="">
                    <div className="mb-4 p-1">
                      <Progress color="success" value={25} />
                    </div>

                    <div className="mb-4 p-1">
                      <Progress color="info" value={50} />
                    </div>

                    <div className="mb-4 p-1">
                      <Progress color="warning" value={75} />
                    </div>

                    <div className="mb-4 p-1">
                      <Progress color="danger" value={100} />
                    </div>

                  </div>
                </CardBody>
              </Card>
            </Col>
          </Row>

          <Row>
            <Col xl={6}>
              <Card>
                <CardBody>
                  <h4 className="card-title">Custom progress</h4>
                  <p className="card-title-desc">Custom progress
                    Example of Custom progress</p>

                  <div className="pt-2">
                    <div className="custom-progess mb-5">
                      <Progress multi className="progress-sm">
                        <Progress color="danger" bar value={84} />
                      </Progress>
                      <div className="avatar-xs progress-icon">
                        <span className="avatar-title rounded-circle border border-danger">
                          <i className="bx bxl-html5 text-danger font-size-18"></i>
                        </span>
                      </div>
                    </div>

                    <div className="custom-progess mb-5">
                      <Progress multi className="progress-sm">
                        <Progress color="primary" bar value={75} />
                      </Progress>
                      <div className="avatar-xs progress-icon">
                        <span className="avatar-title rounded-circle border border-primary">
                          <i className="bx bxl-css3 text-primary font-size-18"></i>
                        </span>
                      </div>
                    </div>
                    <div className="custom-progess mb-2">
                      <Progress multi className="progress-sm">
                        <Progress color="info" bar value={62} />
                      </Progress>
                      <div className="avatar-xs progress-icon">
                        <span className="avatar-title rounded-circle border border-info">
                          <i className="bx bxl-jquery text-info font-size-18"></i>
                        </span>
                      </div>
                    </div>
                  </div>

                </CardBody>
              </Card>
            </Col>

            <Col xl={6}>
              <Card>
                <CardBody>
                  <h4 className="card-title">Progress Example</h4>
                  <p className="card-title-desc">You can use these classes with existing components to create new ones.</p>

                  <div className="mt-5">
                    <div className="position-relative m-4">
                      <Progress multi style={{ height: "1px" }}>
                        <Progress color="primary" bar value={50} />
                      </Progress>
                      <Button color="primary" size="sm" type="button" className="position-absolute top-0 start-0 translate-middle rounded-pill" style={{ width: "2rem", height: "2rem" }}>1</Button>
                      <Button color="primary" size="sm" type="button" className="position-absolute top-0 start-50 translate-middle rounded-pill" style={{ width: "2rem", height: "2rem" }}>2</Button>
                      <Button color="secondary" size="sm" type="button" className="position-absolute top-0 start-100 translate-middle rounded-pill" style={{ width: "2rem", height: "2rem" }}>3</Button>
                    </div>
                  </div>


                </CardBody>
              </Card>

            </Col>

          </Row>
        </Container>
      </div>
    </React.Fragment>
  );
};

export default UiProgressbar;
