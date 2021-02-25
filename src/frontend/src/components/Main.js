import React, { useEffect, useState } from "react";
import { getCurrentUserInformation, saveUserInformation, saveSalesData, getSalesData } from "../utils/mockApiHelper";
import InputPage from "./InputPage";
import OutputPage from "./OutputPage";

const Main = ({ onLogout }) => {
  const [showOutput, setShowoutput] = useState(false);
  const [csvData, setcsvData] = useState([]);

  useEffect(() => {
    const userInformation = getCurrentUserInformation();
    const salesData = getSalesData();

    if (userInformation?.name && salesData?.length) {
      setShowoutput(true);
    }
  }, []);

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
    <>
      {!showOutput && (
        <InputPage
          onLogout={onLogout}
          setcsvData={setcsvData}
          setShowoutput={setShowoutput}
        />
      )}
      {!!showOutput && (
        <OutputPage
          handleReset={handleReset}
          onLogout={onLogout}
        />
      )}
    </>
  );
};
export default Main;
