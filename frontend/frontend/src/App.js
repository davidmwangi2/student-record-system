
import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Students from "./student";
import Enrollments from "./enrollments"; 
import "./App.css";
import "./index.css";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Students />} />
        <Route path="/enrollments" element={<Enrollments />} />
      </Routes>
    </Router>
  );
}

export default App;
