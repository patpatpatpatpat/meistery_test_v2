import axios from "axios";

const defaultOptions = {
  baseURL: `http://${process.env.REACT_APP_HOST}/`,
  headers: {
    "Content-Type": "application/json",
  },
  xsrfHeaderName: "X-XSRF-TOKEN",
  xsrfCookieName: "csrftoken",
};

const instance = axios.create(defaultOptions);

export const setAuthToken = (token) => {
    if (token) {
      //applying token
      instance.defaults.headers.common["Authorization"] = `Token ${token}`;
    } else {
      //deleting the token from header
      delete instance.defaults.headers.common["Authorization"];
    }
  };
  
export default instance;