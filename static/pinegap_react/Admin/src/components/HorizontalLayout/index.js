import React, { useEffect, useState, useCallback } from "react";
import  withRouter  from "../Common/withRouter";
import PropTypes from "prop-types";

import {
  changeLayout,
  changeLayoutMode,
  changeTopbarTheme,
  changeLayoutWidth,
  showRightSidebarAction,
} from "../../store/actions";

//redux
import { useSelector, useDispatch } from "react-redux";
import { createSelector } from "reselect";

// Other Layout related Component
import Navbar from "./Navbar";
import Header from "./Header";
import Footer from "./Footer";
import Rightbar from "../CommonForBoth/Rightbar";
import { useLocation } from "react-router-dom";

const Layout = (props) => {
  const dispatch = useDispatch();
  const selectLayoutState = (state) => state.Layout;
  const selectLayoutProperties = createSelector(
    selectLayoutState,
    (layout) => ({
      topbarTheme: layout.topbarTheme,
      layoutModeType: layout.layoutModeType,
      layoutWidth: layout.layoutWidth,
      isPreloader: layout.isPreloader,
      showRightSidebar: layout.showRightSidebar,

    })
  );
  const {
    topbarTheme,
    layoutModeType,
    layoutWidth,
    isPreloader,
    showRightSidebar
  } = useSelector(selectLayoutProperties);
  
const path = useLocation();
  useEffect(() => {
    const title = path.pathname;
    let currentage = title.charAt(1).toUpperCase() + title.slice(2);

    document.title = currentage + " | Minible - React Admin & Dashboard Template";
  }, [path.pathname]);

  useEffect(() => {
    window.scrollTo(0, 0);
  }, []);

  //hides right sidebar on body click
  const hideRightbar = useCallback((event) => {
    var rightbar = document.getElementById("right-bar");
    //if clicked in inside right bar, then do nothing
    if (rightbar && rightbar.contains(event.target)) {
      return;
    } else {
      //if clicked in outside of rightbar then fire action for hide rightbar
      dispatch(showRightSidebarAction(false));
    }
  }, [dispatch]);

  /*
  layout settings
  */
  useEffect(() => {
    dispatch(changeLayout("horizontal"));
  }, [dispatch]);

  const pathName = props.router.location.pathname;

  useEffect(() => {
    //init body click event fot toggle rightbar
    document.body.addEventListener("click", hideRightbar, true);

    if (isPreloader === true) {
      document.getElementById("preloader").style.display = "block";
      document.getElementById("status").style.display = "block";

      setTimeout(function () {
        document.getElementById("preloader").style.display = "none";
        document.getElementById("status").style.display = "none";
      }, 2500);
    } else {
      document.getElementById("preloader").style.display = "none";
      document.getElementById("status").style.display = "none";
    }
  }, [isPreloader, hideRightbar, pathName]);

  useEffect(() => {
    if (topbarTheme) {
      dispatch(changeTopbarTheme(topbarTheme));
    }
  }, [dispatch, topbarTheme]);

  useEffect(() => {
    if (layoutModeType) {
      dispatch(changeLayoutMode(layoutModeType));
    }
  }, [dispatch, layoutModeType]);

  useEffect(() => {
    if (layoutWidth) {
      dispatch(changeLayoutWidth(layoutWidth));
    }
  }, [dispatch, layoutWidth]);

  const [isMenuOpened, setIsMenuOpened] = useState(false);
  const openMenu = () => {
    setIsMenuOpened(!isMenuOpened);
  };

  return (
    <React.Fragment>
      <div id="preloader">
        <div id="status">
          <div className="spinner">
            <i className="uil-shutter-alt spin-icon"></i>
          </div>
        </div>
      </div>

      <div id="layout-wrapper">
        <header id="page-topbar">
          <Header
            theme={topbarTheme}
            isMenuOpened={isMenuOpened}
            openLeftMenuCallBack={openMenu}
          ></Header>
          <Navbar menuOpen={isMenuOpened} />
        </header>
        <div className="main-content">{props.children}</div>
        <Footer />
      </div>

      {showRightSidebar ? <Rightbar /> : null}
    </React.Fragment>
  );
};

Layout.propTypes = {
  changeLayout: PropTypes.func,
  changeLayoutWidth: PropTypes.func,
  changeTopbarTheme: PropTypes.func,
  children: PropTypes.object,
  isPreloader: PropTypes.any,
  layoutWidth: PropTypes.any,
  location: PropTypes.object,
  showRightSidebar: PropTypes.any,
  topbarTheme: PropTypes.any,
};

export default withRouter(Layout);
