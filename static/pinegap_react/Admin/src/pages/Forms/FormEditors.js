import React from "react"

import {
  Form,
  Card,
  CardBody,
  Col,
  Row,
  CardTitle,
  CardSubtitle,
  Container,
} from "reactstrap"

// Form Editor
import { Editor } from "react-draft-wysiwyg"
import "react-draft-wysiwyg/dist/react-draft-wysiwyg.css"

//Import Breadcrumb
import Breadcrumbs from "../../components/Common/Breadcrumb"

const FormEditors = () => {

  document.title=" Form Editors | Minible - Responsive Bootstrap 5 Admin Dashboard"

  return (
    <React.Fragment>
      <div className="page-content">
        <Container fluid={true}>
          <Breadcrumbs title="Forms" breadcrumbItem="Form Editors" />

          <Row>
            <Col>
              <Card>
                <CardBody>
                  <CardTitle>React-draft-wysiwyg</CardTitle>
                  <CardSubtitle className="mb-3">
                  React-draft-wysiwyg is a external react package that makes it
                    easy to create simple, beautiful wysiwyg editors with the
                    help of ReactJS and DraftJS libraries.
                  </CardSubtitle>
                  <Form method="post" className="wysiwyg-custom">
                    <Editor
                      toolbarClassName="toolbarClassName"
                      wrapperClassName="wrapperClassName"
                      editorClassName="editorClassName"
                    />
                  </Form>
                </CardBody>
              </Card>
            </Col>
          </Row>
        </Container>
      </div>
    </React.Fragment>
  )
}

export default FormEditors
