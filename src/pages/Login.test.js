import React from "react";
import renderer from "react-test-renderer";
import Login from "./Login";

test("if it renders correctly", () => {
  const tree = renderer
    .create(
      <Login
        onLoginSuccess={() => {
          console.log("login success!!");
        }}
      />
    )
    .toJSON();
  expect(tree).toMatchSnapshot();
});
