import api from "./axios";

const getDashboard = () => api.get("/company/dashboard");

const getProfile = () => api.get("/company/profile");

const updateProfile = (data) => api.put("/company/profile", data);

const getDrives = () => api.get("/drives");

const getDrive = (id) => api.get(`/drives/${id}`);

const createDrive = (data) => api.post("/drives", data);

const updateDrive = (id, data) => api.put(`/drives/${id}`, data);

const deleteDrive = (id) => api.delete(`/drives/${id}`);

const getApplications = () => api.get("/applications");

const updateApplicationStatus = (id, data) =>
  api.patch(`/applications/${id}`, data);

export {
  getDashboard,
  getProfile,
  updateProfile,
  getDrives,
  getDrive,
  createDrive,
  updateDrive,
  deleteDrive,
  getApplications,
  updateApplicationStatus,
};
