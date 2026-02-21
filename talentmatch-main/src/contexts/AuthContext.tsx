import React, { createContext, useState, useContext, useEffect, ReactNode } from 'react';
import { UserSession, UserRole, Permission, AuthContextType } from '../types/rbac.types';

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<UserSession | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  // Mock permissions mapping for demo
  const getPermissionsForRole = (role: UserRole): Permission[] => {
    const permissions: Record<UserRole, Permission[]> = {
      [UserRole.ADMIN]: [
        Permission.CREATE_JOB,
        Permission.EDIT_JOB,
        Permission.DELETE_JOB,
        Permission.VIEW_ALL_JOBS,
        Permission.VIEW_ALL_CANDIDATES,
        Permission.EDIT_CANDIDATE,
        Permission.SCORE_CANDIDATE,
        Permission.CONFIGURE_AI,
        Permission.VIEW_ANALYTICS
      ],
      [UserRole.RECRUITER]: [
        Permission.CREATE_JOB,
        Permission.EDIT_JOB,
        Permission.VIEW_ALL_JOBS,
        Permission.VIEW_ALL_CANDIDATES,
        Permission.SCORE_CANDIDATE
      ],
      [UserRole.HIRING_MANAGER]: [
        Permission.VIEW_ALL_JOBS,
        Permission.VIEW_ALL_CANDIDATES,
        Permission.SCORE_CANDIDATE
      ],
      [UserRole.INTERVIEWER]: [
        Permission.VIEW_ALL_JOBS,
        Permission.SCORE_CANDIDATE
      ],
      [UserRole.CANDIDATE]: []
    };
    return permissions[role] || [];
  };

  // Check for existing session on load
  useEffect(() => {
    const checkAuth = async () => {
      const token = localStorage.getItem('auth_token');
      const userData = localStorage.getItem('user_data');
      
      if (token && userData) {
        try {
          const parsedUser = JSON.parse(userData);
          setUser(parsedUser);
        } catch (error) {
          console.error('Failed to parse user data:', error);
          logout();
        }
      }
      setIsLoading(false);
    };
    
    checkAuth();
  }, []);

  const login = async (email: string, password: string) => {
    // For demo purposes - in production, call your backend
    setIsLoading(true);
    try {
      // Mock API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      // Determine role from email for demo
      let role: UserRole = UserRole.CANDIDATE;
      if (email.includes('admin')) role = UserRole.ADMIN;
      else if (email.includes('recruiter')) role = UserRole.RECRUITER;
      else if (email.includes('hiring')) role = UserRole.HIRING_MANAGER;
      else if (email.includes('interviewer')) role = UserRole.INTERVIEWER;
      
      const userSession: UserSession = {
        id: `user_${Date.now()}`,
        email,
        name: email.split('@')[0],
        role,
        permissions: getPermissionsForRole(role),
        accessToken: 'mock_jwt_token'
      };
      
      setUser(userSession);
      localStorage.setItem('auth_token', 'mock_jwt_token');
      localStorage.setItem('user_data', JSON.stringify(userSession));
      
    } catch (error) {
      console.error('Login failed:', error);
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  const loginWithGoogle = async () => {
    // Redirect to Google OAuth
    window.location.href = `${import.meta.env.VITE_API_URL || 'http://localhost:5000'}/api/auth/google`;
  };

  const logout = () => {
    setUser(null);
    localStorage.removeItem('auth_token');
    localStorage.removeItem('user_data');
    window.location.href = '/';
  };

  const hasPermission = (permission: Permission): boolean => {
    return user?.permissions.includes(permission) || false;
  };

  const value: AuthContextType = {
    user,
    isLoading,
    login,
    loginWithGoogle,
    logout,
    hasPermission
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};
