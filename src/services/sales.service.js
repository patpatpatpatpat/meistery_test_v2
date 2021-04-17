import axios from "../api/axios.instance";

export const createSalesRecordService = (data) => {
  return axios.post("/api/v1/sales", data);
};

export const getSalesRecordService = (id) => {
  return axios.get(`/api/v1/sales/${id}`);
};

export const getSalesListService = () => {
  return axios.get("/api/v1/sales");
};

export const getSalesStatisticsService = () => {
  return axios.get(`/api/v1/sale_statistics`);
};
