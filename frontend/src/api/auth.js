import api from "./axios";

const loginUser = (data) => api.post("/auth/login", data);

const getMe = () => api.get("/auth/me");

const registerStudent = (data) => api.post("/auth/register/student", data);

const registerCompany = (data) => api.post("/auth/register/company", data);

export { loginUser, getMe, registerStudent, registerCompany };
