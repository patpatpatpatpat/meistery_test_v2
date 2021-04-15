import userData from "../api/user";
import {
  getMostExpensiveProduct,
  getMostRevenueEarningProduct,
  getMostSoldProduct,
  getAverageSale,
} from "./helpers";

/**
 * Mock API for getting authentication token if we find a match for the given email and password in the mock user data.
 * @param {string} email
 * @param {string} password
 */
export const getAuthToken = (email, password, users) => {
  const currentUser = userData.find(
    (item) => item.email === email && item.password === password
  );
  if (currentUser?.authToken) {
    localStorage.setItem("authToken", currentUser.authToken);
    localStorage.setItem("currentUserId", currentUser.id);
    return currentUser.authToken;
  }
  return null;
};

/**
 * Logout procedure and cleaning up localStorage.
 */
export const logout = () => {
  localStorage.removeItem("authToken");
  localStorage.removeItem("currentUserId");
  localStorage.removeItem("currentUserInformation");
  localStorage.removeItem('salesData');
};

/**
 * Mock API for current user information.
 */
export const getCurrentUserInformation = () => {
  return JSON.parse(localStorage.getItem("currentUserInformation"));
};

/**
 * Save user information in localStorage.
 * @param {object} userInformation
 */
export const saveUserInformation = (userInformation) => {
  return localStorage.setItem(
    "currentUserInformation",
    JSON.stringify({
      ...userInformation,
      userId: localStorage.getItem("currentUserId"),
    })
  );
};

/**
 * Saves saleData in the localStorage
 * @param {array} salesData
 */
export const saveSalesData = (salesData) => {
  localStorage.setItem("salesData", JSON.stringify(salesData));
};

/**
 * Get saleData from the localStorage
 */
export const getSalesData = () => {
  const salesDataStr = localStorage.getItem("salesData");
  console.log("salesDataStr", salesDataStr);
  if (salesDataStr) {
    return JSON.parse(salesDataStr);
  }
  return [];
};

/**
 * Generate the aggregated data for showing in the statistics table.
 */
export const getAggregatedData = () => {
  const currentUserId = localStorage.getItem("currentUserId");
  const salesData = getSalesData();
  const currentUserSalesData = salesData.filter(
    (item) => item.userId === currentUserId
  );
  return {
    avgSaleCurrentUser: getAverageSale(currentUserSalesData),
    avgSale: getAverageSale(salesData),
    mostExpensiveProduct: getMostExpensiveProduct(currentUserSalesData),
    mostRevenueEarningProduct: getMostRevenueEarningProduct(
      currentUserSalesData
    ),
    mostSoldProduct: getMostSoldProduct(currentUserSalesData),
  };
};

export const generateToken = (max) => {
  var s = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ';
  var n = s.length-1;
  var token = '';
  for (var i = 0; i < max; i++) {
      token += s.charAt(Math.floor(Math.random() * n));
  }
  return token;
}
