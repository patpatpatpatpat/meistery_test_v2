import React, { useState } from "react";
import Grid from "@material-ui/core/Grid";
import Paper from "@material-ui/core/Paper";
import Login from "./Login";
import useStyles from "../layout/Style";
import Main from "../components/Main";
import { belongsTo, createServer, hasMany, Model } from "miragejs";
import saleData from "../api/sales_data";
import userData from "../api/user";
import {
  getAverageSale,
  getMostExpensiveProduct,
  getMostRevenueEarningProduct,
  getMostSoldProduct,
} from "../utils/helpers";
import { generateToken } from "../utils/mockApiHelper";

createServer({
  models: {
    user: Model,
    sale: Model.extend({
      user: belongsTo(),
    }),
    userinformation: Model,
  },

  seeds(server) {
    userData.forEach((user) => {
      server.create("user", user);
    });
  },

  routes() {
    this.post("/api/token", (schema, request) => {
      var users = schema.users.all().models;
      var data = JSON.parse(request.requestBody);

      const user = users.find((item) => {
        return item.email === data.email && item.password === data.password;
      });

      if (user && user.password === data.password) {
        var token = generateToken(64);
        return {
          access_token: token,
          token_type: "Bearer",
          user_id: user.id,
        };
      } else {
        return Response(
          401,
          {},
          {
            code: 401,
            message: "Invalid username and/or password, please try again",
          }
        );
      }
    });

    this.post("/api/userinformation", (schema, request) => {
      const payLoad = JSON.parse(request.requestBody);
      schema.db.userinformations.insert(payLoad);
      return { userinformation: payLoad };
    });

    this.get("/api/userinformation/:userId", (schema, request) => {
      const currentUserInfo = schema.userinformations
        .all()
        .models.find((item) => {
          return item.userId === request.params.userId;
        });

      return { userInformation: currentUserInfo };
    });

    this.post("/api/sales", (schema, request) => {
      const payLoad = JSON.parse(request.requestBody);
      schema.db.sales.insert(payLoad);
      return { sales: payLoad };
    });

    this.get("/api/sales/:userId", (schema, request) => {
      const currentUserId = request.params.userId;
      const salesData = schema.sales.all().models;
      const currentUserSalesData = salesData.filter(
        (item) => item.userId === currentUserId
      );
      return { sales: currentUserSalesData };
    });

    this.get("/api/aggregated_data/:userId", (schema, request) => {
      const currentUserId = request.params.userId;
      const salesData = schema.sales.all().models;
      const currentUserSalesData = salesData.filter(
        (item) => item.userId === currentUserId
      );
      return {
        aggregatedData: {
          avgSaleCurrentUser: getAverageSale(currentUserSalesData),
          avgSale: getAverageSale(salesData),
          mostExpensiveProduct: getMostExpensiveProduct(currentUserSalesData),
          mostRevenueEarningProduct: getMostRevenueEarningProduct(
            currentUserSalesData
          ),
          mostSoldProduct: getMostSoldProduct(currentUserSalesData),
        },
      };
    });
  },
});

const Dashboard = () => {
  const classes = useStyles();
  const [token, setToken] = useState(localStorage.getItem("authToken"));

  if (!token) {
    return (
      <Login
        onLoginSuccess={setToken}
      />
    );
  }
  return (
    <Paper className={classes.control}>
      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Main onLogout={setToken} />
        </Grid>
      </Grid>
    </Paper>
  );
};

export default Dashboard;
