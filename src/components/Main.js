import React, { useEffect, useState } from "react";
import {
  getCurrentUserInformation,
  saveUserInformation,
  saveSalesData,
  getSalesData,
} from "../utils/mockApiHelper";
import InputPage from "./InputPage";
import OutputPage from "./OutputPage";
import { getUserRecordService } from "../services/user.service";
import { getCountryCityListService } from "../services/country.service";
import { DashboardContext } from "../pages/Dashboard";

export const MainContext = React.createContext({});

const Main = ({ onLogout }) => {
  const context = React.useContext(DashboardContext);
  const { token, setToken, currentUserId, setCurrentUserId } = context;

  const [userInformation, setUserInformation] = useState({});

  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [age, setAge] = useState("");
  const [gender, setGender] = useState("");
  const [city, setCity] = useState("");
  const [country, setCountry] = useState("");

  const [salesData, setSalesData] = useState([]);
  const [countryList, setCountryList] = useState([]);
  const [showOutput, setShowoutput] = useState(false);
  const [csvData, setcsvData] = useState([]);

  useEffect(() => {
    getUserRecordService(currentUserId).then((response) => {
      if (response.status === 200) {
        setUserInformation(response.data);
      }
    });
    getCountryCityListService().then((response) => {
      if (response.status === 200) {
        setCountryList(response.data);
        console.log("country list", response.data);
      }
    });
    setSalesData(getSalesData());
  }, []);

  useEffect(() => {
    const userInformationIsNotBlankObject =
      Object.keys(userInformation).length > 0 &&
      userInformation.constructor === Object;
    const salesDataIsNotEmpty = salesData.length > 0;
    if (userInformationIsNotBlankObject && salesDataIsNotEmpty) {
      setShowoutput(true);
    }
  }, [userInformation, salesData]);

  useEffect(() => {
    const userInformation = getCurrentUserInformation();
    const salesData = getSalesData();
    if (salesData && showOutput) {
      const rows = salesData.filter(
        (item) => item.userId === userInformation?.userId
      );
      setcsvData([...rows]);
    }
  }, [showOutput]);

  const handleReset = () => {
    setShowoutput(false);
    setcsvData([]);
    saveUserInformation({});
    saveSalesData([]);
  };

  return (
    <MainContext.Provider
      value={{
        name,
        setName,
        email,
        setEmail,
        age,
        setAge,
        gender,
        setGender,
        city,
        setCity,
        country,
        setCountry,
      }}
    >
      {!showOutput && (
        <InputPage
          setcsvData={setcsvData}
          setShowoutput={setShowoutput}
          userInformation={userInformation}
          setUserInformation={setUserInformation}
          countryList={countryList}
        />
      )}
      {!!showOutput && (
        <OutputPage
          handleReset={handleReset}
          userInformation={userInformation}
          countryList={countryList}
        />
      )}
    </MainContext.Provider>
  );
};
export default Main;
