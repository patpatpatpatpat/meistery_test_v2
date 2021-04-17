import React from "react";
import {
  Table,
  TableCell,
  TableRow,
  TableContainer,
  TableHead,
  TableBody,
  Paper,
} from "@material-ui/core";

const StatTable = (props) => {
  const data = props.data;

  if (!data || data === undefined || Object.keys(data).length === 0) {
    return null;
  }

  const columns = [
    { field: "avgSaleCurrentUser", headerName: "" },
    { field: "avgSale", headerName: "" },
    { field: "", headerName: "" },
    {
      field: "mostRevenueEarningProduct",
      headerName: "",
    },
    { field: "mostSoldProduct", headerName: "" },
  ];

  return (
    <div style={{ height: 400, width: "100%" }}>
      <TableContainer component={Paper}>
        <Table style={{ minWidth: 700 }} aria-label="spanning table">
          <TableHead>
            <TableRow>
              <TableCell align="center">Average Sales for Employee</TableCell>
              <TableCell align="center">Average Sales for All Employees</TableCell>
              <TableCell align="center">Highest Revenue Sale</TableCell>
              <TableCell align="center">Highest Revenue Product</TableCell>
              <TableCell align="center">Highest Selling Product</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            <TableRow>
              <TableCell>
                <Table component={Paper}>
                  <TableHead>
                    <TableRow>
                      <TableCell>UserName</TableCell>
                      <TableCell>Average</TableCell>
                    </TableRow>
                    <TableRow>
                      <TableCell>{props.currentUserName}</TableCell>
                      <TableCell>{data.avgSaleCurrentUser}</TableCell>
                    </TableRow>
                  </TableHead>
                </Table>
              </TableCell>
              <TableCell>
                <Table component={Paper}>
                  <TableHead>
                    <TableRow>
                      <TableCell>Average</TableCell>
                    </TableRow>
                    <TableRow>
                      <TableCell>{data.avgSale}</TableCell>
                    </TableRow>
                  </TableHead>
                </Table>
              </TableCell>
              <TableCell>
                <Table component={Paper}>
                  <TableHead>
                    <TableRow>
                      <TableCell>Product Name</TableCell>
                      <TableCell>Revenue</TableCell>
                    </TableRow>
                    <TableRow>
                      <TableCell>{data.mostExpensiveProduct.product}</TableCell>
                      <TableCell>{Number(data.mostExpensiveProduct.revenue)}</TableCell>
                    </TableRow>
                  </TableHead>
                </Table>
              </TableCell>
              <TableCell>
                <Table component={Paper}>
                  <TableHead>
                    <TableRow>
                      <TableCell>Product Name</TableCell>
                      <TableCell>Total Revenue</TableCell>
                    </TableRow>
                    <TableRow>
                      <TableCell>{data.mostRevenueEarningProduct.name}</TableCell>
                      <TableCell>{data.mostRevenueEarningProduct.revenue}</TableCell>
                    </TableRow>
                  </TableHead>
                </Table>
              </TableCell>
              <TableCell>
                <Table component={Paper}>
                  <TableHead>
                    <TableRow>
                      <TableCell>Product Name</TableCell>
                      <TableCell>Total Sales</TableCell>
                    </TableRow>
                    <TableRow>
                      <TableCell>{data.mostSoldProduct.name}</TableCell>
                      <TableCell>{data.mostSoldProduct.count}</TableCell>
                    </TableRow>
                  </TableHead>
                </Table>
              </TableCell>
            </TableRow>
          </TableBody>
        </Table>
      </TableContainer>
    </div>
  );
};

export default StatTable;
