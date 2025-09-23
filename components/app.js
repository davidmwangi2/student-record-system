import React from "react";
import StudentForm from "./components/StudentForm";
import StudentList from "./components/StudentList";

function App() {
  return (
    <div className="min-h-screen p-8">
      <h1 className="text-3xl font-bold mb-6 text-center">🎓 Student Record System</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <StudentForm />
        <StudentList />
      </div>
    </div>
  );
}

export default App;
