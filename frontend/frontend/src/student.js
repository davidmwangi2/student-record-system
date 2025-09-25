import React, { useState } from "react";

function Students() {
  const [students, setStudents] = useState([
    { id: 1, name: "Alice", course: "Math" },
    { id: 2, name: "Bob", course: "Physics" },
  ]);

  return (
    <div className="p-6">
      <h2 className="text-xl font-bold mb-4">Students</h2>
      <ul className="list-disc pl-6">
        {students.map((student) => (
          <li key={student.id}>
            {student.name} - {student.course}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Students;
