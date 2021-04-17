import "../api/axios.instance"
import axios

export const getCountryCityListService = () => {
    return axios.get("/api/v1/countries");
  };