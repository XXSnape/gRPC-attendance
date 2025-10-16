import React from "react";
import { Flex, Radio } from "antd";

import LoginForm from "./components/Login";

const onChange = (e) => {
  console.log(`radio checked:${e.target.value}`);
};

function App() {
  return <LoginForm />;
}

export default App;
