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
    setIsLoading(true);
    try {
      // Call real backend API for authentication
      const response = await fetch(`${import.meta.env.VITE_API_URL || 'http://localhost:5000'}/api/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      });

      if (!response.ok) {
        throw new Error('Invalid credentials');
      }

      const result = await response.json();
      const { access_token, user: backendUser } = result.data || result;

      const userSession: UserSession = {
        id: backendUser.id,
        email: backendUser.email,
        name: backendUser.name,
        role: backendUser.role as UserRole,
        permissions: getPermissionsForRole(backendUser.role as UserRole),
        accessToken: access_token,
      };

      setUser(userSession);
      localStorage.setItem('auth_token', access_token);
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
