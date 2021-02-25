import React, { useEffect, useState } from "react";
import InputLabel from "@material-ui/core/InputLabel";
import MenuItem from "@material-ui/core/MenuItem";
import FormControl from "@material-ui/core/FormControl";
import Select from "@material-ui/core/Select";
import Grid from "@material-ui/core/Grid";
import useStyles from "../layout/Style";
import { Typography } from "@material-ui/core";
import Button from "@material-ui/core/Button";
import { logout } from "../utils/mockApiHelper";
import { sortSaleData } from "../utils/helpers";
import Table from "./Table";
import Chart from "./Chart";
import StatTable from "./StatTable";
import { chartFilters, sortKeys } from "../data";
import "react-toastify/dist/ReactToastify.css";

const OutputPage = ({ onLogout, handleReset }) => {
  const [userInfo, setUserInfo] = useState({});
  const [name, setName] = useState();
  const [email, setEmail] = useState("");
  const [age, setAge] = useState("");
  const [gender, setGender] = useState("");
  const [city, setCity] = useState("");
  const [country, setCountry] = useState("");
  const [aggregatedData, setAggregatedData] = useState({});
  const classes = useStyles();

  const [csvData, setcsvData] = useState([]);
  const [chartFilter, setChartFilter] = useState(chartFilters[0]);
  const [orderBy, setOrderBy] = useState(sortKeys[0]);

  useEffect(() => {
    /**
     * Expected response:
     * {
     *    userInformation: {
     *      name: string, 
     *      email: string, 
     *      age: number, 
     *      gender: string, 
     *      city: string, 
     *      country: string 
     *    }
     * }
     */
    fetch("/api/userinformation/" + localStorage.getItem("currentUserId"))
      .then((res) => res.json())
      .then((data) => {
        setUserInfo(data.userInformation);
      });

      /**
       * Expected response:
       * {
       *    sales: {
       *        date: string
       *        id: string
       *        product: string
       *        revenue: string
       *        sales_number: string
       *        userId: string
       *    }
       * }
       */
    fetch("/api/sales/" + localStorage.getItem("currentUserId"))
      .then((res) => res.json())
      .then((data) => {
        console.log(data.sales);
        setcsvData([...data.sales]);
      });

    /**
     * Expected Response:
     * {
     *  "aggregatedData":{
     *       "avgSaleCurrentUser": number,
     *       "avgSale": number,
     *       "mostExpensiveProduct":{
     *         "userId": string,
     *         "id": string,
     *         "date": string,
     *         "product": string,
     *         "sales_number": string,
     *         "revenue": string
     *       },
     *       "mostRevenueEarningProduct":{
     *         "name": string,
     *         "revenue": number
     *       },
     *       "mostSoldProduct":{
     *         "name": string,
     *         "count": number
     *       }
     *   }
     * }
     */
    fetch("/api/aggregated_data/" + localStorage.getItem("currentUserId"))
      .then((res) => res.json())
      .then((data) => {
        setAggregatedData(data.aggregatedData);
      });
  }, []);

  useEffect(() => {
    if (userInfo?.name) {
      const { name, email, age, gender, city, country } = userInfo;
      setName(name);
      setEmail(email);
      setAge(age);
      setGender(gender);
      setCity(city);
      setCountry(country);
    }
  }, [userInfo]);

  useEffect(() => {
    if (csvData && csvData.length) {
      const rows = sortSaleData(csvData, orderBy);
      setcsvData([...rows]);
    }
  }, [orderBy]);

  return (
    <>
      <Grid container spacing={3}>
        <Grid item xs={12} style={{ textAlign: "right" }}>
          <Button
            variant="contained"
            size="medium"
            color="secondary"
            onClick={() => {
              logout();
              onLogout(localStorage.getItem("authToken"));
            }}
          >
            Logout
          </Button>
        </Grid>
      </Grid>
      <Typography variant="h6">Personal Information</Typography>
      <Grid container spacing={8}>
        <Grid item xs={6}>
          <Grid container spacing={3}>
            <Grid item xs={6}>
              <p style={{ textAlign: "left", fontWeight: "bolder" }}>Name :</p>
            </Grid>
            <Grid item xs={6}>
              <p style={{ textAlign: "right" }}>{name}</p>
            </Grid>
          </Grid>
          <hr />
          <Grid container spacing={3}>
            <Grid item xs={6}>
              <p style={{ textAlign: "left", fontWeight: "bolder" }}>Age :</p>
            </Grid>
            <Grid item xs={6}>
              <p style={{ textAlign: "right" }}>{age}</p>
            </Grid>
          </Grid>
          <hr />
          <Grid container spacing={3}>
            <Grid item xs={6}>
              <p style={{ textAlign: "left", fontWeight: "bolder" }}>
                Gender :
              </p>
            </Grid>
            <Grid item xs={6}>
              <p style={{ textAlign: "right" }}>{gender}</p>
            </Grid>
          </Grid>
          <hr />
        </Grid>
        <Grid item xs={6}>
          <Grid container spacing={4}>
            <Grid item xs={6}>
              <p style={{ textAlign: "left", fontWeight: "bolder" }}>Email :</p>
            </Grid>
            <Grid item xs={6}>
              <p style={{ textAlign: "right" }}>{email}</p>
            </Grid>
          </Grid>
          <hr />
          <Grid container spacing={3}>
            <Grid item xs={6}>
              <p style={{ textAlign: "left", fontWeight: "bolder" }}>
                Country :
              </p>
            </Grid>
            <Grid item xs={6}>
              <p style={{ textAlign: "right" }}>{country}</p>
            </Grid>
          </Grid>
          <hr />
          <Grid container spacing={3}>
            <Grid item xs={6}>
              <p style={{ textAlign: "left", fontWeight: "bolder" }}>City :</p>
            </Grid>
            <Grid item xs={6}>
              <p style={{ textAlign: "right" }}>{city}</p>
            </Grid>
          </Grid>
          <hr />
        </Grid>
      </Grid>
      {csvData?.length && (
        <Grid container spacing={8}>
          <Grid item xs={6}>
            <Grid container xs={12}>
              <Grid item lg={9}>
                <Typography variant="h6">Data</Typography>
              </Grid>
              <Grid item lg={3}>
                <FormControl variant="outlined" className={classes.formControl}>
                  <InputLabel id="demo-simple-select-outlined-label">
                    OrderBy
                  </InputLabel>
                  <Select
                    labelId="demo-simple-select-outlined-label"
                    id="demo-simple-select-outlined"
                    value={orderBy}
                    onChange={(event) => {
                      setOrderBy(event.target.value);
                    }}
                    label="OrderBy"
                  >
                    {sortKeys.map((item, index) => (
                      <MenuItem value={item} key={index}>
                        {item}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Grid>
            </Grid>
            <Table data={csvData} />
          </Grid>
          <Grid item xs={6}>
            <Grid container xs={12}>
              <Grid item lg={9}>
                <Typography variant="h6">Chart</Typography>
              </Grid>
              <Grid item lg={3}>
                <FormControl variant="outlined" className={classes.formControl}>
                  <InputLabel id="demo-simple-select-outlined-label">
                    Y-Axis
                  </InputLabel>
                  <Select
                    labelId="demo-simple-select-outlined-label"
                    id="demo-simple-select-outlined"
                    value={chartFilter}
                    onChange={(event) => {
                      setChartFilter(event.target.value);
                    }}
                    label="YAxis"
                  >
                    {chartFilters.map((item, index) => (
                      <MenuItem value={item} key={index}>
                        {item}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Grid>
            </Grid>
            <Chart data={csvData} yAxisLabel={chartFilter} />
          </Grid>
        </Grid>
      )}
      {aggregatedData && (
        <Grid container spacing={8}>
          <Grid item lg={12}>
            <Typography variant="h6">Statistics Table</Typography>
          </Grid>
          <Grid item lg={12}>
            <Grid container>
              <StatTable data={aggregatedData} currentUserName={name} />
            </Grid>
          </Grid>
        </Grid>
      )}
      <Grid container spacing={3}>
        <Grid item xs={12} style={{ textAlign: "center" }}>
          <Button
            variant="contained"
            size="medium"
            color="secondary"
            onClick={handleReset}
          >
            Reset
          </Button>
        </Grid>
      </Grid>
    </>
  );
};
export default OutputPage;
