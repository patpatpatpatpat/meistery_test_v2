import React, { useEffect, useState } from "react";
import TextField from "@material-ui/core/TextField";
import InputLabel from "@material-ui/core/InputLabel";
import MenuItem from "@material-ui/core/MenuItem";
import FormControl from "@material-ui/core/FormControl";
import FormHelperText from "@material-ui/core/FormHelperText";
import Select from "@material-ui/core/Select";
import Grid from "@material-ui/core/Grid";
import useStyles from "../layout/Style";
import { Typography } from "@material-ui/core";
import Button from "@material-ui/core/Button";
import { logout } from "../utils/mockApiHelper";
import {
  preProcessData,
  sortSaleData,
  isValidEmail,
  isValidName,
} from "../utils/helpers";
import { countries, cities, genders, sortKeys } from "../data";
import Papa from "papaparse";
import {
  getCurrentUserInformation,
  saveUserInformation,
  saveSalesData,
} from "../utils/mockApiHelper";
import Dialog from "./Dialog";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import { isValid } from "date-fns";

const InputPage = ({ onLogout, setShowoutput, setcsvData }) => {
  const classes = useStyles();
  const [name, setName] = useState();
  const [email, setEmail] = useState("");
  const [age, setAge] = useState("");
  const [gender, setGender] = useState("");
  const [city, setCity] = useState("");
  const [country, setCountry] = useState("");
  const [file, setFile] = useState();
  const [rawData, setRawData] = useState();
  const [cityList, setCityList] = useState([]);
  const [openDialog, setOpenDialog] = useState(false);
  const [hasError, setHasError] = useState(false);
  const [hasUpdatedUserInformation, setHasUpdatedUserInformation] = useState(
    false
  );

  useEffect(() => {
    const userInformation = getCurrentUserInformation();
    if (userInformation?.name) {
      setName(userInformation.name);
      setAge(userInformation.age);
      setEmail(userInformation.email);
      setGender(userInformation.gender);
      setCountry(userInformation.country);
      setCity(userInformation.city);
      setCityList(cities[userInformation.country]);
    }
  }, []);

  const btnEnabeled =
    !!name &&
    !!email &&
    !!age &&
    !!gender &&
    !!city &&
    !!country &&
    hasUpdatedUserInformation &&
    (!!file || !!rawData);

  const handleReset = () => {
    setName("");
    setEmail("");
    setAge("");
    setGender("");
    setCity("");
    setCountry("");
    setFile();
    setShowoutput(false);
    setcsvData("");
    setRawData("");
    setHasError(false);
    saveUserInformation({});
    saveSalesData([]);
    setHasUpdatedUserInformation(false);
  };

  const onUpdateUserInformation = () => {
    const canUpdateInformation = name && email && gender && country && city;
    if (!canUpdateInformation) {
      toast.error("Please fill up the missing user informations!!!");
      setHasError(true);
      return;
    }

    const userInformationObject = {
      email,
      name,
      gender,
      age,
      country,
      city,
      userId: localStorage.getItem("currentUserId"),
    };

    fetch("/api/userinformation", {
      method: "post",
      body: JSON.stringify(userInformationObject),
    })
      .then((res) => res.json())
      .then((data) => {
        setHasError(false);
        saveUserInformation(userInformationObject);
        setHasUpdatedUserInformation(true);
        toast.success("Successfully updated user information");
      })
      .catch((err) => console.log(err));
  };

  /**
   * Converts the parsed array data from csv file to csv string, and display set rawData prop to display
   * it in Manual CSV Data input field
   *
   * @param {array} data - parsed array of objects from csv file
   */
  const updateData = (data) => {
    const csv = Papa.unparse(data.data);
    setRawData(csv);
  };

  /**
   * Checks if data is already available in Manual CSV Data input field
   * if available, then open confirmation dialog and ask user for confirmation to replace data
   * If not available, then call handleCSVUpload to prepare data for chart and table
   */
  const confirmUpload = () => {
    if (!!rawData) {
      setOpenDialog(true);
    } else {
      handleCSVUpload();
    }
  };

  /**
   * Validate the uploaded file type, if it's not in text/csv format, then display error
   * If file is valid, parse the file and execute callback function
   */
  const handleCSVUpload = () => {
    if (!!file && file.type === "text/csv") {
      Papa.parse(file, {
        complete: updateData,
      });
    } else {
      toast.error("Please upload valid csv file");
    }
    setOpenDialog(false);
  };

  /**
   * This function actully parse the final data used to show table and charts in output screen
   * Check if rawData (comma seprated string) exists, if yes then convert it to array and call showOutPut function
   */
  const handleSubmit = () => {
    if (!!rawData) {
      Papa.parse(rawData, {
        complete: onShowOutPut,
      });
    }
  };

  /**
   * Set csvData prop and shows the ocountriesutput page
   */
  const onShowOutPut = (data) => {
    data.data.shift();
    const rows = sortSaleData(preProcessData(data.data), sortKeys[0]);
    fetch("/api/sales", {
      method: "post",
      body: JSON.stringify(rows),
    })
      .then((res) => res.json())
      .then((data) => {
        saveSalesData(data.sales); // saving sales data in local storage using mock API call.
        setShowoutput(true);
        // toast.success("Successfully updated user information");
      })
      .catch((err) => console.log(err));
  };

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
      <Typography variant="h6">User</Typography>
      <Grid container spacing={3} alignItems={"center"}>
        <Grid item xs={6}>
          <TextField
            error={(hasError && !name) || (name && !isValidName(name))}
            helperText={
              !name && hasError
                ? "Name can not be empty"
                : name && !isValidName(name)
                ? "Name should have first name and last name"
                : ""
            }
            id="name"
            label="Name"
            variant="outlined"
            fullWidth={true}
            onChange={(event) => {
              setName(event.target.value);
            }}
            value={name}
          />
        </Grid>
        <Grid item xs={3}>
          <FormControl variant="outlined" className={classes.formControl}>
            <InputLabel id="demo-simple-select-outlined-label">
              Gender
            </InputLabel>
            <Select
              error={hasError && !gender}
              labelId="demo-simple-select-outlined-label"
              id="demo-simple-select-outlined"
              value={gender}
              onChange={(event) => {
                setGender(event.target.value);
              }}
              label="Gender"
            >
              {genders.map((item, index) => (
                <MenuItem value={item} key={index}>
                  {item}
                </MenuItem>
              ))}
            </Select>
            {!gender && hasError && (
              <FormHelperText error>Gender can not be empty</FormHelperText>
            )}
          </FormControl>
        </Grid>
        <Grid item xs={3}>
          <FormControl variant="outlined" className={classes.formControl}>
            <InputLabel id="demo-simple-select-outlined-label">Age</InputLabel>
            <Select
              error={hasError && !age}
              labelId="demo-simple-select-outlined-label"
              id="demo-simple-select-outlined"
              value={age}
              onChange={(event) => {
                setAge(event.target.value);
              }}
              label="Age"
            >
              {[...Array(121)].map((elementInArray, index) => (
                <MenuItem value={index} key={index}>
                  {index}
                </MenuItem>
              ))}
            </Select>
            {!age && hasError && (
              <FormHelperText error>Age can not be empty</FormHelperText>
            )}
          </FormControl>
        </Grid>
        <Grid item xs={6}>
          <TextField
            error={(hasError && !email) || (email && !isValidEmail(email))}
            helperText={
              !email && hasError
                ? "Email can not be empty"
                : email && !isValidEmail(email)
                ? "Please insert a valid email address."
                : ""
            }
            id="email"
            label="Email"
            variant="outlined"
            fullWidth={true}
            value={email}
            onChange={(event) => {
              setEmail(event.target.value);
            }}
          />
        </Grid>
        <Grid item xs={3}>
          <FormControl variant="outlined" className={classes.formControl}>
            <InputLabel id="demo-simple-select-outlined-label">
              Country
            </InputLabel>
            <Select
              error={hasError && !country}
              labelId="demo-simple-select-outlined-label"
              id="demo-simple-select-outlined"
              value={country}
              onChange={(event) => {
                setCountry(event.target.value);
                setCity("");
                setCityList(cities[event.target.value]);
              }}
              label="Country"
            >
              {countries.map((item) => (
                <MenuItem value={item} key={item}>
                  {item}
                </MenuItem>
              ))}
            </Select>
            {!country && hasError && (
              <FormHelperText error>Country can not be empty</FormHelperText>
            )}
          </FormControl>
        </Grid>
        <Grid item xs={3}>
          <FormControl variant="outlined" className={classes.formControl}>
            <InputLabel id="demo-simple-select-outlined-label">City</InputLabel>
            <Select
              error={hasError && !city}
              labelId="demo-simple-select-outlined-label"
              id="demo-simple-select-outlined"
              value={city}
              onChange={(event) => {
                setCity(event.target.value);
              }}
              label="City"
            >
              {cityList.map((item) => (
                <MenuItem value={item}>{item}</MenuItem>
              ))}
            </Select>
            {!city && hasError && (
              <FormHelperText error>City can not be empty</FormHelperText>
            )}
          </FormControl>
        </Grid>
      </Grid>
      <Grid container spacing={3}>
        <Grid item xs={12} style={{ textAlign: "left" }}>
          <Button
            variant="contained"
            size="medium"
            color="secondary"
            onClick={onUpdateUserInformation}
          >
            Update User Data
          </Button>
        </Grid>
      </Grid>
      <br />
      <Typography variant="h6">Input Data</Typography>
      <Grid container spacing={3}>
        <Grid item xs={10}>
          <TextField
            id="name"
            variant="outlined"
            type="file"
            fullWidth={true}
            onChange={(event) => {
              setFile(event.target.files[0]);
            }}
            accept="csv"
          />
        </Grid>
        <Grid item xs={2}>
          <Button
            variant="contained"
            size="large"
            color="primary"
            className={classes.margin}
            style={{
              float: "right",
              height: 55,
              width: "100%",
            }}
            onClick={confirmUpload}
            disabled={!file}
          >
            Upload File
          </Button>
        </Grid>
        <Grid item xs={12}>
          <TextField
            label="Manual CSV Data Input"
            multiline
            rows={10}
            variant="outlined"
            rowsMax={10}
            fullWidth={true}
            onChange={(event) => {
              setRawData(event.target.value);
            }}
            InputLabelProps={{
              shrink: true,
            }}
            value={rawData}
          />
        </Grid>
      </Grid>
      <Grid container spacing={3}>
        <Grid item xs={12} style={{ textAlign: "center" }}>
          <Button
            variant="contained"
            size="medium"
            color="primary"
            className={classes.margin}
            disabled={!btnEnabeled}
            style={{ marginRight: 20 }}
            onClick={handleSubmit}
          >
            Upload
          </Button>
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
      <Dialog
        openDialog={openDialog}
        handleCloseDialog={() => {
          setOpenDialog(false);
        }}
        handleAccept={handleCSVUpload}
      />
      <ToastContainer />
    </>
  );
};
export default InputPage;
