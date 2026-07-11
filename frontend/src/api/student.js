import api from "./axios";

const getDashboard = () => api.get("/student/dashboard");

const getProfile = () => api.get("/student/profile");

const updateProfile = (data) => api.put("/student/profile", data);

const getDrives = () => api.get("/student/drives");

const applyDrive = (id) => api.post(`/student/apply/${id}`);

const getApplications = () => api.get("/student/applications");

export {
  getDashboard,
  getProfile,
  updateProfile,
  getDrives,
  applyDrive,
  getApplications,
};
