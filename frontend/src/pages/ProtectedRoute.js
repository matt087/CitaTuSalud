import React from 'react';
import { Navigate } from 'react-router-dom';

const ProtectedRoute = ({ isAuthenticated, children, requiredRole, userRole }) => {
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }
  if (userRole !== requiredRole) {
    return <Navigate to="/" replace />;
  }
  return children;
};

export default ProtectedRoute;
