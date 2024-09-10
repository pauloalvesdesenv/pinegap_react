import PropTypes from "prop-types";
import React, { useEffect, useCallback } from "react";

import withRouter from "../Common/withRouter";
import {
  changeLayout,
  changeSidebarTheme,
  changeLayoutMode,
  changeTopbarTheme,
  changeSidebarSize,
  changeLayoutWidth,
  showRightSidebarAction,
} from "../../store/actions";

import Header from "./Header";
import Sidebar from "./Sidebar";
import Footer from "./Footer";
import Rightbar from "../CommonForBoth/Rightbar";

//redux
import { useSelector, useDispatch } from "react-redux";
import { createSelector } from 'reselect';

const Layout = (props) => {
  const dispatch = useDispatch();

  

  const selectLayoutState = (state) => state.Layout;
    const selectLayoutProperties = createSelector(
        selectLayoutState,
        (layout) => ({
          isPreloader: layout.isPreloader,
          leftSideBarType: layout.leftSideBarType,
          layoutModeType: layout.layoutModeType,
          layoutWidth: layout.layoutWidth,
          topbarTheme: layout.topbarTheme,
          sidebarSizeType: layout.sidebarSizeType,
          showRightSidebar: layout.showRightSidebar,
          leftSideBarTheme: layout.leftSideBarTheme
        })
    );

    const {
          isPreloader,
          leftSideBarType,
          layoutModeType,
          layoutWidth,
          topbarTheme,
          sidebarSizeType,
          showRightSidebar,
          leftSideBarTheme
    } = useSelector(selectLayoutProperties);    

  const isMobile = /iPhone|iPad|iPod|Android/i.test(navigator.userAgent);

  const toggleMenuCallback = () => {
    if (leftSideBarType === "default") {
      dispatch(changeSidebarSize("condensed", isMobile));
    } else if (leftSideBarType === "condensed") {
      dispatch(changeSidebarSize("default", isMobile));
    }
  };

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
  layout  settings
  */

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
    window.scrollTo(0, 0);
  }, []);

  useEffect(() => {
    dispatch(changeLayout("vertical"));
  }, [dispatch]);

  useEffect(() => {
    if (leftSideBarTheme) {
      dispatch(changeSidebarTheme(leftSideBarTheme));
    }
  }, [leftSideBarTheme, dispatch]);
  useEffect(() => {
    if (layoutWidth) {
      dispatch(changeLayoutWidth(layoutWidth));
    }
  }, [layoutWidth, dispatch]);

  useEffect(() => {
    if (sidebarSizeType) {
      dispatch(changeSidebarSize(sidebarSizeType));
    }
  }, [sidebarSizeType, dispatch]);

  useEffect(() => {
    if (layoutModeType) {
      dispatch(changeLayoutMode(layoutModeType));
    }
  }, [layoutModeType, dispatch]);

  useEffect(() => {
    if (topbarTheme) {
      dispatch(changeTopbarTheme(topbarTheme));
    }
  }, [topbarTheme, dispatch]);

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
        <Header toggleMenuCallback={toggleMenuCallback} />
        <Sidebar
          theme={leftSideBarTheme}
          // type={leftSideBarType}
          isMobile={isMobile}
        />
        <div className="main-content">{props.children}</div>
        <Footer />
      </div>
      {showRightSidebar ? <Rightbar /> : null}
    </React.Fragment>
  );
};

Layout.propTypes = {
  changeLayoutWidth: PropTypes.func,
  changeLayoutMode: PropTypes.func,
  changeSidebarTheme: PropTypes.func,
  changeSidebarSize: PropTypes.func,
  changeTopbarTheme: PropTypes.func,
  children: PropTypes.object,
  isPreloader: PropTypes.any,
  layoutModeType: PropTypes.any,
  layoutWidth: PropTypes.any,
  leftSideBarTheme: PropTypes.any,
  leftSideBarType: PropTypes.any,
  location: PropTypes.object,
  showRightSidebar: PropTypes.any,
  topbarTheme: PropTypes.any,
};

export default withRouter(Layout);
