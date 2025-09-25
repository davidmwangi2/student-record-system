
import React, { useState } from "react";

function Enrollments() {
  const [enrollments, setEnrollments] = useState([
    { id: 1, student: "Alice", course: "Math" },
    { id: 2, student: "Bob", course: "Physics" },
  ]);

  return (
    <div className="p-6">
      <h2 className="text-xl font-bold mb-4">Enrollments</h2>
      <ul className="list-disc pl-6">
        {enrollments.map((enrollment) => (
          <li key={enrollment.id}>
            {enrollment.student} enrolled in {enrollment.course}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Enrollments;
