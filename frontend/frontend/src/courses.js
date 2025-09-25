import React, { useEffect, useState } from "react";
import api from "../api";

export default function Courses() {
  const [courses, setCourses] = useState([]);
  const [title, setTitle] = useState("");

  useEffect(() => {
    fetchCourses();
  }, []);

  const fetchCourses = async () => {
    const res = await api.get("/courses");
    setCourses(res.data);
  };

  const addCourse = async (e) => {
    e.preventDefault();
    await api.post("/courses", { title });
    setTitle("");
    fetchCourses();
  };

  return (
    <div>
      <h2>Courses</h2>
      <form onSubmit={addCourse}>
        <input
          placeholder="Course Title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
        />
        <button type="submit">Add Course</button>
      </form>

      <ul>
        {courses.map((c) => (
          <li key={c.id}>{c.title}</li>
        ))}
      </ul>
    </div>
  );
}