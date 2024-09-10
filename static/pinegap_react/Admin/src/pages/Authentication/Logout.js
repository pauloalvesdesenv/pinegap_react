import PropTypes from 'prop-types'
import React, { useEffect } from "react"
import { connect, useDispatch } from "react-redux"
import withRouter from '../../components/Common/withRouter'

import { logoutUser } from "../../store/actions"
import { useNavigate } from 'react-router-dom';

const Logout = () => {

  document.title=" Logout | Minible - Responsive Bootstrap 5 Admin Dashboard"

  const history = useNavigate();
  const dispatch = useDispatch();

  useEffect(() => {
    dispatch(logoutUser(history));
  }, [dispatch, history]);

  return <></>
}

Logout.propTypes = {
  history: PropTypes.object,
  logoutUser: PropTypes.func
}

export default withRouter(connect(null, { logoutUser })(Logout));
