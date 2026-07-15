import api from "./axios";

const getDashboard = () => api.get("/admin/dashboard");

const updateCompanyApproval = (companyId, status) => {
  return api.patch(`/admin/companies/${companyId}/approval`, {
    status,
  });
};

const getUsers = () => api.get("/admin/users");

const blockUser = (id) => api.patch(`/admin/users/${id}/block`);

const unblockUser = (id) => api.patch(`/admin/users/${id}/unblock`);

const deleteUser = (id) => api.delete(`/admin/users/${id}`);

const getCompanies = () => api.get("/admin/companies");

const getStudents = () => api.get("/admin/students");

const getDrives = () => api.get("/admin/drives");

const deleteDrive = (id) => api.delete(`/admin/drives/${id}`);

const generateMonthlyReport = () => api.post("/admin/generate-monthly-report");

const getReportStatus = (taskId) => api.get(`/admin/report-status/${taskId}`);

const downloadReport = (filename) =>
  api.get(`/admin/download-report/${filename}`, {
    responseType: "blob",
  });

export {
  getDashboard,
  updateCompanyApproval,
  getUsers,
  blockUser,
  unblockUser,
  deleteUser,
  getCompanies,
  getStudents,
  getDrives,
  deleteDrive,
  generateMonthlyReport,
  getReportStatus,
  downloadReport,
};
