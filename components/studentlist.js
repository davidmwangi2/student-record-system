import React, { useState } from "react";

function StudentList() {
  const [students] = useState([
    { id: 1, name: "Alice", course: "Mathematics" },
    { id: 2, name: "Bob", course: "Physics" },
    { id: 3, name: "Charlie", course: "Computer Science" },
  ]);

  return (
    <div className="bg-white shadow-md rounded-lg p-6">
      <h2 className="text-xl font-semibold mb-4">Student Records</h2>
      <ul className="space-y-2">
        {students.map((student) => (
          <li
            key={student.id}
            className="border p-2 rounded flex justify-between"
          >
            <span>{student.name}</span>
            <span className="text-gray-600">{student.course}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default StudentList;
