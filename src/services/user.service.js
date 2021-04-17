import axios from "../api/axios.instance";

export const createUserService = (data) => {
    return axios.post("/api/v1/users", data);
  };
export const getUserRecordService = (id) => {
    return axios.get(`/api/v1/users/${id}`);
  };
export const updateUserService = (id, data) => {
  return axios.patch(`/api/v1/users/${id}`, data);
}