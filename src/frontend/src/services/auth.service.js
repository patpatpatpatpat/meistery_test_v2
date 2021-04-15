import axios from "../api/axios.instance";

export const loginService = (data) => {
  return axios.post("/api/v1/login", data);
};

export const logoutService = () => {
  return axios.get("/api/v1/logout");
};
