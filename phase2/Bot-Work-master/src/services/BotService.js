const API_URL = "http://localhost:3000/bots";

const getBots = async () => {
  const res = await fetch(API_URL);
  return res.json();
};

const deleteBot = async (id) => {
  await fetch(`${API_URL}/${id}`, { method: "DELETE" });
};

export default { getBots, deleteBot };
