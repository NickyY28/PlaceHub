import api from "./axios";

const getDashboard = () => api.get("/admin/dashboard");

const getUsers = () => api.get("/admin/users");

const blockUser = (id) => api.patch(`/admin/users/${id}/block`);

const unblockUser = (id) => api.patch(`/admin/users/${id}/unblock`);

const deleteUser = (id) => api.delete(`/admin/users/${id}`);

const getCompanies = () => api.get("/admin/companies");

const getStudents = () => api.get("/admin/students");

const getDrives = () => api.get("/admin/drives");

const deleteDrive = (id) => api.delete(`/admin/drives/${id}`);

export {
  getDashboard,
  getUsers,
  blockUser,
  unblockUser,
  deleteUser,
  getCompanies,
  getStudents,
  getDrives,
  deleteDrive,
};
