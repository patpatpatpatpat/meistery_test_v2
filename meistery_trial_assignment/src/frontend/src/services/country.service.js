import axios from "../api/axios.instance";

export const getCountryCityListService = () => {
    return axios.get("/api/v1/country_data");
  };