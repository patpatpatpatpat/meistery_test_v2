import {
  sampleSalesData,
  sampleDataSortedByDate,
  sampleDataSortedByProduct
} from "../sample-data/sample-sales-data";
import { sortSaleData } from "./helpers";

test("if sortSaleData can sort data properly by date", () => {
  const sortedData = sortSaleData(sampleSalesData, "date");
  expect(JSON.stringify(sortedData)).toBe(
    JSON.stringify(sampleDataSortedByDate)
  );
});


test("if sortSaleData can sort data properly by product", () => {
	const sortedData = sortSaleData(sampleSalesData, "product");
	expect(JSON.stringify(sortedData)).toBe(
	  JSON.stringify(sampleDataSortedByProduct)
	);
  });
